import hashlib
import time


def obter_n_linhas (nomeDoArquivo):
    arquivo = open(nomeDoArquivo, errors='ignore')
    n_linhas = sum(1 for linha in arquivo)
    arquivo.close()
    return n_linhas



file = open('rockyou.txt', errors='ignore')
texto = file.read()

n = obter_n_linhas('rockyou.txt')

x = 0
list_palavras = []
for i in range(0,n):
    palavra = ''
    while(texto[x] != '\n'):
        palavra = palavra + texto[x]
        x = x + 1
        
    if texto[x] == '\n':
        x = x + 1
    
    #print(palavra)
    list_palavras.append(palavra)
    

senhaEscolhida = hashlib.md5(list_palavras[n-100].encode()).hexdigest()
    
t1 = time.time()
for p in list_palavras:
    if hashlib.md5(p.encode()).hexdigest() == senhaEscolhida:
        print('A senha é ',p)
        break
tempoExec = time.time() - t1
print("Tempo de execução: {} segundos".format(tempoExec))