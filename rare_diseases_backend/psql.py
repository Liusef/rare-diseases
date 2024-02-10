from pathlib import Path
import psycopg2
from psycopg2.extensions import connection
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
    cursor.execute('select * from disease d where d.name = %s', (name,))
    res = cursor.fetchone()
    
    return res