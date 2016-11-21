# coding=gbk
import requests
payload = {"class":"Koubei","action":"getKoubeiList","package":"ums","params":{"params":{"supplier_id":3054,"page":1,"limit":20,"status":2}}}
r = requests.post("http://groupservice.miyabaobei.com/", params=payload)
print(r.text)
