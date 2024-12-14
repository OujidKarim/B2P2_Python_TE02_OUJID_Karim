# Exercice 1
import pandas as pd
import requests
import json
import csv
import os


# Exercice 2
def get_json(url, limit, page):
    try:
        response = requests.get(url+"/products.json?limit="+str(limit)+"&page="+str(page))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print("Erreur http : " + str(error))
    except requests.exceptions.ConnectionError as error:
        print("Connexion impossible : " + str(error))
    except requests.exceptions.Timeout as error:
        print("Délai dépassé : " + str(error))
    except Exception as error:
        print("Erreur : " + str(error))
    return None

# Exercice 3
def json_to_df(json_data):
    products = json_data.get("products", [])
    if not products:
        return pd.DataFrame()
    return pd.DataFrame(products)

# Exercice 4
def get_products(url):
    all_products = []
    page = 1
    limit = 250
    
    while True:
        print(f"Page {page}")
        json_data = get_json(url, limit, page)
        
        if not json_data or not json_data.get("products"):
            break
            
        df = json_to_df(json_data)
        if df.empty:
            break
            
        all_products.append(df)
        page += 1
    
    if all_products:
        final_df = pd.concat(all_products, ignore_index=True)
        return final_df
    return pd.DataFrame()

# Exercice 5
def get_variants(df_products):
    woo_products = []
    
    for index, product in df_products.iterrows():
        variant = product['variants'][0]
        
        images = ';'.join([img['src'] for img in product['images']]) if product.get('images') else ''
        
        tags = product.get('tags', [])
        if isinstance(tags, str):
            tags = tags.split(', ')
        tags_string = ','.join(tags) if tags else ''
        
        # Création du dictionnaire basé sur l'exemple fourni pour les données
        product_data = {
            'ID': index,
            'Type': 'simple',
            'SKU': variant.get('sku', ''),
            'Name': product['title'],
            'Published': 1,
            'Is featured?': 0,
            'Visibility in catalog': 'visible',
            'Short description': product.get('handle', ''),
            'Description': product['body_html'],
            'Date sale price starts': '',
            'Date sale price ends': '',
            'Tax status': 'taxable',
            'Tax class': '',
            'In stock?': 1,
            'Stock': variant.get('inventory_quantity', 0),
            'Backorders allowed?': 0,
            'Sold individually?': 0,
            'Weight (lbs)': variant.get('weight', ''),
            'Length (in)': '',
            'Width (in)': '',
            'Height (in)': '',
            'Allow customer reviews?': 1,
            'Purchase note': '',
            'Sale price': variant.get('compare_at_price', ''),
            'Regular price': variant.get('price', ''),
            'Categories': product.get('product_type', ''),
            'Tags': tags_string,
            'Shipping class': '',
            # les images sont "retirées" pour que l'importation soit plus rapide. retirer les côtes de 'images' pour importer les images
            'Images':  'images' ,
            'Download limit': '',
            'Download expiry days': '',
            'Parent': '',
            'Grouped products': '',
            'Upsells': '',
            'Cross-sells': '',
            'External URL': '',
            'Button text': '',
            'Position': 0,
            'Meta: _wpcom_is_markdown': '',
            'Download 1 name': '',
            'Download 1 URL': '',
            'Download 2 name': '',
            'Download 2 URL': ''
        }
        woo_products.append(product_data)
    
    return pd.DataFrame(woo_products)

def get_csv(df_variants, filename="csv/products_export.csv"):
    os.makedirs('csv', exist_ok=True)
    df_variants.to_csv(filename, index=False, header=True, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)
    print(f"Fichier CSV généré : {filename}")

# Exercice 6
def get_csv(df_variants, filename="csv/products_export.csv"):
    os.makedirs('csv', exist_ok=True)
    df_variants.to_csv(filename, index=False, header=True, encoding='utf-8')
    print(f"Fichier CSV généré : {filename}")

# Exercice 7
def main():
    print("=== Scrapper Shopify vers WooCommerce ===")
    shopify_url = "https://noyoco.com"
    
    if not shopify_url:
        print("URL invalide")
        return
    
    print("\nRécupération des produits...")
    df_products = get_products(shopify_url)
    
    if df_products.empty:
        print("Aucun produit trouvé")
        return
    
    print(f"\n{len(df_products)} produits trouvés")
    print("\nTraitement des variants...")
    df_variants = get_variants(df_products)
    
    print("\nGénération du CSV...")
    get_csv(df_variants)
    
    print("\nTerminé!")

if __name__ == "__main__":
    main()

