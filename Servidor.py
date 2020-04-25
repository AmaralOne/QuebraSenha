# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 07:37:05 2019

@author: FlavioFilho
"""

from flask import Flask, request
from flask_restplus import Api, Resource, reqparse, inputs, fields
from Regras_quebra_senha import Gerenciador_de_Requisicao
import time


#Classe personaliza de exeception
class ErrorJson(Exception):
   "Error decoding json, check your json."
   pass






#instanciando a Api Flask
flask_app = Flask(__name__)

#Configurando parâmetros do Flask
flask_app.config.setdefault('RESTPLUS_MASK_SWAGGER', False)

#instanciando documentação
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "Quebrador de Senha API", 
		  description = "Quebra Senhas distribuído")



modelTask = app.model('Task', {'senha_hash':fields.String(required = True,description="Senha criptográfada",example='senha'),
                                          'listas_de_senhas': fields.List(fields.String(),required = True, description="Listas de Senhas", example=['Alex','1234','senha','dell','mimimi','rafael','owasp']),
                                          'id_lista':fields.Integer(required = True,description="index da lista",example=1)},)
    
modelPegaTask = app.model('ResqTask', {'id_cliente':fields.String(required = True,description="Id do cliente",example='1213123'),})

modelResultTask = app.model('ResultTask', {'id_cliente':fields.String(required = True,description="Id do cliente",example='1213123'),
                                           'senha':fields.String(description="A senha encontrada",example='123456'),
                                         'resultado':fields.String(required = True,description="Resultado se achou a senha",example=1),
                                         })
    
modelResultTask_retorno = app.model('RetornoResult', {'status':fields.String(required = True,description="Status",example='ok'),})
    
print('abrindo arquivos de senhas')
gr = Gerenciador_de_Requisicao()

    



#Configurando documentação do namespace para as chamdas de métodos
name_space = app.namespace('Methods', description='métodos para clientes ajudarem a quebra senha')

  

#@app.route('/<int:id_cliente>')
@app.route('/')
class MainClass(Resource):   

    #definindo o modelo de retorno do método
    @app.marshal_with(modelTask)
    #definindo os códigos de reposta
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Internal Server Error' })    
    #definindo o modelo de entrada do método
    @app.expect(modelPegaTask)	
    def post(self):

        try:

            #capturando os dados recebidos pelo json
            try:

                id_cliente = request.json['id_cliente']
                result = gr.pegaTask(id_cliente)
                gr.imprime_fila_de_requisicao()
                return result
                #return 'oi'
            except Exception:
                raise ErrorJson("Error decoding demands, check your json.")
                
            except ErrorJson as e:
                print(e.args[0])
                name_space.abort(400, e.args[0], status = "Invalid Argument", statusCode = "400")
            
        except Exception as e:
            print(e.args[0])
            name_space.abort(500, e.args[0], status = "Internal Server Error", statusCode = "500")
            


@app.route('/result')
class MainResult(Resource):   

    #definindo o modelo de retorno do método
    @app.marshal_with(modelResultTask_retorno)
    #definindo os códigos de reposta
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Internal Server Error' })    
    #definindo o modelo de entrada do método
    @app.expect(modelResultTask)	
    def post(self):

        try:
            #capturando os dados recebidos pelo json
            try:
                id_cliente = request.json['id_cliente']
                resultado = request.json['resultado']
                senha = request.json['senha']
                resultado = int(resultado)
                
                r = False
                if resultado == 1:
                    r = True
                    
                print("resultado:",resultado)
                
                
                result = gr.repostaTask(id_cliente,r,senha)

                gr.imprime_fila_de_requisicao()
                return {"status":'ok'}
                #return 'oi'
            except Exception:
                raise ErrorJson("Error decoding demands, check your json.")
                
            except ErrorJson as e:
                print(e.args[0])
                name_space.abort(400, e.args[0], status = "Invalid Argument", statusCode = "400")
            
        except Exception as e:
            print(e.args[0])
            name_space.abort(500, e.args[0], status = "Internal Server Error", statusCode = "500")
            
#Defini a execução da Api
if __name__ == '__main__':
    
    flask_app.run(debug=False,port=8090)
