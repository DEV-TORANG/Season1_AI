from urllib.parse import urlencode, unquote, quote_plus
from urllib.request import urlopen
import urllib
import requests
import json
import pandas as pd
from datetime import datetime

def API_measurement():
    now = datetime.now()
    base_date = now.strftime('%Y%m%d')
    today = now.strftime('%Y-%m-%d')
    print(" 오늘은 " + today + " 입니다 ")
    print()

    if now.hour<2 or (now.hour==2 and now.minute<=10): 
        base_time="2300"
    elif now.hour<5 or (now.hour==5 and now.minute<=10): 
        base_time="0200"
    elif now.hour<8 or (now.hour==8 and now.minute<=10): 
        base_time="0500"
    elif now.hour<11 or (now.hour==11 and now.minute<=10):
        base_time="0800"
    elif now.hour<14 or (now.hour==14 and now.minute<=10): 
        base_time="1100"
    elif now.hour<17 or (now.hour==17 and now.minute<=10): 
        base_time="1400"
    elif now.hour<20 or (now.hour==20 and now.minute<=10): 
        base_time="1700" 
    elif now.hour<23 or (now.hour==23 and now.minute<=10): 
        base_time="2000"
    else: 
        base_time="2300"

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    queryString = "?" + urlencode(
    {
      "ServiceKey": unquote("G5Up%2FGmSMFR5uj6NniGCyu%2Bj6wzI9cxI6m0ZeW2IKVX7Wb%2FZjf6CK%2BWw0lE354uBayP%2B3v5WZOuTYbVEj9Jwhw%3D%3D"),
      "base_date": base_date,
      "base_time": base_time,
      "nx": 87, 
      "ny": 90,
      "numOfRows": "10",
      "pageNo": 1,
      "dataType": "JSON"
    }
    )
    queryURL = url + queryString
    response = requests.get(queryURL)
    '''
    print("=== response json data start ===")
    print(response.text)
    print("=== response json data end ===")
    print()
    '''
    
    r_dict = json.loads(response.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_items = r_body.get("items")
    r_item = r_items.get("item")

    result = {}
    for item in r_item:
            if(item.get("category") == "T1H"):
                    result = item
                    break
    for item in r_item:
            if(item.get("category") == "REH"):
                    result2 = item
                    break
    '''
    print("=== response dictionary(python object) data start ===")
    print(result.get("baseTime") + " 시의 " + " 온도는 " + result.get("obsrValue") + "C" + " 입니다 ")
    print(result2.get("baseTime") + " 시의 " + " 습도는 " + result2.get("obsrValue") + "%" + " 입니다 ")
    print("=== response dictionary(python object) data end ===")
    print()
    '''
    OutTemp = result.get("obsrValue")
    OutHumi = result2.get("obsrValue")

    return OutTemp, OutHumi