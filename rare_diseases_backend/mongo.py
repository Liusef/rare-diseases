from typing import List, Iterable, Tuple
import pymongo
from pymongo.cursor import Cursor
import colors as co


def query_id(client: pymongo.MongoClient, query: str):
    db = client["diseases"]
    collection = db["disease"]
    return collection.find_one({"id": query})


def query_tag(client: pymongo.MongoClient, query: str):
    db = client["diseases"]
    collection = db["tag"]
    return collection.find_one({"name": query})


def query_link_tag(client: pymongo.MongoClient, query: str) -> Cursor:
    db = client["diseases"]
    collection = db["links"]
    return collection.find({"tagid": query})

def query_link_id(client: pymongo.MongoClient, query: str) -> Cursor:
    db = client["diseases"]
    collection = db["links"]
    return collection.find({"disease": query})


def query_vec(client: pymongo.MongoClient, query: List[float], n_candidates: int, 
              limit: int = 0, filter: dict = None):
    db = client["diseases"]
    collection = db["vector store"]

    res = collection.aggregate([
        {
            '$vectorSearch': {
                "index": "indexEmbeddings",
                "path": "embedding",
                "queryVector": query,
                "numCandidates": n_candidates,
                "limit": limit if limit else n_candidates,
                "filter": filter,
            }
        }
    ])

    return res


def insert_vec(client: pymongo.MongoClient, vector: List[float], id: str):
    db = client["diseases"]
    collection = db["vector store"]
    doc = {
        "id": id,
        "embedding": vector
    }
    collection.insert_one(doc)


def insert_vec_many(client: pymongo.MongoClient, documents: Iterable[dict]):
    """
    **IMPORTANT** Remember to pass in your vectors as a dictionary in the following format:
    {
        "id": id,
        "embedding": embedding
    }

    Args:
        client (pymongo.MongoClient): MongoDB Client
        documents (Iterable[dict]): Iterable of documents in the above format
    """
    db = client["diseases"]
    collection = db["vector store"]
    collection.insert_many(documents)

def insert_disease(client: pymongo.MongoClient, document):
    assert "id" in document 
    assert "uri" in document 
    assert "tags" in document 
    assert "akas" in document 
    assert "overview" in document 
    assert "affected" in document

    # check if already exists
    db = client["diseases"]
    col = db["disease"]
    if len(col.find({"id": document["id"]}).limit(1)):
        print(f"{co.RED}ERROR:{co.RESET} Tried to insert duplicate")
        return 
    
    # links
    id = document["id"]
    _ins_tags(client, document["tags"])
    links = [{"tagid": tag, "disease": id} for tag in document["tags"]]
    linkcol = db["links"]
    linkcol.insert_many(links)

    document.pop('tags', None)
    col.insert_one(document)

def _ins_tags(client, tags):
    db = client["diseases"]
    col = db["tag"]
    tags = [{"name": tag} for tag in tags]
    col.update_many(tags, tags, upsert=True)


def _del_vec(client, id):
    db = client["diseases"]
    col = db["vector store"]
    col.delete_many({"id": id})

def _del_disease(client, id):
    db = client["diseases"]
    col = db["disease"]
    col.delete_many({"id": id})

def _del_link_id(client, id):
    db = client["diseases"]
    col = db["links"]
    col.delete_many({"disease": id})

def _del_link_tag(client, tag):
    db = client["diseases"]
    col = db["links"]
    col.delete_many({"tagid": tag})

def _del_tag(client, tag):
    db = client["diseases"]
    col = db["tag"]
    col.delete_many({"name": tag})


def delete_disease_id(client: pymongo.MongoClient, id: str):
    _del_vec(client, id)
    _del_disease(client, id)
    _del_link_id(client, id)

def delete_tag(client: pymongo.MongoClient, tag: str):
    _del_tag(client, tag)
    _del_link_tag(client, tag)

