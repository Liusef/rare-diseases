from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import time
import json
from pathlib import Path

"https://rarediseases.org/rare-diseases/page/1/?starts_with=A"

driver = webdriver.Chrome()
data = {}
base_url = Path("https://rarediseases.org/rare-diseases/")
current_letter = "A"

def extract_page_data(current_page):
    url = str(base_url / f'page/{current_page}/?starts_with={current_letter}')
    print(len(data.keys()), url)
    driver.get(url)

    articles: List[WebElement] = driver.find_elements(By.XPATH, '//article')
    
    for article in articles:
        anchor = article.find_element(By.XPATH, 'h5/a')
        aka = article.find_elements(By.XPATH, 'p/span')
        link = anchor.get_attribute('href')
        
        article_data = {
            'aka': [nick.text for nick in aka],
            'uri': link
        }
        data[anchor.text] = article_data
        
    print("extracted page data")


def extract_letter_data():
    driver.get(str(base_url / f'page/1/?starts_with={current_letter}'))
    all_page_nums = driver.find_elements(By.XPATH, '//div[2]/div/div[2]/div[4]/div/ol/li')

    num_pages = max(1, len(all_page_nums) - 2)

    for i in range(num_pages):
        current_page = i + 1
        extract_page_data(current_page)

driver.get(str(base_url / f'?starts_with={current_letter}'))
all_letters = driver.find_elements(By.XPATH, '//div[2]/div/div[2]/div[2]/a')
all_letters = [a.text for a in all_letters]
print(all_letters)

for letter in all_letters:
    current_letter = letter
    extract_letter_data()

with open(Path(__file__).parent / 'scraper-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
         
driver.close()