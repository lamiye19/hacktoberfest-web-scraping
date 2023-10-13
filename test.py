from bs4 import BeautifulSoup

html_doc = "<html><body><p>Hello, World!</p><p>Encore Hello, World!</p></body></html>"

# Objet  Beautiful Soup
soup = BeautifulSoup(html_doc, 'html.parser')

""" paragraph = soup.find('p')
print(paragraph.text) """

paragraph = soup.find_all('p')
for p in paragraph:
    print(p)
