NUM = "NUM"
EOF = "EOF"
OP = "OP"
OP2 = "OP2"

import re

class Analisador:
    tokenizador = None

    def inicializarTokenizador(codigoFonte):
        Analisador.tokenizador = Tokenizador(codigoFonte)

    def termo():
        resultado = 0
        tokenizador = Analisador.tokenizador
        tokenizador.selecionarProximo()
        if (tokenizador.atual.tipo != EOF):
            # print(tokenizador.atual.tipo, tokenizador.atual.valor)
            if tokenizador.atual.tipo == NUM:
                resultado += int(tokenizador.atual.valor)
                tokenizador.selecionarProximo()
                while (tokenizador.atual.tipo != OP and tokenizador.atual.tipo != EOF):
                    if (tokenizador.atual.valor == "*"):
                        tokenizador.selecionarProximo()
                        if (tokenizador.atual.tipo == NUM):
                            resultado *= int(tokenizador.atual.valor)
                        else:
                            raise ValueError ("Erro de sintaxe")
                    elif (tokenizador.atual.valor == "/"):
                        tokenizador.selecionarProximo()
                        if tokenizador.atual.tipo == NUM:
                            resultado /= int(tokenizador.atual.valor)
                        else:
                            raise ValueError ("Erro de sintaxe")
                    tokenizador.selecionarProximo()
            else:
                raise ValueError ("Erro no primeiro token")

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


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Tokenizador:

    def __init__(self, codigoFonte):
        tempCodigo = codigoFonte
        while(re.search("\/\*((?!\/\*).)*\*\/", tempCodigo)):
            tempCodigo = re.sub("\/\*((?!\/\*).)*\*\/", "", tempCodigo)
        
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


Analisador.inicializarTokenizador(input("CODIGO: "))
print(Analisador.analisarExpressao())
