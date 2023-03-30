import os
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Chrome driver'ı başlat /start chrome driver
driver = webdriver.Chrome()

# Birden fazla anahtar kelime aratmak için anahtar kelimelerin listesi /List of keywords to search for multiple keywords
keywords = ['flowers','view', 'see']

# Anahtar kelimeler için döngü/Loop for keywords
for keyword in keywords:

    # Google Images'a git /Go to Google Images
    driver.get("https://www.google.com/imghp")

    # Arama kutusunu bul ve anahtar kelimeyi arat /Find the search box and search for the keyword
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(keyword)
    search_box.submit()

    # Sayfayı aşağı doğru kaydır /Scroll down the page
    elem = driver.find_elements(By.TAG_NAME,"body")


    # Scroll yaparak tüm resimlerin yüklenmesini sağla /Make all images load by scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Sayfayı en aşağıya kaydır /Scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Yeni resimler yüklendi mi kontrol et /Check if new images have been uploaded
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Resimleri bul ve indir /Find and download images
    # Resimler "nature" dosyasına kaydedilir / pictures are saved in "nature" file
    images = driver.find_elements(By.CSS_SELECTOR, "img.rg_i")
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'nature')
    for i, image in enumerate(images):
        # Resim URL'sini al /Get image URL
        image_url = image.get_attribute("src")
        if image_url is not None:
            # Resim URL'sini kullanarak dosya adını oluştur /Generate filename using image URL
            filename = os.path.join(desktop_path, f"nature_{i}.jpg")
            # Resmi indir /Download image
            urllib.request.urlretrieve(image_url, filename)

# Chrome driver'ı kapat /Turn off chrome driver
driver.quit()
