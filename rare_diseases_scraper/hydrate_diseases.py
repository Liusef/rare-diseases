import json
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import time
import re
import logging

logging.disable(logging.INFO)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('log-level=3')

driver = webdriver.Chrome(options=options)

with open(Path(__file__).parent / 'scraper-data.json', encoding='utf-8') as f:
    data = json.load(f)


def get_p_data(parent: WebElement):
    p_elements = parent.find_elements(By.TAG_NAME, "p")
    text = " ".join([p.get_attribute("textContent") for p in p_elements])
    return text

keys = list(data.keys())
total = len(keys)
for i, disease in enumerate(keys):
    print(f"Collecting for {disease} ({i+1}/{total})")
    start = time.perf_counter()
    value = data[disease]
    url = value['uri']

    if value.get('symptom_text', None):
        continue
    
    # Collect symptoms text
    driver.get(str(Path(url)))
    try:
        symptoms = driver.find_element(By.CSS_SELECTOR, '#symptoms')
        symptoms_text = get_p_data(symptoms)
    except NoSuchElementException:
        symptoms_text = ''
        
    symptom_list = re.findall(r'\((.+?)\)', symptoms_text)
    value['symptom_text'] = symptoms_text
    value['symptom_list'] = symptom_list

    # Collect Affected Populations
    try:
        affected = driver.find_element(By.CSS_SELECTOR, '#affected')
        affected_text = get_p_data(affected)
    except NoSuchElementException:
        affected_text = ''

    value['affected_text'] = affected_text
    
    with open(Path(__file__).parent / 'scraper-data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    if ((i+1) % 100) == 0:
        print("restarting chrome (memory D:<)")
        driver.close()
        driver = webdriver.Chrome(options=options)
    
    time.sleep(0.5)
    end = time.perf_counter()
    print(f"Time left: {(end-start)*(total-(i+1))/60:.2f}minutes")

with open(Path(__file__).parent / 'scraper-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

