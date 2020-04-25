# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 08:07:00 2019

@author: FlavioFilho
"""
import hashlib
from datetime import datetime


class ModelTask(object):
    def __init__(self,senha_hash,lista_de_senha,id_lista):
        self.senha_hash = senha_hash
        self.lista_de_senha = lista_de_senha
        self.id_lista = id_lista
        
    def json(self):
            
        return{"senha_hash":self.senha_hash,
                    "listas_de_senhas":self.lista_de_senha,
                        "id_lista":self.id_lista
                    }
        
class Task(object):
    def __init__(self,id_lista):
        self.id_lista = id_lista
        self.id_cliente = ''
        self.time_envio = ''
        self.time_resposta = ''
        self.resultado = False
        
    
    def enviarLista(self,id_cliente):
        self.id_cliente = id_cliente
        self.time_envio = datetime.now()
        
    def repostLista(self,resultado):
        self.time_resposta = datetime.now()
        self.resultado = resultado
        

        
        

def obter_n_linhas (nomeDoArquivo):
    arquivo = open(nomeDoArquivo, errors='ignore')
    n_linhas = sum(1 for linha in arquivo)
    arquivo.close()
    return n_linhas   

    
        
class Gerenciador_de_Requisicao(object):
    def __init__(self):
        
        self.list_palavras = []
        self.fila_de_requisicao = []
        self.tamanho_da_página = 100000
        self.lista_de_blocos_de_senha = []
        self.quantidade_de_senhas = 0
        self.quantidades_de_bloco = 0
        self.achouSenha = False
        self.senhaQuebrada = ''
        
        self.lerArquivosSenhas()
        
        self.iniciar_lista_de_blocos_de_senha()

        self.senhaEscolhida = hashlib.md5(self.list_palavras[self.quantidade_de_senhas-100].encode()).hexdigest()
        #self.senhaEscolhida = hashlib.md5(self.list_palavras[500000].encode()).hexdigest()
        
    def lerArquivosSenhas(self): 
        file = open('rockyou.txt', errors='ignore')
        texto = file.read()
        
        n = obter_n_linhas('rockyou.txt')
        
        self.quantidade_de_senhas = n
        
        x = 0
        
        for i in range(0,n):
            palavra = ''
            while(texto[x] != '\n'):
                palavra = palavra + texto[x]
                x = x + 1
                
            if texto[x] == '\n':
                x = x + 1
            
            #print(palavra)
            self.list_palavras.append(palavra)
            
    def iniciar_lista_de_blocos_de_senha(self):
        self.quantidades_de_bloco = int(self.quantidade_de_senhas/self.tamanho_da_página)
        if self.quantidade_de_senhas % self.tamanho_da_página > 0 :
            self.quantidades_de_bloco =  self.quantidades_de_bloco + 1
        for b in range(self.quantidades_de_bloco):
            self.lista_de_blocos_de_senha.append(Task(b))
            
    def Task_não_executada(self):
        for b in range(self.quantidades_de_bloco):
            if (self.lista_de_blocos_de_senha[b].time_envio == ''):
                break
            
        return b
            
        
    def pegaTask(self,id_cliente):
        if self.achouSenha == False:
            if len(self.fila_de_requisicao) == 0:
                task = self.Task_não_executada()
                print("task:: ",task)
                self.lista_de_blocos_de_senha[task].enviarLista(id_cliente)
                self.fila_de_requisicao.append(self.lista_de_blocos_de_senha[task])
                lista_das_senhas = self.list_palavras[(task*self.tamanho_da_página):((task+1)*self.tamanho_da_página)]
                result = ModelTask(self.senhaEscolhida,lista_das_senhas,task)
                
                return result.json()
            for r in self.fila_de_requisicao:
                 
                 y = datetime.now()             
                 timeDifference = y - r.time_envio
                 time_difference_in_minutes = (int(timeDifference.days) * 24 * 60) + int((timeDifference.seconds) / 60)
                 
                 if time_difference_in_minutes > 2 :
                     task = r.id_lista
                     self.fila_de_requisicao.remove(r)
                     self.lista_de_blocos_de_senha[task].enviarLista(id_cliente)
                     self.fila_de_requisicao.append(self.lista_de_blocos_de_senha[task])
                     lista_das_senhas = self.list_palavras[(task*self.tamanho_da_página):((task+1)*self.tamanho_da_página)]
                     result = ModelTask(self.senhaEscolhida,lista_das_senhas,task)
                     return result.json()
                 task = self.Task_não_executada()
                 self.lista_de_blocos_de_senha[task].enviarLista(id_cliente)
                 self.fila_de_requisicao.append(self.lista_de_blocos_de_senha[task])
                 lista_das_senhas = self.list_palavras[(task*self.tamanho_da_página):((task+1)*self.tamanho_da_página)]
                 result = ModelTask(self.senhaEscolhida,lista_das_senhas,task)
                
                 return result.json()
        else:
            listaux = []
            result = ModelTask('0',listaux,0)
            return result.json()
        
    def repostaTask(self,id_cliente,resultado,senha):
        for r in self.fila_de_requisicao:
            if r.id_cliente == id_cliente:
                task = r.id_lista
                self.lista_de_blocos_de_senha[task].repostLista(resultado)
                self.fila_de_requisicao.remove(r)
                break
            
        print(resultado)
        if resultado == True:
            self.achouSenha = True
            self.senhaQuebrada = senha
            print("************************")
            print("A senha quebrada é ",senha)
            print("************************")
        
    def imprime_fila_de_requisicao(self):
        for r in self.fila_de_requisicao:
            print('id_lista: ',r.id_lista,'id_cliente: ',r.id_cliente,'horario_envio: ',r.time_envio)

             
        
        
        