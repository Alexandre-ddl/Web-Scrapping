import requests
from bs4 import BeautifulSoup

def get_sitemap_urls(sitemap_index_url):
    # Télécharge le contenu de l'index sitemap
    response = requests.get(sitemap_index_url)
    # Utilisez 'html.parser' comme solution de secours
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trouve tous les éléments <loc> qui contiennent les URLs des sitemaps
    sitemap_urls = [loc.text for loc in soup.find_all('loc')]
    
    return sitemap_urls

def get_page_urls(sitemap_urls):
    page_urls = []
    for sitemap_url in sitemap_urls:
        # Télécharge chaque sitemap individuel
        response = requests.get(sitemap_url)
        # Utilisez 'html.parser' ici aussi
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrait les URLs des pages
        page_urls.extend([loc.text for loc in soup.find_all('loc')])
    
    return page_urls

sitemap_index_url = 'https://www.boticinal.com/sitemap.xml'

sitemap_urls = get_sitemap_urls(sitemap_index_url)

page_urls = get_page_urls(sitemap_urls)


import re 
def filter_urls(page_urls, pattern):
    # Compile the regex pattern
    regex = re.compile(pattern)
    # Filter the URLs
    filtered_urls = [url for url in page_urls if regex.search(url)]
    return filtered_urls

pattern = r'https://www\.boticinal\.com/.+\.html$'

# Filtrer les URLs en utilisant le modèle défini
filtered_urls = filter_urls(page_urls, pattern)

import pickle
with open('html_products_boticinal.pkl', 'wb') as fichier:
    pickle.dump(filtered_urls, fichier)