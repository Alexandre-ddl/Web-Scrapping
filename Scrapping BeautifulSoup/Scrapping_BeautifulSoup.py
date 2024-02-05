import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import pickle

def clean_filename(url):
    filename = url.split('/')[-1].split('?')[0]
    if not filename.lower().endswith(('.png', '.jpeg', '.jpg')):
        filename += '.jpeg'
    return filename

def get_product_info(url, save_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Récupère le titre de la page
    page_title = soup.select_one('title').text if soup.select_one('title') else 'No Title'
    
    product_images = soup.find_all('img', {'alt': 'main product photo', 'class': 'gallery-placeholder__image'})

    description_text = soup.find('div', id='description').get_text(strip=True) if soup.find('div', id='description') else "Description not available"

    composition_div = soup.find('div', id='composition').get_text(strip=True) if soup.find('div', id='composition') else "Composition not available"

    conseil_div = soup.find('div', id='conseil').get_text(strip=True) if soup.find('div', id='conseil') else "Conseil not available"

    brand  = soup.find('a' , class_ = 'product-brand-link').get_text(strip=True) 
    
    category_spans = soup.find_all('span', class_='category')

    id_bio = soup.find('span', class_='is_bio').get_text(strip=True)

    weight_unit = soup.find('span', class_='weight_unit').get_text(strip=True)

    manufacturer = soup.find('span', class_='manufacturer').get_text(strip=True)

    gtin = soup.find('span', class_='gtin').get_text(strip=True)

    categories_text = [span.get_text() for span in category_spans]
    products = []
    
    for img in product_images:
        image_url = img['src']
        img_response = requests.get(image_url, stream=True)
        
        if img_response.status_code == 200:
            filename = clean_filename(image_url)
            filepath = os.path.join(save_path, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)
            
            #print(f'L\'image a été téléchargée et sauvegardée sous : {filepath}')
            products.append({
                'filename': filename,
                'title': page_title,
                'description': description_text,
                'composition' : composition_div,
                'conseil' : conseil_div,
                'catégories' :  categories_text ,
                'brand' :  brand,
                'is_bio' : id_bio,
                'weight_unit' : weight_unit,
                'manufacturer' : manufacturer,
                'gtin' : gtin,

            })
        else:
            print('Échec du téléchargement de l\'image.')

    return products  
 

# Fonction pour sauvegarder les données dans un fichier CSV en mode ajout
def save_to_csv(products, save_path, csv_filename="product_images.csv"):
    # Chemin complet du fichier CSV
    csv_path = os.path.join(save_path, csv_filename)
    
    # Crée un DataFrame à partir des produits
    df = pd.DataFrame(products)
    
    # Vérifie si le fichier existe déjà pour décider de l'en-tête
    header = not os.path.exists(csv_path)
    
    # Ajoute les données au fichier CSV, 'a' pour append, ajout à la fin
    df.to_csv(csv_path, mode='a', index=False, header=header, encoding='utf-8')
    #print(f'Les données ont été ajoutées dans {csv_path}')


test = True 
if test :
    #url = 'https://www.boticinal.com/la-roche-posay-toleriane-sensitive-creme-hydratante-anti-rougeurs-40ml.html'
    #url = 'https://www.boticinal.com/la-roche-posay-effaclar-gel-moussant-nettoyant-visage-anti-boutons-anti-points-noirs-400ml.html'
    url = 'https://www.boticinal.com/mavala-vernis-a-ongles-305-samarkand-5ml.html'
    save_path = "images"  # Ou spécifiez un chemin de répertoire
    products    = get_product_info(url, save_path)

    # Sauvegarde des informations dans un fichier CSV
    save_to_csv(products,"")

else :
    with open('../Get html link/html_products_boticinal.pkl', 'rb') as fichier:
            urls = pickle.load(fichier)

    for url in urls[::-1][::10]:
        save_path = "images"  
        products  = get_product_info(url, save_path)

        # Sauvegarde des informations dans un fichier CSV
        save_to_csv(products,"")