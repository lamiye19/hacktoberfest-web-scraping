# HacktoberFest Lome 2023: Data Extraction

Ce dépôt a été créé pour documenter le workshop sur les outils et méthodes d'extration Web et PDF dans le cadre de Hacktoberfest. Ici, nous faisons l'extraction à partir des données sur le web. Retrouvez la documentation sur l'extraction à partir de fichiers PDF dans [ce dépôt](https://github.com/gausoft/hacktoberfest-pdf-tabular-data-extraction).

Présentation du [workshop (slides)](https://docs.google.com/presentation/d/1a_KG5tUcjo6759QEeSOEV2pZKi2roCQr/edit#slide=id.p25)

## Sur quelles données travaillons nous ?

Dans le cadre de cet atelier, exclusivement pour étude, nous collectons les données immobilières de quelques pays sur Coin Afrique. Le but

## Utilisation

### Étape 1: Installation des outils nécessaires

Dans le cadre de cet atelier, nous aurons besoin de :

```
pip install slugify
pip install requests
pip install beautifulsoup4
pip install pandas
```

### Étape 2: Mieux comprendre
Sur Coin Afrique, nous retrouvons les annonces immobilières sur ```https://{pays}.coinafrique.com/categorie/immobilier?page={page_num}```. C'est une pagination de plus de 30 pages qui contiennent au plus 84 annonces chacune.

Sur une page de plusieurs éléments, nous récupérons juste le lien vers chaque page de détails que nous précédons de ```https://{pays}.coinafrique.com/```

Sur la page détail d'un bien immobilier, il y a une balise « div » qui contient tous les informations du bien. Voici la structure

```
<div data-ad='{"address":"Lomé, Togo","amount_discount":0,"category":{"specialized_ad":202,"id":49,"illustration":"categorie_illustrations/20180103163542.png","name":"Terrains","occasion":false,"parent":{"name":"Immobilier","icon":"https://static.coinafrique.com/static/assets/categories/20180103163400.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/20180103163400_yellow.png","illustration":"categorie_illustrations/v1/20180103163400.png","range_id":"Range 270M","children":[{"name":"Villas","icon":"https://static.coinafrique.com/static/assets/categories/20180103163417.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/20180103163417_yellow.png","illustration":"categorie_illustrations/v1/20180103163417.png","range_id":"Range 270M","offer_type":["sell","rent"],"id":48,"expiration":365,"is_negociable_price_active":false,"specialized_ad":200},{"name":"Terrains","icon":"https://static.coinafrique.com/static/assets/categories/20180103163542.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/20180103163542_yellow.png","illustration":"categorie_illustrations/v1/20180103163542.png","range_id":"Range 270M","offer_type":["sell"],"id":49,"expiration":365,"is_negociable_price_active":false,"specialized_ad":202},{"name":"Appartements","icon":"https://static.coinafrique.com/static/assets/categories/20180103163436.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/20180103163436_yellow.png","illustration":"categorie_illustrations/v1/20180103163436.png","range_id":"Range 270M","offer_type":["sell","rent"],"id":51,"expiration":365,"is_negociable_price_active":false,"specialized_ad":201},{"name":"Immeubles","icon":"https://static.coinafrique.com/static/assets/categories/20180103163459.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/20180103163459_yellow.png","illustration":"categorie_illustrations/v1/20180103163459.png","range_id":"Range 850M","offer_type":["sell","rent"],"id":50,"expiration":365,"is_negociable_price_active":false,"specialized_ad":203},{"name":"Bureaux &amp; Commerces","icon":"https://static.coinafrique.com/static/assets/categories/20180103163525.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/20180103163525_yellow.png","illustration":"categorie_illustrations/v1/20180103163525.png","range_id":"Range 270M","offer_type":["sell","rent"],"id":60,"expiration":365,"is_negociable_price_active":false,"specialized_ad":204},{"name":"Maisons de vacances","icon":"https://static.coinafrique.com/static/assets/categories/vacances.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/vacances_yellow.png","illustration":"categorie_illustrations/v1/vacances.png","range_id":"Range 2,5M","offer_type":["rent"],"id":206,"expiration":365,"is_negociable_price_active":false,"specialized_ad":200},{"name":"Chambres","icon":"https://static.coinafrique.com/static/assets/categories/chambres.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/chambres_yellow.png","illustration":"categorie_illustrations/v1/chambres.png","range_id":"Range 150K","offer_type":["rent"],"id":205,"expiration":365,"is_negociable_price_active":false,"specialized_ad":204},{"name":"Terrains agricoles","icon":"https://static.coinafrique.com/static/assets/categories/agricole.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/agricole_yellow.png","illustration":"categorie_illustrations/v1/agricole.png","range_id":"Range 270M","offer_type":["sell","rent"],"id":253,"expiration":365,"is_negociable_price_active":false,"specialized_ad":202},{"name":"Appartements meublés","icon":"https://static.coinafrique.com/static/assets/categories/apt_meubles.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/apt_meubles_yellow.png","illustration":"categorie_illustrations/v1/apt_meubles.png","range_id":"Range 270M","offer_type":["sell","rent"],"id":254,"expiration":365,"is_negociable_price_active":false,"specialized_ad":201},{"name":"Fermes &amp; Vergers","icon":"https://static.coinafrique.com/static/assets/categories/fermes.png","icon_selected":"https://static.coinafrique.com/static/assets/categories/fermes_yellow.png","illustration":"categorie_illustrations/v1/fermes.png","range_id":"Range 270M","offer_type":["sell","rent"],"id":255,"expiration":365,"is_negociable_price_active":false,"specialized_ad":202}],"id":14,"expiration":365,"is_negociable_price_active":false,"specialized_ad":2,"occasion":false}},"currency":"CFA","date_creation":"2023-10-06T17:15:00Z","date_listing":"2023-10-15T17:56:13Z","deal_type":0,"description":"A vendre\n1 lot(600m2) angle rue a 100m du goudron\ndocument : titre foncier\nquartier : agoe sogbossito oando a 100m du goudron\nprix :45 000 000fcfa a débattre","duration":"2023-12-05T17:15:00Z","geolocation":{"lat":6.1256261,"lng":1.2254183},"id":4405927,"images":[{"thumb":"https://images.coinafrique.com/thumb_4405927_uploaded_image1_1696612501.jpg","normal":"https://images.coinafrique.com/4405927_uploaded_image1_1696612501.jpg"},null,null,null,null,null],"is_delivery":false,"is_discount":false,"is_exchange_accepted":false,"is_favorite":false,"is_financeable":false,"is_new":false,"is_own_ad":false,"is_top_ad":false,"is_urgent":false,"moderation_message":"","phone":"+22892690325","photos":{"photo2":null,"photo3":null,"photo1":{"thumb":"https://images.coinafrique.com/thumb_4405927_uploaded_image1_1696612501.jpg","normal":"https://images.coinafrique.com/4405927_uploaded_image1_1696612501.jpg"}},"price":45000000,"specialized_ad":202,"state":"2","title":"Terrain 600 m² - Agoe Sogbossito","user":{"geolocation":{"lat":6.1256261,"lng":1.2254183},"photo":"","phone":"92690325","published_ads":1078,"address":"Togo","whatsapp_phone":"+22892690325","name":"Immo Goodluck","uuid":"4f76c5c6-8a8e-4be4-a39c-bdbb2c49adb8","member_since":"2019-07-03T05:46:44Z","email":"","is_pro":true},"view_nbr":87,"re_room":0,"re_bathroom":0,"re_offer_type":"sell","re_surface":600,"re_surface_unit":"m2","country_code":"TG","photosCount":1}'
    data-ad-address="Lomé, Togo" data-ad-locality="Lomé, Togo" data-ad-price="45000000"
    data-ad-title="Terrain 600 m² - Agoe Sogbossito" data-category-id="49" data-category-name="Terrains"
    data-country='{"devise":{"id":1,"nom":"CFA","negotiable_limit":100},"id":21,"active":true,"code":"TG","financing_available":false,"latitude":8.619543,"longitude":0.824782,"nom":"Togo","phone_code":"+228","monetization_enabled":true,"is_pro_feature_enabled":true,"is_subscription_feature_enabled":true,"prefix":"au"}'
    data-country-id="21" data-geolocation='{"lat":6.1256261,"lng":1.2254183}' data-mobile="92690325"
    data-post-id="4405927" data-user-id="4f76c5c6-8a8e-4be4-a39c-bdbb2c49adb8" id="ad-details">
</div>
```



## Ressources pour aller plus loin

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pandas.pydata.org/docs/)

## Clause de non-responsabilité

Ce code a été écrit exclusivement dans le cadre de cet apprentissage. Une mauvaise utilisation de celui ci peut être nuisible pour le site et l'auteur se désengage de toute responsabilité liée à son utilisation. Veuillez respecter les lois sur la protection des données et les droits d'auteur lors de l'utilisation de ce code.