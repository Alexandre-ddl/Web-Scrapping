from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
from urllib.parse import urlparse
from multiprocessing import Process
import pickle


def Selenium_images(https):

    options = ChromeOptions()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(options=options)

    driver.get(https)


    # Extraire le titre de la page et formater pour le nom du fichier
    page_title = driver.title.split('|')[0].strip().replace(' ', '_').replace(',', '').replace('-', '_')

    images = driver.find_elements(By.CSS_SELECTOR, ".fotorama__stage img")


    folder_name = 'images/'+page_title
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


    for img in images:
        img_url = img.get_attribute('src')
        # Extraire le nom du fichier de l'URL de l'image
        img_filename = urlparse(img_url).path.split('/')[-1]
        # Chemin complet pour sauvegarder l'image
        save_path = os.path.join(folder_name, img_filename)
        
        # Télécharger et sauvegarder l'image
        img_data = requests.get(img_url).content
        with open(save_path, 'wb') as handler:
            handler.write(img_data)
        #print(f'Image téléchargée et sauvegardée sous : {save_path}')

    driver.quit()

if __name__ == '__main__':


    with open('../Get html link/html_products_boticinal.pkl', 'rb') as fichier:
        urls = pickle.load(fichier)

    processes = []

    for url in urls[:4]:
        print('url : ',url)
        p = Process(target=Selenium_images, args=(url,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()