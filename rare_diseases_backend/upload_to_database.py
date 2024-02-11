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


print('Deleting bad keys >:(')
keys_to_delete = ["s", "pt", "i", "p", "t", "o", "0.07 in", "~0.5%", "0.6 in", "<1%", "1", "1%", "<10%", "100%", "10/11", "10-20 times greater than normal", "102 f", "102 to 104 degrees f", "104-105 degrees fahrenheit", "104of", "10/54", "10/72", "10% of patients", "10 percent of individuals with mctd", "10q", "11/68", "116 cm", "11 out of 24", "11 pairs instead of 12", "11years – adulthood", "1/200,000", "120 centimeters", "120 cm", "1-23 months", "1250 g", "12.6% to 33%", "1–2 years of age", "13,14,15,21,or 22", "13 – 15 years", "13.5%", "1-3 millimeters", "15/48", "15q", "15 years and greater", "16%", "16/50", "17%", "18%", "18p", "19%", "19.2%", "19/74", "1 family", "<1 percent of all cjd; less than 500 cases ever known", "2", "2%", ">20", "20%", "2001", "200-250 mmh2o or 20-25 cmh2o is considered borderline high", "20-30%", "20-80%", "21%", "2-11 years", "21/73", "22/72", "23/59", "235 inches", "2-3 syndactyly", "24 cases each", "24-hours per day", "25%", "<2500 grams", "25 cases", "26%", "27%", "28/73", "~29%", "29%", "29/45", "2 to 3 years behind the chronological age", "2 to < 6 years", "~3%", "3", "30%", "30.4%", "30-40% of patients [3,6]", "30% of cases", "30 percent of gcse", "30’s and 40’s", "31%", "32.6%", "32/64", "33%", "33/48", "34/73", "3,4-dap", "35-50%", "~35-50 years", "36%", "37/74", "38%", "38/68", "39oc", ">3 ml", "3 months to < 2 years", "4", "4%", "~40%", "40%", "400 or more rads", "40/73", "~40% of cases; most will have a neuroblastoma but less commonly ganglioneuroma or ganglioneuroblastoma", "40% of patients", "42%", "43%", "44%", "4/48", "44%, strokes", "46%", "46/63", "46, xy", "47%", "47%, transient ischemic attacks", "48/69", "48/70", "49%", "4h syndrome", "<5%", "5", "5%", "<50", "50%", "50/80", "50% of patients", "50% of them being bilateral pheo", "52%", "5-29%", "52.9%", "53%", "5:30-6:30am", "54/74", "54/88", "~55%", "55/77", "56%", "58%", "59.3%", "5% of those affected", "6", "6%", "60%", "60/74", "60.9%", "60 inches", "60% of patients", "60 to 80%", "61%", "6/24", "63.5%", "64%", "6/48", "67%", "68%", "6 ft. 2 in.", "6 ft. 4 in. to 6 ft. 8 in.", "6th cranial nerve", "6 to < 15 years", "7", "70% of patients", "70 percent of cases", "70 percent of gcse", "70% will have minimal words by 24 months of age", "7-17 days", "71/88", "78%", "78/90", "7th cranial nerve", "8", "8%", ">80%", "~80%", "80%", "80-90%", "80-99%", "80% hip, 80% knee, and 65% elbow", "~80 inches", "80% of cases", "81%", "82%", "83%", "84-128cm", "85%", "85% of cases", "86%", "8.7%", "87%", "88%", "9", "9%", "~90%", "90%", "90% of cases", "92%", "93%", "94%", "9/54", "95% of those affected", "9/62", "97%", "98%", "9p", "a", "aac",]
keys_to_delete += ["about 2/3 of patients", "about 25%% of cases", "about 30cm or 12 inches", "about 35%% of cases", "about 40%% of cases", "about 50%% of children with similar symptoms do not have a tumor", "about 5-7 percent", "about 70% of cases", "about 8%", ]
keys_to_delete += ["wasserstein et al, jimd, 2013", "spinal-onset als", "bulbar-onset als", "lund, et al 2019", "berends et al, 2001", "berends et al, 2001, rosias et al, 2001", "cruz d et al., 2001", "berry et al. 2013", "sokol & loughran, 2006; zhang et al. 2010", "shah et al, 2016", "rivero et al. 2021", "tetti et al. 2018", "cui et al. 2017", "yang et al, 2022", "ramos et al., 2018", "nicolas et al., 2015", "anselm et al. 2016; matricardi et al. 2020; yang et al. 2020", "abramov et al, 2020, stamberger et al, 2016", "stamberger et al, 2016", "reports ranging from 16-31%; stamberger et al, 2016", "pennington et al., 1980; bender et al., 1993", "skraban et al, 2017", ]
keys_to_delete += ["""for a description of sebaceous nevus see schimmelpenning syndrome above.""", """for a total of four""", """for example eating only ice cream""", """for example, by ct or mri""", """for example, one patient had a congenital heart abnormality and another was born with abnormal kidneys""", """for example, the rise in parathyroid hormone will allow the body to maintain a normal serum calcium level""", """for example, the rotavirus or chickenpox""", """for example, with eating, bathing, and ambulation""", """for example: low voltage""", """for further information on cornelia de lange syndrome, please see the "related disorders" section of this report below.""", """for further information on hodgkin’s disease, please see the "related disorders" section below.""", """for further information on kfs, please see the "related disorders" section of this report below.""", """for further information on subtypes, disease staging, treatment options, etc., please see the "classification," "staging," and "standard therapies" section of this report below.""", """for further information on these chromosomal disorders, please see the "causes" and "related disorders" sections of this report below.""", """for further information on this condition, please choose "holoprosencephaly" as your search term in the rare disease database.""", """for further information on this disorder, please see the "related disorders" section of this report below.""", """for further information, please choose "hashimoto*" as your search term in the rare disease database.""", """for further information, please see standard therapies below.""", """for further information, please see the "causes" section of this report below.""", """for further information, please see the "standard therapies" section of this report below.""", """for further information, please see the "standard therapies: diagnosis" section of this report below.""", """for further information, please use "holoprosencephaly" as your search term in the rare disease database.""", """for information on these diseases, see the related disorders section of this report.""", """for information on this condition, choose "tethered spinal cord" as your search term in the rare disease database.""", """for information on treatment, see the standard therapies section below.""", """for instance, face droop if the facial nerve is affected""", """for more information  on spina bifida occulta, choose "spina bifida" as your search term in the  rare disease database.""", """for more information about "hypoparathyroidism," please see the related disorders section of this report.""", """for more information choose "gillespie" as your search term in the rare disease database.""", """for more information choose "pierre-robin" as your search term in the rare disease database""", """for more information choose "wilms" as your search term in the rare disease database.""", """for more information on a disorder involving telangiectasias choose "hemorrhagic telangiectasia, hereditary" for your search term in the rare disease database.""", """for more information on aep, see the related disorders section below""", """for more information on agenesis of corpus callosum, see the related disorders section of this report.""", """for more information on apnea, choose "sleep apnea" as your search term in the rare disease database.""", """for more information on blepharospasm, please see the related disorders section below.""", """for more information on central diabetes insipidus, choose "central diabetes insipidus" as your search term in the rare disease database.""", """for more information on depression, see the related disorders section of this report.""", """for more information on dysautonomia, see the related disorders section below""", """for more information on familial adenomatous polyposis, see the related disorders section of this report.""", """for more information on gbs, see the related disorders section of this report.""", """for more information on hydrocephalus, choose "hydrocephalus" as your search term in the rare disease database""", """for more information on hypopituitarism, see the related disorders section of this report.""", """for more information on hypothyroidism, hypoglycemia and diabetes insipidus, please see the related disorders section of this report.""", """for more information on klippel-feil syndrome and sprengel deformity, please see the related disorders section of this report.""", """for more information on legg-calve-perthes disease, see the related disorders section of this report.""", """for more information on lennox-gastaut syndrome, see the related disorders section below.""", """for more information on lowe syndrome, see the related disorders section of this report""", """for more information on lyme disease, choose "lyme" as your search term in the rare disease database.""", """for more information on lyme disease, please see the "related disorders" section of this report below.""", """for more information on megaloblastic anemia, see the related disorders section of this report.""", """for more information on noonan and cardiofaciocutaneous syndromes, see the related disorders section below.""", """for more information on sprengel deformity, see the related disorders section of this report.""", """for more information on tetralogy of fallot, see the related disorders section of this report.""", """for more information on these conditions, choose "cleft palate and cleft lip" as your search terms in the rare disease database.""", """for more information on these conditions, choose the name of the disease as your search term in the rare disease database.""", """for more information on these conditions, see the related disorders section of this report.""", """for more information on these disorders, choose "aniridia" and "cataracts" as your search terms in the rare disease database.""", """for more information on these disorders, choose "epilepsy" and/or "diabetes" as your search terms in the rare disease database""", """for more information on these disorders, choose "hydrocephalus" and  "cleft palate" as your search terms in the rare disease database.""", """for more information on these disorders, choose "itp" and "anemia, hemolytic, acquired autoimmune" as your search terms in the rare disease database.""", """for more information on these disorders, choose "neuropathy, peripheral" as your search term in the rare disease database.""", """for more information on these disorders, choose exact disorder name as your search term in the rare disease database.""", """for more information on these disorders, choose the disorder name as your search term in the rare disease database.""", """for more information on these disorders, choose the specific disorder name as your search term in the rare disease database.""", """for more information on these disorders, see the related disorders section below.""", """for more information on these disorders, see the related disorders section of this report.""", """for more information on these heart defects, choose the specific name as your search term in the rare disease database.""", """for more information on these heart defects, see the related disorders section of this report.""", """for more information on these seizure types, use "epilepsy" as your search terms in the rare disease database.""", """for more information on these types of seizures choose "epilepsy" as your search term in the rare disease database""", """for more information on this condition, choose "holoprosencephaly" as your search term in the rare disease database.""", """for more information on this condition, choose "idiopathic intracranial hypertension" as your search term in the rare disease database.""", """for more information on this condition, choose "infantile apnea" as your search term in the rare disease database.""", """for more information on this condition, please choose "spina bifida" as your search term in the rare disease database.""", """for more information on this condition, please see the "related disorders" section of this report below.""", """for more information on this condition, please see the related disorders section of this report.""", """for more information on this condition, search for "dwm’ in the rare disease database.""", """for more information on this condition, use "horner" as your search term in the rare disease database.""", """for more information on this disorder choose "arteriovenous" for your search term in the rare disease database.""", """for more information on this disorder choose "cavernous hemangioma" for your search term in the rare disease database.""", """for more information on this disorder choose "polycystic kidney disease" as your search term in the rare disease database""", """for more information on this disorder choose "spina bifida" as your search term in the rare disease database.""", """for more information on this disorder choose "tetralogy of fallot" as your search term in the rare disease database""", """for more information on this disorder, choose "acromegaly" as your search term in the rare disease database.""", """for more information on this disorder, choose "acth deficiency" as your search term in the rare disease database""", """for more information on this disorder, choose "acute myeloid leukemia" as your search term in the rare disease database.""", """for more information on this disorder, choose "adult respiratory distress" as your search term in the rare disease database.""", """for more information on this disorder, choose "aicardi" as your search term in the rare disease database""", """for more information on this disorder, choose "carnitine" as your search words in the rare disease database""", """for more information on this disorder, choose "cloves syndrome" as your search term in the rare disease database""", """for more information on this disorder, choose "cushing" as your search term in the rare disease database.""", """for more information on this disorder, choose "cytomegalovirus" as your search term in the rare disease database.""", """for more information on this disorder, choose "dandy-walker" as your search term in the rare disease database.""", """for more information on this disorder, choose "dermatomyositis" as your search term in the rare disease database.""", """for more information on this disorder, choose "eisenmenger" as your search term in the rare disease database.""", """for more information on this disorder, choose "endocarditis" as your search term in the rare disease database.""", """for more information on this disorder, choose "froelich’s syndrome" as your search term in the rare disease database""", """for more information on this disorder, choose "frontotemporal degeneration" as your search term in the rare disease database""", """for more information on this disorder, choose "glioma" as your search term in the rare disease database""", """for more information on this disorder, choose "growth hormone deficiency" as your search term in the rare disease database""", """for more information on this disorder, choose "hemimegalencephaly" as your search term in the rare disease database""", """for more information on this disorder, choose "hereditary olivopontocerebellar atrophy" as your search term in the rare disease database.""", """for more information on this disorder, choose "hirschsprung" as your search term in the rare disease database.""", """for more information on this disorder, choose "hlh" as your search term in the rare disease database""", """for more information on this disorder, choose "hydrocephalus" as your search term in the rare disease database""", """for more information on this disorder, choose "insipidus" as your search term in the rare disease database""", """for more information on this disorder, choose "klippel-trenaunay" as your search term in the rare disease database""", """for more information on this disorder, choose "limb-girdle muscular dystrophy" as your search term in the rare disease database.""", """for more information on this disorder, choose "medulloblastoma" as your search term in the rare disease database.""", """for more information on this disorder, choose "megalencephaly-capillary malformation" as your search term in the rare disease database""", """for more information on this disorder, choose "megaloblastic anemia" as your search term in the rare disease database.""", """for more information on this disorder, choose "meningitis" as your search term in the rare disease database""", """for more information on this disorder, choose "miyoshi" as your search term in the rare disease database.""", """for more information on this disorder, choose "moyamoya" as your search term in the rare disease database""", """for more information on this disorder, choose "myelodysplastic syndromes" as your search term in the rare disease database.""", """for more information on this disorder, choose "myoclonus" as your search term in the rare disease database.""", """for more information on this disorder, choose "n24" as your search term in the rare disease database""", """for more information on this disorder, choose "neonatal herpes" as your search term in the rare disease database.""", """for more information on this disorder, choose "neutropenia" as your search term in the rare disease database.""", """for more information on this disorder, choose "poems" as your search term in the rare disease database.""", """for more information on this disorder, choose "precocious puberty" as your search term in the rare disease database""", """for more information on this disorder, choose "precocious puberty" as your search term in the rare disease database.""", """for more information on this disorder, choose "respiratory distress" as your search term in the rare disease database.""", """for more information on this disorder, choose "rubella" as your search term in the rare disease database.""", """for more information on this disorder, choose "split hand" as your search term in the rare disease database.""", """for more information on this disorder, choose "sspe" as your search term in the rare disease database.""", """for more information on this disorder, choose "tinnitus" as your search term in the rare disease database.""", """for more information on this disorder, choose "toxoplasmosis" as your search term in the rare disease database.""", """for more information on this disorder, choose "uterine leiomyosarcoma" as your search term in the rare disease database.""", """for more information on this disorder, choose "vasculitis" as your search term in the rare disease database.""", """for more information on this disorder, choose "ventricular septal defect" as your search term in the rare disease database.""", """for more information on this disorder, choose "wilms’ tumor" as your search term in the rare disease database.""", """for more information on this disorder, choose "zollinger ellison" as your search term in the rare disease database.""", """for more information on this disorder, see the related disorders section below.""", """for more information on this disorder, see the related disorders section of this report.""", """for more information on this, choose "lissencephaly" as your search term in the rare disease database.""", """for more information on those conditions, choose the name of the disorder as your search term in the rare disease database.""", """for more information on tinnitus, choose "tinnitus" as your search term in the rare disease database.""", """for more information on trisomy 15q25-qter, see the "causes" section below.""", """for more information on ventricular septal defects see the related disorders section below.""", """for more information, choose "acromegaly" as your search term in the rare disease database.""", """for more information, choose "congenital heart block" as your search term in the rare disease database""", """for more information, choose "cushing’s" as your search term in the rare disease database.""", """for more information, choose "hydrocephalus" as your search term in the rare disease database.""", """for more information, choose "neonatal hemochromatosis" as your search term in the rare disease database.""", """for more information, choose "polymyositis" and "dermatomyositis" as your search terms in the rare disease database.""", """for more information, choose "raynaud" as your search term in the rare disease database""", """for more information, choose "retinitis pigmentosa" as your search term in the rare disease database""", """for more information, choose "tetralogy of fallot" as your search term in the nord rare disease database.""", """for more information, choose the specific disorder name as your search term in the rare disease database.""", """for more information, please choose "epilepsy" as your search term in the rare disease database.""", """for more information, please choose "sprengel" as your search term in the rare disease database.""", """for more information, please choose "vitiligo" as your search term in the rare disease database.""", """for more information, please see the "standard therapies" section below.""", """for more information, search "lymphangioleiomyomatosis" in the rare disease database""", """for more information, search for "central core disease" in the rare disease database.""", """for more information, search for "centronuclear myopathy" in the rare disease database.""", """for more information, search for "cftd" in the rare disease database.""", """for more information, search for "nemaline myopathy" in the rare disease database.""", """for more information, see "ventricular septal defect" in the related disorders section of this report.""", """for more information, see the individual entries for fcmd and wss in nord’s rare disease database.""", """for more information, see the individual nord entry on "collagen type vi-related disorders" in nord’s rare disease database.""", """for more information, see the related disorders section below""", """for more information, see the standard therapies: diagnosis section below.""", """for more on salmonellosis, see below. for further information on malaria, please choose "malaria" as your search term in the rare disease database.""", """for more on west syndrome, please see the related disorders section below.""", """for more, see "causes" below.""", ]
keys_to_delete += ["formerly called matp", "formerly eds vii", "formerly edsi and edsii", "formerly edsiii", "formerly edsiv", "formerly edsvi", "formerly edsvii, a and b", "formerly edsviic", "formerly hallopeau-siemens rdeb", ]

cursor.executemany('delete from keyword k where k.name = %s', [(key,) for key in keys_to_delete])
cursor.execute('delete from keyword k where length(k.name) <= 2',)

connection.commit()