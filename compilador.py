NUM = "NUM"
EOF = "EOF"
OP = "OP"
OP2 = "OP2"
PAR = "PAR"
EQ = "EQ"
PV = "PV"
BRA = "BRA"
PRINTF = "PRINTF"

import re
from node import *

class SymbolTable:
    table = {}

    def setSymbol(symbol, value):
        table[symbol] = value

    def getSymbol(symbol):
        return table[symbol]


class Analisador:
    tokenizador = None

    def inicializarTokenizador(codigoFonte):
        Analisador.tokenizador = Tokenizador(codigoFonte)

    def analisarComandos():
        tokenizador = Analisador.tokenizador
        tokenizador.selecionarProximo()

        if (tokenizador.atual.tipo == BRA):
            tokenizador.selecionarProximo()
            while (tokenizador.atual.tipo != BRA):
                Analisador.analisarComando()


    def analisarComando():
        tokenizador = Analisador.tokenizador
        tokenizador.selecionarProximo()

        if (tokenizador.atual.tipo == PRINT):
            Analisador.analisarPrint
        elif (tokenizador.atual.tipo == ID_):
            Analisador.analisarAtribuicao
        elif (tokenizador.atual.tipo == BRA):
            Analisador.analisarComandos

    def analisarPrint():
        tokenizador = Analisador.tokenizador
        valor = None

        if (tokenizador.atual.tipo == PRINTF):
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == PAR):
                tokenizador.selecionarProximo()
                if (tokenizador.atual.tipo == ID_):
                    valor = SymbolTable.getSymbol(tokenizador.atual.valor)
                elif (tokenizador.atual.tipo == NUM)
                    valor = Analisador.analisarExpressao().Evaluate()
                if(tokenizador.atual.tipo == PAR):
                    print(valor)

    def analisarAtribuicao():
        tokenizador = Analisador.tokenizador

        if (tokenizador.atual.tipo == ID_):
            symbol = tokenizador.atual.valor
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == EQ):
                node = Analisador.analisarExpressao
                SymbolTable.setSymbol(symbol, node.Evaluate())


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
            elif (tokenizador.atual.tipo == ID_):
                node = IdVal(tokenizador.atual.valor, None)
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

            elif (origem[self.posicao] == "=":
                tipo = EQ
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao] == "{" or origem[self.posicao] == "}"):
                tipo = BRA
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao] == ";":
                tipo = PV
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao].isalpha():
                tipo = ID_
                valor = origem[self.posicao]
                self.posicao += 1
                while (origem[self.posicao].isalpha() or \
                       origem[self.posicao].isdigit() or \
                       origem[self.posicao] == "_"):
                       valor += origem[self.posicao]
                       self.posicao += 1

                self.atual = Token(tipo, valor)
                self.posicao += 1

Analisador.inicializarTokenizador(input("CODIGO: "))
node = (Analisador.analisarExpressao())
print(node.Evaluate())
