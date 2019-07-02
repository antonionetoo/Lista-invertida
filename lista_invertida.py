import re
import time 
import sys
import json
import os
import segmenta_arquivos as segmenta

verde = '\033[92m'
branco = '\33[37m'
vermelho = '\033[91m'
azul = '\033[1;34m'

negrito = '\033[1m'
fim = '\033[0m'
        
class Buscador:
    historico = []

    def __init__(self, caminho_documentos):
        self.historico = []
        self.ocorrencias = []
        self.caminho_documentos = caminho_documentos

    def busca(self, valor_busca):
        #TODO refactorinf
        self.valor_busca = valor_busca

        tempo_inicial_processamento = time.time()
        ocorrencias = self.__realiza_busca__(valor_busca)

        h = ('{} {} {:<10} {} {}'.format(azul, negrito, valor_busca, branco, fim), ' {:>10} '.format(round(time.time() - tempo_inicial_processamento, 4)))

        if (ocorrencias is not None and ocorrencias):
            h += ('{:>10}'.format(len(ocorrencias)), )

        self.historico.append(h)
        self.ocorrencias = ocorrencias
    
    def imprimi_ocorrencias(self):

        if (self.ocorrencias is None or len(self.ocorrencias) == 0):
            print('{} Palavra {}\'{}\'{} não encontrada {}'.format(vermelho, negrito, self.valor_busca, fim, branco))
        else:
            print('\n\'{}\' encontrado em:'.format(self.valor_busca))
            
            for o in self.ocorrencias:
                print('Documento: {}, posicoes: {} '.format(o[0], o[1]))
                
                for p in self.linhas_do_arquivo(o[0] + '.txt')[0][1].split():
                    print(' ', end = '')
                    if (p == self.valor_busca):
                        print ('{}{}{}{}{}'.format(negrito, verde, p , fim, branco), end = '')
                    else:
                        print(p, end = '')

                print("\n")

            print("Total de documentos encontrados: {}".format(len(self.ocorrencias)))

    
    def __realiza_busca__(self, valor_busca):
        raise NotImplementedError()

    def linhas_do_arquivo(self, nome_arquivos = None):

        arquivos = []
        if (nome_arquivos is None):
            arquivos = os.listdir(self.caminho_documentos)
        else:
            arquivos.append(nome_arquivos)

        documentos = []
        for a in arquivos:
            numero_documento = a.split('.')[0]

            with open(self.caminho_documentos + a) as arquivo:
                for linha in arquivo:
                    documentos.append((numero_documento, linha))
        
        return documentos
    
    def imprimi_historico(self):
        print('{:<10} {:>10} {:>10}'.format('Busca por', 'Tempo de busca', 'Ocorrências'))
        for h in self.historico:
            
            for i in range (len(h)):
                print(h[i], end = '')
            print()
        
        print()

class BuscadorArquivoInvertido(Buscador):
    
    def __init__(self, caminho_documentos):
        super().__init__(caminho_documentos)
        self.vocabulario = dict()

    def __realiza_busca__(self, valor_busca):
        self.carrega_vocabulario()
        try:
            o = self.vocabulario[valor_busca]
            return o
        except KeyError:
            return None

    
    def carrega_vocabulario(self):

        if (os.path.isfile('vocabulario.json')):

            with open('vocabulario.json', 'r') as f:
                self.vocabulario = json.load(f)
            return

        for documento in self.linhas_do_arquivo():
         
            numero_documento = documento[0]
            linha = documento[1]

            for i, palavra in enumerate(linha.split()):
                if (palavra in self.vocabulario):

                    for o in self.vocabulario[palavra]:
                        if (o[0] == numero_documento):    
                            o[1].append(i + 1)
                            break
                    else:
                        self.vocabulario[palavra].append((numero_documento,  [i + 1]))
                    
                else:
                    self.vocabulario[palavra] = [(numero_documento,  [i + 1])]
                    
        self.salva_vocabulario()
    
    def salva_vocabulario(self, caminho = 'vocabulario.json'):
        f = json.dumps(self.vocabulario)

        with open(caminho, 'w') as arq:
            arq.writelines(f)
    
    def imprimi_historico(self):
        print('Histórico de busca lista invertida')
        super().imprimi_historico()

    def imprimi_ocorrencias(self):
        print('Ocorrências arquivo invertido')
        super().imprimi_ocorrencias()


class BuscadorSequencial(Buscador):

    def __init__(self, caminho_documentos):
        super().__init__(caminho_documentos)
    
    def __realiza_busca__(self, valor_busca):
        ocorrencias = []
        for documento in self.linhas_do_arquivo():
            numero_documento = documento[0]
            linha = documento[1]

            for i, letra in enumerate(linha.split()):
                if (letra == valor_busca):
                    for o in ocorrencias:
                        if (o[0] == numero_documento):
                            o[1].append(i)
                            break
                    else:
                        ocorrencias.append((numero_documento,  [i]))
        
        return ocorrencias

    def imprimi_historico(self):
        print('\n\nHistórico de busca sequencial')
        super().imprimi_historico()
    
    def imprimi_ocorrencias(self):
        print('\n\nOcorrências sequencial')
        super().imprimi_ocorrencias()


caminho_documentos = 'documentos/'
buscador_sequencial = BuscadorSequencial(caminho_documentos)
buscador_arquivo_invertido = BuscadorArquivoInvertido(caminho_documentos)

def ocorrencia(o):
    return o[1]

def maiores_ocorrencias_palavras(n):
    print(n)
    maiores_ocorrencias = []

    print('{0} Maiores ocorrências de palavras {0}'.format('*'*20))

    for chave, valor in buscador_arquivo_invertido.vocabulario.items():
        i = 0
        for v in valor:
            i += len(v[1])
            
        maiores_ocorrencias.append((chave, i))

    maiores_ocorrencias = sorted(maiores_ocorrencias, key = ocorrencia, reverse = True)
    
    for i in range(0, n):
        try:
            print (maiores_ocorrencias[i])
        except IndexError:
            break

    print('\n')

def pesquisa():

    while True:
        try:
            l = input()
            if (not l):
                break
        except EOFError:
            break

        buscador_sequencial.busca(l)
        buscador_arquivo_invertido.busca(l)

def exibi_historicos():
    print('{0} Histórico de buscas {0}'.format('*'*20))

    buscador_sequencial.imprimi_historico()
    buscador_arquivo_invertido.imprimi_historico()

    print('\n')

def exibi_ocorrencias():
    buscador_sequencial.imprimi_ocorrencias()
    buscador_arquivo_invertido.imprimi_ocorrencias()

for i, s in enumerate(sys.argv):
    try:
        if (s == '-p'):
            pesquisa()
        elif (s == '-o'):
            maiores_ocorrencias_palavras(int(sys.argv[int(i) + 1]))
        elif (s == '-h'):
            exibi_historicos()
        elif (s == '-s'):
            segmenta.segmenta(caminho_documentos, sys.argv[int(i) + 1], int(sys.argv[int(i) + 2]))
        elif (s == '-e'):
            exibi_ocorrencias()

    except IndexError:
        print('Número de parâmetros incorreto')



#print('Documento diferentes:')
#for o in buscador_sequencial.ocorrencias:
#    if (o not in buscador_arquivo_invertido.ocorrencias):
#        print (o)
