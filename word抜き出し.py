# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V87NfQBkIQRm30-a-uVjKm-MXaqTNJTj
"""

# !pip install requests

import json

import requests as req

header={"Content-Type":"application/json"}


text=input()
param={ "request_id":"record001", "sentence":text,"class_filter":"ART|ORG|PSN|LOC"}

APIKEY="6867436846733131632f4d73646478724e4a566c5679496a325946663957585765716a595a5156526b6236"
url=f'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/entity?APIKEY={APIKEY}'
r=req.post(url,headers=header,data=json.dumps(param))

import pprint
pprint.pprint(r.json())