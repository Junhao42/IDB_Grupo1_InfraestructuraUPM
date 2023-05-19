import requests
from pandas import json_normalize
import pandas as pd
import json

path = r'./dois.txt'

papers = pd.DataFrame(columns=['paper_id', 'title', 'publication_date'])
autores = []
textos = pd.DataFrame(columns=['title', 'abstract'])
js = []
docs = pd.DataFrame(columns=["paper", "author", "paperId"])
abstracts = []


with open(path, mode='r') as dois:
    for linea in dois:
        linea = linea.rstrip('\n')
        r = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/{linea}?fields=title,publicationDate,year,authors,abstract", auth=('user', 'pass'))
        
        if r:
            print('Descargado!:', linea)
            papers.loc[linea] = [r.json()['paperId'], r.json()['title'], r.json()['year']]
            
            textos.loc[linea] = [r.json()['title'], r.json()['abstract']]

            autores.append(json_normalize(r.json()['authors'])['name'].tolist())

            abstracts.append(r.json()['abstract'])

            js.append(r.json()) # Creamos un fichero .json para usarlo en las consultas simples con elastic search

            docs.loc[linea] = [r.json()['title'], json_normalize(r.json()['authors'])['name'].tolist(), r.json()['paperId']]

            with open ("/mnt/shared-data/elastic-"+str(r.json()['paperId'])+".json", "w") as archivo:
                json.dump(r.json(), archivo, indent=4)

        else:
            print('No se ha encontrado el pdf con DOI', linea)

    lista_aplanada = sum(autores, start=[])
    authors = pd.DataFrame(pd.DataFrame(lista_aplanada).value_counts()).reset_index().rename({0:'author','count':'publications'}, axis='columns')

    textos = textos.reset_index().drop(columns=['index'])

    abs = pd.DataFrame(abstracts)

    docs = docs.explode('author').reset_index().drop(columns=['index'])
    docs.index.name='Id'

with open("/mnt/shared-data/metadatos.json", "w") as fichero:
    for i in js:
        json.dump(i, fichero)
        fichero.write('\n')
    
papers.to_csv(r'/mnt/shared-data/documents.csv')
authors.to_csv(r'/mnt/shared-data/authors.csv')
docs.to_csv(r'/mnt/shared-data/docs.csv')
textos.to_csv(r'/mnt/shared-data/parrafos.csv')
abs.to_csv(r'/mnt/shared-data/abstracts.csv', index=False, header=False)