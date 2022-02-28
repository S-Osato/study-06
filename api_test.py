from api import get_api, get_ranking_list,search_item,search_price,write_ranking
from json_test import json_ranking
import pprint
import pandas as pd

def test_get_api():
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
    params = {
        "format": "json",
        "keyword": "PS5",
        "applicationId": "1019079537947262807",
        "minPrice": 111
    }
    res = get_api(url=url,params=params)
    
    # チェック
    # 正常系　→　うまくいった時の処理
    assert len(res["Items"]) >= 1
    assert res["Items"][0]["Item"]["itemCode"]
    
    # 異常系　→　失敗時の処理
    params = {
        "format": "json",
        "keyword": "PS5ああああああ",
        "applicationId": "1019079537947262807",
        "minPrice": 111
    }
    res = get_api(url=url,params=params)
    
    assert len(res["Items"]) == 0

def test_get_ranking_list():
    
    res = get_ranking_list(json=json_ranking)
        
    # チェック
    # 正常系　→　うまくいった時の処理
    assert len(res) >= 1
    assert res.iloc[0,0]
    assert res.iloc[0,1]
    
    # 異常系　→　失敗時の処理
    res = get_ranking_list(json={})
    assert len(res) == 0
    
def test_write_ranking():
    genruId = "506536" #炭酸飲料
    csv_path = "test_result/ranking1.csv"
    write_ranking(genreId=genruId, csv_path=csv_path)
    
    # チェック
    # 正常系　→　うまくいった時の処理
    res = pd.read_csv(csv_path, header=0)
    assert len(res) >= 1
    assert res.iloc[0,0]
    assert res.iloc[0,1]
    
    genruId = "1111" #架空
    csv_path = "test_result/ranking2.csv"
    write_ranking(genreId=genruId, csv_path=csv_path)
    
     # 異常系　→　失敗時の処理
    res = pd.read_csv(csv_path, header=0)
    assert len(res) == 0
    
def test_search_item():
    keyword = "鬼滅"
    
    res = search_item(keyword=keyword)
    
    # チェック
    # 正常系　→　うまくいった時の処理
    assert len(res) >= 1
    
    res = search_item(keyword="")
    # 異常系　→　失敗時の処理
    assert res == None
    
def test_search_price():
    keyword = "鬼滅"
    
    res = search_price(keyword=keyword)
    
    # チェック
    # 正常系　→　うまくいった時の処理
    assert len(res) >= 1
    
    res = search_price(keyword="")
    # 異常系　→　失敗時の処理
    assert res == None