import os
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Chrome driver'ı başlat /start chrome driver
driver = webdriver.Chrome('/path/to/chromedriver')

# Yandex Görseller'e git /Go to Yandex Images
driver.get("https://yandex.com/images/")

# Arama kutusunu bul ve "flowers" kelimesini arat/Find the search box and search for "flowers"
# "flowers" yerine aramak istediğin görselin adını yaz /Write the name of the image you want to search instead of "flowers"

# ActionChains kullanarak arama kutusuna yazı yazdırma/Printing text in search box using ActionChains
search_box = driver.find_element(By.NAME, "text")
actions = ActionChains(driver)
actions.move_to_element(search_box).click().send_keys("flowers").send_keys(Keys.ENTER).perform()


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

# Resimleri bul ve indir flowers dosyasına kaydet /Find and download pictures save to flowers file
images = driver.find_elements(By.CSS_SELECTOR,"img.serp-item__thumb")
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'flowers')
for i, image in enumerate(images):
    # Resim URL'sini al /Get image URL
    image_url = image.get_attribute("src")
    if image_url is not None:
        # Resim URL'sini kullanarak dosya adını oluştur /Generate filename using image URL
        filename = os.path.join(desktop_path, f"flower_{i}.jpg")
        # Resmi indir /Download image
        urllib.request.urlretrieve(image_url, filename)

# Chrome driver'ı kapat/Turn off chrome driver
driver.quit()
