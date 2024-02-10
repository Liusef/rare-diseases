from pathlib import Path
from run_embeddings import EmbedDiseaseSymptoms
import json


BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent

scraper_file = ROOT_DIR / 'rare_diseases_scraper' / 'scraper-data.json'

with open(scraper_file, encoding='utf-8') as f:
    scraper_data = json.load(f)
    

with open(BASE_DIR / 'vector_data.json', encoding='utf-8') as f:
    vec_data = json.load(f)

embedder = EmbedDiseaseSymptoms()

keys = list(scraper_data.keys())
total = len(keys)
for i, disease in enumerate(keys):
    print(f"Embedding for {disease} ({i+1}/{total})")
    value = scraper_data[disease]
    if not value.get('symptom_text'):
        continue
    
    if disease in vec_data:
        continue
    
    document = value['symptom_text']
    embeddings = embedder.encode_document(document)
    json_friendly_embeddings = [e.tolist() for e in embeddings]
    
    vec_data[disease] = json_friendly_embeddings
    if ((i+1) % 20) == 0:
        with open(BASE_DIR / 'vector_data.json', 'w') as f:
            json.dump(vec_data, f)


with open(BASE_DIR / 'vector_data.json', 'w') as f:
    json.dump(vec_data, f)