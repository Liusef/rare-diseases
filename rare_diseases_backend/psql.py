from pathlib import Path
import psycopg2
from psycopg2.extensions import connection
from pgvector.psycopg2 import register_vector
import numpy as np
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent

load_dotenv(ROOT_DIR / '.env', override=True)

dbname=os.getenv('POSTGRES_DB')
user=os.getenv('POSTGRES_DB')
password=os.getenv('POSTGRES_PASSWORD')
host=os.getenv('HOST_NAME')
port=os.getenv('HOST_PORT')

def get_connection():
    return psycopg2.connect(f"dbname={dbname} user={user} password={password} host={host} port={port}")

# Do all the fun stuff here :)

def get_diseases(conn: connection):
    cursor = conn.cursor()
    cursor.execute('select * from disease')
    res = cursor.fetchall()
    
    return res

def get_disease_by_name(conn: connection, name):
    cursor = conn.cursor()
    cursor.execute('select d.name, d.url, d.affected_text, d.symptom_text from disease d where d.name = %s', (name,))
    res = cursor.fetchone()
    
    return res

def get_keywords_fuzzy(conn: connection, key_partial):
    cursor = conn.cursor()
    cursor.execute("""select k.name from keyword k where k.name ~*  %s""", (key_partial,))

    res = cursor.fetchall()
    
    return res

def get_exact_keywords(conn: connection, query):
    cursor = conn.cursor()
    cursor.execute("""select k.name from keyword k where %s ILIKE '%%' || k.name || '%%'""", (query,))
    res = cursor.fetchall()
    return res

def get_disease_by_embedding(conn: connection, embedding: np.ndarray):
    register_vector(conn)
    cursor = conn.cursor()
    cursor.execute("""select d.name from disease_embeddings de 
                   left join disease d on d.id = de.disease_id 
                   order by (de.embedding <=> %s) limit 50""", (embedding,))
    
    res = cursor.fetchall()
    
    return res

def get_diseases_with_keyword(conn: connection, keyword):
    cursor = conn.cursor()
    cursor.execute('''select d.name from disease d 
                   join disease_keyword dk on dk.disease_id = d.id 
                   join keyword k on dk.keyword_id = k.id 
                   where k.name = %s''', (keyword,))
    res = cursor.fetchall()
    if res:
        return [r[0] for r in res]


def get_keyword_count(conn: connection, name):
    cursor = conn.cursor()
    cursor.execute('select k.count from keyword k where k.name = %s', (name,))
    res = cursor.fetchone()
    if not res:
        return
    
    return res[0]