import numpy as np

from psql import get_disease_by_name


def vote_by_pareto(diseases):
    votes = 1/(np.arange(len(diseases))+1)
    
    return votes
    
def vote_by_pareto_sqrt(diseases):
    return np.sqrt(vote_by_pareto(diseases))

def vote_by_pareto_pow(diseases, pow):
    return np.power(vote_by_pareto(diseases), pow)

def disease_row_to_object(disease_row):
    name, url, affected_text, symptom_text = disease_row
    
    obj = {
        'name': name,
        'url': url,
        'affected_text': affected_text,
        'symptom_text': symptom_text
    }
    return obj