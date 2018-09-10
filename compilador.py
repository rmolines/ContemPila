NUM = "NUM"
EOF = "EOF"
OP = "OP"
OP2 = "OP2"
PAR = "PAR"

import re
from node import *

class Analisador:
    tokenizador = None

    def inicializarTokenizador(codigoFonte):
        Analisador.tokenizador = Tokenizador(codigoFonte)


    def analisarExpressao():
        tokenizador = Analisador.tokenizador
        node = Analisador.analisarTermo()

        while (tokenizador.atual.tipo == OP):
            valor_atual = tokenizador.atual.valor
            node = BinOp(valor_atual, [node, Analisador.analisarTermo()])

        return node
        

    def analisarTermo():
        tokenizador = Analisador.tokenizador
        
        node = Analisador.analisarFator()  
        while (tokenizador.atual.tipo == OP2):
            node = BinOp(tokenizador.atual.valor, [node, Analisador.analisarFator()])

        return node


    def analisarFator():
        tokenizador = Analisador.tokenizador
        tokenizador.selecionarProximo()
        
        if (tokenizador.atual.tipo != EOF): 
            if tokenizador.atual.tipo == NUM:
                node = IntVal(tokenizador.atual.valor, None)
                tokenizador.selecionarProximo()
            elif tokenizador.atual.tipo == PAR:
                node = Analisador.analisarExpressao()
                if (tokenizador.atual.tipo != PAR):
                    raise ValueError ("Não fechou parenteses")
                else:
                    tokenizador.selecionarProximo()
            elif tokenizador.atual.tipo == OP:
                node = UnOp(tokenizador.atual.valor, [Analisador.analisarFator()])
            else:
                raise ValueError ("Token fator ou primeiro token inválido")

        return node



class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Tokenizador:

    def __init__(self, codigoFonte):
        tempCodigo = codigoFonte
        while(re.search("\/\*.*\*\/", tempCodigo)):
            tempCodigo = re.sub("\/\*.*\*\/", "", tempCodigo)
        
        tempCodigo = re.sub("\/\*", "", tempCodigo)
        print(tempCodigo)

        self.origem = tempCodigo
        self.posicao = 0
        self.atual = None

    def selecionarProximo(self):
        origem = self.origem
        valor = ""


        while(self.posicao < len(origem) and origem[self.posicao] == ' '):
            self.posicao+=1

        if (self.posicao == len(origem)):
            valor = ""
            tipo = EOF
            self.atual = Token(tipo, valor)
        else:
            if(origem[self.posicao].isdigit()):
                tipo = NUM
                while(self.posicao < len(origem) and origem[self.posicao].isdigit()):
                    valor = valor + origem[self.posicao]
                    self.posicao+=1
                self.atual = Token(tipo, valor)

            elif(origem[self.posicao] == "+" or origem[self.posicao] == "-" ):
                tipo = OP
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao+=1

            elif (origem[self.posicao] == "*" or origem[self.posicao] == "/"):
                tipo = OP2
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1
            
            elif (origem[self.posicao] == "(" or origem[self.posicao] == ")"):
                tipo = PAR
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1


Analisador.inicializarTokenizador(input("CODIGO: "))
node = (Analisador.analisarExpressao())
print(node.Evaluate())