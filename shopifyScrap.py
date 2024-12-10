# Exo 1

import pandas as pd
import requests
import json as json
import csv as csv

# Exo 2

def get_json(url, limit, page):
    try:
        response = requests.get(url+"/products.json?limit="+str(limit)+"&page="+str(page))
    except requests.exceptions.HTTPError as error:
        print("Erreur http" + error)
    except requests.exceptions.ConnectionError as error:
        print("Connexion impossible" + error)
    except requests.exceptions.Timeout as error:
        print("Délai dépassé" + error)
    except response.raise_for_status() as error:
        print("Erreur" + error)
    return response.json()
    
    
# get_json("https://noyoco.com", 1, 2)

# 
# Exo 3

def json_to_df(json):
    return pd.DataFrame(json)
    

print(json_to_df(get_json("https://noyoco.com", 1, 1)))

# Exo 4

def get_products():
    pages = True
    dictionnary = {}
    while(pages):
        for i in range (1,5):
            dictionnary['col'+str(i)] = str(i)
            json_to_df(get_json("https://noyoco.com", 1, i).get("products", [])).to_csv('test.csv', index=True)
        
        if(i>=4):
            pages = False
            
get_products()
            


