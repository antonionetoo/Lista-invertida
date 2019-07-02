import sys
import os

def excluir_arquivos(caminho):
    arquivos = os.listdir(caminho)
    for arquivo in arquivos:
        os.remove(caminho + arquivo)


def criar_arquivos (linhas, caminho, numero_repeticoes):
    for i, l in enumerate(linhas.split('.')):
        for j in range(1, numero_repeticoes + 1):
            if (l):
                arq = open(caminho+ str(i * j) + '.txt', 'w')
                arq.writelines(l.replace('\n', ''))
                arq.close()
                

def segmenta(caminho, arquivo, numero_repeticoes = 1):
    arq = open(arquivo) 
    linhas = arq.read()
    arq.close()

    if (os.path.isfile('vocabulario.json')):
        excluir_arquivos(caminho)
        os.remove('vocabulario.json')
    criar_arquivos(linhas, caminho, numero_repeticoes)