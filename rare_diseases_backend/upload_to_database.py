from pathlib import Path
import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector
from psql import get_connection
from collections import Counter

import json

BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent

disease_path = ROOT_DIR / 'rare_diseases_scraper' / 'scraper-data.json'
vector_path = ROOT_DIR / 'rare_diseases_embeddings' / 'vector_data.json'

with open(disease_path, encoding='utf-8') as f:
    diseases = json.load(f)

with open(vector_path, encoding='utf-8') as f:
    vectors = json.load(f)

connection = get_connection()
register_vector(connection)

cursor = connection.cursor()

print('Adding keywords')
kw_counter = Counter()
for disease in diseases:
    value = diseases[disease]
    kw_counter.update([v.casefold() for v in value['symptom_list']])

kw_rows = list(kw_counter.items())
cursor.executemany('insert into keyword (name, count) values (%s, %s) on conflict do nothing', kw_rows)

print('Adding diseases')
disease_rows = []
for disease in diseases:
    value = diseases[disease]
    disease_row = (disease.casefold(), value['uri'].casefold(), value['affected_text'], value['symptom_text'])
    disease_rows.append(disease_row)

cursor.executemany('insert into disease (name, url, affected_text, symptom_text) values (%s, %s, %s, %s) on conflict do nothing', disease_rows)

print('Getting ids for disease/keywords (future insertions)')
cursor.execute('select id, name from disease')
disease_ids = cursor.fetchall()
disease_ids = {name: id for id, name in disease_ids}

cursor.execute('select id, name from keyword')
keyword_ids = cursor.fetchall()
keyword_ids = {name: id for id, name in keyword_ids}


print('Adding disease keywords')
disease_keywords_rows = []
for disease in diseases:
    value = diseases[disease]
    dk_row_extend = [(disease_ids[disease.casefold()], keyword_ids[keyword.casefold()]) for keyword in value['symptom_list']]
    disease_keywords_rows.extend(dk_row_extend)

cursor.executemany('insert into disease_keyword (disease_id, keyword_id) values (%s, %s) on conflict do nothing', disease_keywords_rows)

print('Adding disease embeddings')
embedding_rows = []
for disease in vectors:
    embeddings = vectors[disease]
    
    embeddings_extend = [(disease_ids[disease.casefold()], np.array(embed)) for embed in embeddings]
    embedding_rows.extend(embeddings_extend)
    
cursor.executemany('insert into disease_embeddings (disease_id, embedding) values (%s, %s) on conflict do nothing', embedding_rows)

connection.commit()