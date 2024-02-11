from flask import Flask
from dotenv import load_dotenv
from psql import *
from flask import request
from utils import vote_by_pareto, vote_by_pareto_pow, vote_by_pareto_sqrt, disease_row_to_object
from scipy.special import softmax
from run_embeddings import EmbedDiseaseSymptoms
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv(override=True)

app = Flask(__name__)
embedder = EmbedDiseaseSymptoms()


@app.route("/get_keywords", methods=['GET'])
def get_keywords():
    connection = get_connection()
    result = {}
    
    query = request.args.get('q')
    
    if not query:
        return result
    
    print(query)
    exact_keywords = get_exact_keywords(connection, query)
    if not exact_keywords:
        return result 
    
    keywords = [res[0] for res in exact_keywords]
    result['results'] = keywords
    
    return result

@app.route("/get_possible_keywords", methods=['GET'])
def get_possible_keywords():
    connection = get_connection()
    result = {}
    
    query = request.args.get('q')
    
    if not query:
        return result
    
    keywords = get_keywords_fuzzy(connection, query)
    if not keywords:
        return result
    keywords = [k[0] for k in keywords]
    result['results'] = keywords
    
    return result

@app.route("/get_disease_results", methods=['GET'])
def get_disease_results():
    connection = get_connection()
    
    result = {'results':[]}
    
    query = request.args.get('q')
    limit = 10
    
    if not query:
        return result
    
    embedding = embedder.encode_query(query)
    embedding = np.average(embedding, 0)
    
    diseases = get_disease_by_embedding(connection, embedding)
    if not diseases:
        return result

    diseases = [disease[0] for disease in diseases]
    votes = vote_by_pareto(diseases)
    
    counter = {}
    for disease, vote in zip(diseases, votes):
        counter.update({disease: counter.get(disease, 0) + vote})
    
    # DO BASED OFF OF TAGS EXISTING IN MODEL:
    kw_weight = 1
    keywords = get_exact_keywords(connection, query)
    if keywords:
        keywords = set([k[0] for k in keywords])
        for keyword in keywords:
            diseases_to_add = get_diseases_with_keyword(connection, keyword)
            keyword_count = get_keyword_count(connection, keyword)
            for disease in diseases_to_add:
                counter.update({disease: counter.get(disease, 0) + (kw_weight/keyword_count)})
                pass
    
    
    items = list(counter.items())
    items.sort(key= lambda x: x[1], reverse=True)
    diseases, scores = zip(*items)

    diseases, scores = diseases[:limit], scores[:limit]
    
    scores = softmax(scores)
    for disease, score in zip(diseases, scores):
        row = get_disease_by_name(connection, disease)
        disease_obj = disease_row_to_object(row)
        disease_obj['probability'] = score
        result['results'].append(disease_obj)
    
    return result
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")