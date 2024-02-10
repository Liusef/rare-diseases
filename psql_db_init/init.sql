create extension if not exists vector;

create table if not exists keyword (
    id serial primary key,
    name varchar unique not null
);

create index idx_keyword_name on keyword (name);

create table if not exists disease (
    id serial primary key,
    name varchar unique not null,
    url varchar not null,
    affected_text text,
    symptom_text text
);

create index idx_disease_name on disease (name);

create table if not exists disease_keyword (
    disease_id integer references disease(id) on delete cascade,
    keyword_id integer references keyword(id) on delete cascade,
    primary key (disease_id, keyword_id)
);

create table if not exists disease_embeddings (
    id serial primary key,
    disease_id integer references disease(id) on delete cascade,
    embedding vector(768) not null
);