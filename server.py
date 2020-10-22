import requests
from bs4 import BeautifulSoup
import json
import xmltodict
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

class Uri(BaseModel):
    uri: str


def parse_data(uri:str):
  payload = {}
  headers = {
    'Cookie': '__cfduid=dbdade35f2ca26435e1b04fb37a20c77b1601388967; uid=lo_2676c4ef2585; __cfruid=94c564f54a6364cc766586f4a13965b29547ab9f-1601388968'
  }
  
  response = requests.request("GET", uri, headers=headers, data = payload)
  
  data = xmltodict.parse(response.text.encode('utf8'))

  l = []
  for k in data['rss']['channel']['item']:
    data_dict={}
    try:
      data_dict["id"]=k['guid']['#text'].split("/")[-1]
      data_dict["title"]=k['title']
      data_dict["link"]=k['link']
      data_dict["pub_date"]=k['pubDate']
      data_dict["author"]=k['dc:creator']
      soup = BeautifulSoup(k['description'], 'html.parser')
      for link in soup.find_all('img'):
        data_dict["img"]=link.get('src')
      # print(k['content:encoded'])
    except Exception as e:
      print()
    l.append(data_dict)

  return l

@app.post("/")
def get_data(uri:Uri):
    return parse_data(uri.uri)

@app.get("/health")
def get_health():
  return {"ping":"Its working fast 🚅"}