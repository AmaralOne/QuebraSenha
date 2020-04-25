# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:24:40 2019

@author: FlavioFilho
"""

import hashlib
import requests
import json
from uuid import getnode as get_mac
from random import randint

mac = get_mac()

rand = randint(0,10000)

client = str(mac)+'-'+str(rand)
print(client)
data = {  "id_cliente":client }

url = "http://127.0.0.1:8090/"
url2 = "http://127.0.0.1:8090/result"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

while(True):
    achou = 0
    senha = ''
    r = requests.post(url, data=json.dumps(data), headers=headers)
    #print(r.json())
    aux = r.json()
    senhaEscolhida = aux['senha_hash']
    list_palavras = aux['listas_de_senhas']
    id_lista = aux['id_lista']
    print("id_lista: ",id_lista)
    if senhaEscolhida == '0':
        print("já quebrou a senha")
        break;
    print("testar lista")
    for p in list_palavras:
        if hashlib.md5(p.encode()).hexdigest() == senhaEscolhida:
            print("A senha é ",p)
            achou  = 1
            senha = p
            break
    print("já testou")
    resp = {  "id_cliente": client,"resultado": achou, "senha": senha }
    r = requests.post(url2, data=json.dumps(resp), headers=headers)
    
    
    

