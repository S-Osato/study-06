import warnings
warnings.simplefilter('ignore', FutureWarning)

from operator import ge
import requests
import pandas as pd
import os

APP_ID = "1099878610526244104"

def get_api(url, params: dict):
    result = requests.get(url, params=params)
    return result.json()

def get_ranking_list(json: dict):
    ranking_list = pd.DataFrame(columns=["順位", "商品名"])
    if json.get('Items'):
        for item in json['Items']:
            item_rank = item['Item']['rank']
            item_name = item['Item']['itemName']
            tmp_ranking_list = [{"順位":item_rank, "商品名":item_name}]
            ranking_list = ranking_list.append(tmp_ranking_list)
            print(f"順位:{item_rank} 商品名：{item_name}")
    
    return ranking_list

def write_ranking(genreId, csv_path: str):
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"
    # パラメータを記述
    params = {
        "format": "json",
        "genreId": genreId,
        "applicationId": APP_ID,
    }
    
    ranking_list = get_ranking_list(get_api(url, params=params))
    if "/" in csv_path:
        dir = os.path.dirname(csv_path)
        os.makedirs(dir, exist_ok=True)
    ranking_list.to_csv(csv_path,index=False)

def search_item(keyword):
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
    # パラメータを記述
    params = {
        "format": "json",
        "keyword": keyword,
        "applicationId": APP_ID,
        "minPrice": 111
    }
    
    json = get_api(url, params=params)
    
    if json.get('Items'):
        for item in json['Items']:
            item_name = item['Item']['itemName']
            item_price = item['Item']['itemPrice']
            print(f"商品名:{item_name} 価格：{item_price}")
    else:
        json = None
        
    return json

def search_price(keyword):
    url = "https://app.rakuten.co.jp/services/api/Product/Search/20170426"
    # パラメータを記述
    params = {
        "format": "json",
        "keyword": keyword,
        "applicationId": APP_ID,
    }
    
    json = get_api(url, params=params)
    if json.get('Products'):
        for product in json['Products']:
            product_name = product['Product']['productName']
            product_max_price = product['Product']['salesMaxPrice']
            product_min_price = product['Product']['salesMinPrice']
            print(f"商品名:{product_name} 最高値：{product_max_price} 最安値：{product_min_price}")

    else:
        json = None
    return json

if __name__ == "__main__":
    print("商品検索:1\n価格検索:2\nランキング出力:3")
    command = input("コマンドを入力してください。 >>> ")
    if command == "1":
        keyword=input("キーワードを入力してください。 >>> ")
        search_item(keyword)
        
    elif command == "2":
        keyword=input("キーワードを入力してください。 >>> ")
        search_price(keyword)
        
    elif command == "3":
        genreId=input("ジャンルIDを入力してください。 >>> ")
        write_ranking(genreId, "ranking.csv")
