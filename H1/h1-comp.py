NUM = "NUM"
EOF = "EOF"
OP = "OP"
OP2 = "OP2"
PAR = "PAR"

import re

class Analisador:
    tokenizador = None

    def inicializarTokenizador(codigoFonte):
        Analisador.tokenizador = Tokenizador(codigoFonte)

    def termo():
        resultado = 0
        tokenizador = Analisador.tokenizador
        
        resultado += Analisador.analisarFator()        
        if (tokenizador.atual.tipo != EOF):
            while ((tokenizador.atual.tipo != PAR and tokenizador.atual.tipo != OP) and tokenizador.atual.tipo != EOF):
                if (tokenizador.atual.valor == "*"):
                    resultado *= Analisador.analisarFator()
                elif (tokenizador.atual.valor == "/"):
                    resultado /= Analisador.analisarFator()

        return resultado


    def analisarExpressao():
        tokenizador = Analisador.tokenizador
        resultado = 0
        resultado += Analisador.termo()
        while (tokenizador.atual.tipo == OP):
            if (tokenizador.atual.valor == "+"):
                resultado += Analisador.termo()
            elif (tokenizador.atual.valor == "-"):
                resultado -= Analisador.termo()
            else:
                raise ValueError ("Erro de sintaxe")

        return resultado

    def analisarFator():
        resultado = 0
        fator = 1
        tokenizador = Analisador.tokenizador
        tokenizador.selecionarProximo()
        if (tokenizador.atual.tipo != EOF):
            if tokenizador.atual.tipo == NUM:
                resultado += int(tokenizador.atual.valor)
                tokenizador.selecionarProximo()
            elif tokenizador.atual.tipo == PAR:
                # tokenizador.selecionarProximo()
                resultado += Analisador.analisarExpressao()
                # tokenizador.selecionarProximo()
                if (tokenizador.atual.tipo != PAR):
                    raise ValueError ("Não fechou parenteses")
                else:
                    tokenizador.selecionarProximo()
            elif tokenizador.atual.tipo == OP:
                if tokenizador.atual.valor == "-":
                    fator *= -1
                resultado += Analisador.analisarFator() * fator
                # tokenizador.selecionarProximo()
            else:
                raise ValueError ("Token fator ou primeiro token inválido")

        return resultado



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
print(Analisador.analisarExpressao())
