# Auteur : Sémiat Oyénikè Olaitan
# Date : 10 Octobre 2023
#
# Ce programme collecte les données immobilières sur Coin Afrique.





import os
import time
from slugify import slugify
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd



liste_pays = ['tg', 'bj', 'sn', 'ci', 'cm', 'bf',
         'cg', 'ga', 'gn', 'ml', 'ne', 'cd']


# Récupère "count" pages de biens immobiliers à partir de la page numero "de"
# pour le pays "pays".
def get_pages(count=1, de=1, pays='tg'):
    if de < 1:
        print("La page", de, " n'existe pas.")
        return 0
    
    pause = 0
    nb = 1
    filename = f"datas/donnee-"
    cleaned_filename = f"datas/cleaned/donnee-"
    country_filename = f"{filename}{pays}"
    country_cleaned_filename = f"{cleaned_filename}{pays}"

    # Vérifier si les fichiers existent pour les complèter ou créer
    if os.path.exists(f"{country_filename}.csv"):
        global_result = pd.read_csv(f"{country_filename}.csv")
    else:
        global_result = pd.DataFrame()

    if os.path.exists(f"{country_cleaned_filename}.csv"):
        global_cleaned_result = pd.read_csv(f"{country_cleaned_filename}.csv")
    else:
        global_cleaned_result = pd.DataFrame()

    # Lien de base
    url = f"https://{pays}.coinafrique.com/categorie/immobilier"
    a_page_url = f"https://{pays}.coinafrique.com"

    for page_num in range(de, count + de):
        if page_num == 1:
            page_url = url
        else:
            page_url = url + f"?page={page_num}"

        print('\nCOLLECTE DE LA PAGE - ', page_num)
        response = requests.get(page_url)
        page = response.content

        # liste des liens des articles
        links = parse_page(page)

        print('Récupérer les pages de détails.\n')
        i = 0
        result = pd.DataFrame()
        for link in links:
            i += 1
            complete_link = a_page_url + link
            response = requests.get(complete_link)

            # Extraire les données sur la page détails
            annonce = parse_annonce(response.content)

            # Ajouter la nouvelle donnée aux anciennes
            result = pd.concat([result, annonce], axis=0)
            print('Annonce', i, ": Récupérée\n")

        if i == 0:
            print('\n ------ FIN DE CHARGEMENTS ------ \n')
            break
        else:
            print('\n------ Annonces chargé avec success ------ \n')

        global_result = pd.concat([global_result, result], axis=0)

        print('NETTOYAGE DES DONNÉES \n')
        # Enlever les doublons
        #global_result.drop_duplicates(inplace=True)

        # Remplir les champs sans valeur avec un caractère vide
        result.fillna('', inplace=True)

        # Trie: les biens qui ne sont pas en location
        # result = result[result['transaction'] != "rent"]

        global_cleaned_result = pd.concat([global_cleaned_result, result], axis=0)
        #global_cleaned_result.drop_duplicates(inplace=True)

        # Faire une pause après 5 pages
        if nb > pause + 5:
            print('... pause ...')
            time.sleep(60)
            pause += nb
        nb += 1
            
        print('SAUVEGARDE DES DONNÉES \n')
        global_result.to_csv(f"{country_filename}.csv", sep=',', index=False)
        global_cleaned_result.to_csv(f"{country_cleaned_filename}.csv", sep=',', index=False)

        # format json
        global_cleaned_result.to_json(f"{country_cleaned_filename}.json", orient='records')



    return 0

# Analyse une page des biens et retourne les liens vers les pages détails de chaque élément
def parse_page(page):
    soup = BeautifulSoup(page, "html.parser")

    # Chercher les balises ayant l'attribut class="ad__card-image" et récupérer les liens
    links = [ a['href'] for a in soup.find_all(attrs={"class": "ad__card-image"}) ]
    
    return links


# Extrait les données sur la page détails
def parse_annonce(page):
    soup = BeautifulSoup(page, "html.parser")
    result = pd.DataFrame()

    details = soup.find(attrs={"id": "ad-details"})
    if not details:
        return result
    
    result["id"] = [details["data-post-id"]]

    # L'attribut "data-ad-title" est sous le format TITRE [à/-] QUARTIER
    # Nous avons adopté la forme [-] en remplaçant "à" par "-"
    titre = details["data-ad-title"].replace(" à ", " - ").strip().split(" - ")
    result["titre"] = [titre[0]]
    result['slug'] = [slugify(titre[0])]
    if len(titre) > 1:
        result["quartier"] = [titre[1]]

    result["prix"] = [details["data-ad-price"]]
    result["categorie"] = [details["data-category-name"]]
    result["pays"] = [json.loads(details["data-country"].replace("'", "\""))]

    # L'attribut "data-ad-locality" est sous le format VILLE[,] PAYS
    # O VILLE[,] PRECISION SUR LA VILLE[,]PAYS
    result["adresse"] = [details["data-ad-locality"]]
    ville = details["data-ad-address"].split(",")
    if len(ville) > 2:
        result["ville"] = [ville[1]]
    else:
        result["ville"] = [ville[0]]
    
    geolocation = json.loads(details["data-geolocation"])
    result["latitude"] = [geolocation["lat"]]
    result["longitude"] = [geolocation["lng"]]

    annonce = json.loads(details["data-ad"])

    result["montant_remise"] = [annonce["amount_discount"]]
    result["description"] = [annonce["description"]]
    result["date_creation"] = [annonce["date_creation"]]
    result["duree"] = [annonce["duration"]]
    result["date_publication"] = [annonce["date_listing"]]
    result["type_deal"] = [annonce["deal_type"]]
    result["est_livree"] = [annonce["is_delivery"]]
    result["a_remise"] = [annonce["is_discount"]]
    result["accepte_echange"] = [annonce["is_exchange_accepted"]]
    result["est_favoris"] = [annonce["is_favorite"]]
    result["est_financeable"] = [annonce["is_financeable"]]
    result["est_nouveau"] = [annonce["is_new"]]
    result["est_proprietaire"] = [annonce["is_own_ad"]]
    result["est_top"] = [annonce["is_top_ad"]]
    result["est_urgent"] = [annonce["is_urgent"]]
    result["message_moderation"] = [annonce["moderation_message"]]
    result["etat"] = [annonce["state"]]  # 1,2,3

    if "re_room" in annonce:
        result["nb_chambre"] = [annonce["re_room"]]
    else:
        result["nb_chambre"] = [0]

    if "re_bathroom" in annonce:
        result["nb_salle_bain"] = [annonce["re_bathroom"]]
    else:
        result["nb_salle_bain"] = [0]

    if "re_surface" in annonce:
        result["surface"] = [annonce["re_surface"]]
    else:
        result["surface"] = [0]

    if "re_surface_unit" in annonce:
        result["unite_surface"] = [annonce["re_surface_unit"]]
    else:
        result["unite_surface"] = ["m²"]

    result["nb_photo"] = [annonce["photosCount"]]
    result["images"] = [annonce["images"]]

    if "re_offer_type" in annonce:
        result["transaction"] = [annonce["re_offer_type"]]
    else:
        result["transaction"] = [""]


    # Pour la cote d'ivoire, il faut utiliser ce code
    # result["pays"] = [details["data-country"].replace("'", "\"")]
    result["agent"] = [annonce["user"]]

    # Dans le cas où les informations sont à récupérer dans différentes balises
    # result["description"] = [soup.find(attrs={"class": "ad__info__box ad__info__box-descriptions"}).contents[1].text]
    return result



if __name__ == "__main__":
    print('Ce programme collecte les données immobilières sur Coin Afrique.\n')

    for pays in liste_pays:
        print('PAYS:', pays, '\n')
        get_pages(count=30, de=3, pays=pays)

