from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import time

driver = webdriver.Chrome()
driver.get("https://rarediseases.org/rare-diseases/?starts_with=A")

scraper_txt = open("scraper-data.json", 'w').close() # clear current txt file

scraper_txt = open("scraper-data.json", 'a')
scraper_txt.write('{\n')

def extract_page_data(driver):
    articles: List[WebElement] = driver.find_elements(By.XPATH, '//article')
    
    for article in articles:
        
        anchor = article.find_element(By.XPATH, 'h5/a')
        aka = article.find_elements(By.XPATH, 'p/span')
        link = anchor.get_attribute('href')
        
        scraper_txt.write(f'    "{anchor.text}" : {{\n')
        
        scraper_txt.write('        "aka": [\n')
        
        for nickname in aka:
            scraper_txt.write(f'            "{nickname.text}",\n')
        
        scraper_txt.write('        ],\n')
        scraper_txt.write(f'        "uri": "{link}",\n    }},\n\n')

    print("extracted page data")


def extract_letter_data(driver):
    all_page_nums = driver.find_elements(By.XPATH, '//div[2]/div/div[2]/div[4]/div/ol/li')
    number_of_pages = 0
    if (len(all_page_nums) == 0):
        number_of_pages = 1
    else:
        number_of_pages = int(all_page_nums[-2].text)

    for page_num in range(number_of_pages):
        
        extract_page_data(driver)
        print(page_num)

all_letters = driver.find_elements(By.XPATH, '//div[2]/div/div[2]/div[2]/a')

for letter in range(len(all_letters)):
    extract_letter_data(driver)
    print(letter)

scraper_txt.write('}\n')
scraper_txt.close()
driver.close()