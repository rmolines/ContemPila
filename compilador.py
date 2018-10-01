NUM = "NUM"
EOF = "EOF"
OP = "OP"
OP2 = "OP2"
PAR = "PAR"
EQ = "EQ"
PV = "PV"
BRA = "BRA"
PRINTF = "PRINTF"
ID_ = "ID_"
BOOL = "BOOL"
IF = "IF"
WHILE = "WHILE"
ELSE = "ELSE"
BOOLOP = "BOOLOP"
REL = "REL"
NOT = "NOT" 
SCANF = "SCANF" 


import re
from node import *


class Analisador:
    tokenizador = None

    def inicializarTokenizador(codigoFonte):
        Analisador.tokenizador = Tokenizador(codigoFonte)
        Analisador.tokenizador.selecionarProximo()

    def analisarComandos():
        tokenizador = Analisador.tokenizador
        nodes = []
        node = None

        if (tokenizador.atual.valor == "{"):
            tokenizador.selecionarProximo()
            nodes.append(Analisador.analisarComando())
    
            while (tokenizador.atual.valor != "}"):
                nodes.append(Analisador.analisarComando())
            node = Commands(nodes)
        tokenizador.selecionarProximo()


        return node


    def analisarComando():
        tokenizador = Analisador.tokenizador

        node = None

        if (tokenizador.atual.tipo == PRINTF):
            node = Analisador.analisarPrint()
            if (tokenizador.atual.tipo == PV):
                tokenizador.selecionarProximo()

        elif (tokenizador.atual.tipo == SCANF):
            node = Analisador.analisarScanf()
            if (tokenizador.atual.tipo == PV):
                tokenizador.selecionarProximo()
            
        elif (tokenizador.atual.tipo == ID_):
            node = Analisador.analisarAtribuicao()
            if (tokenizador.atual.tipo == PV):
                tokenizador.selecionarProximo()
            
        elif (tokenizador.atual.tipo == BRA):
            node = Analisador.analisarComandos()
            if (tokenizador.atual.tipo == PV):
                tokenizador.selecionarProximo()
            
        elif (tokenizador.atual.tipo == IF):
            node = Analisador.analisarIf()
            
        elif (tokenizador.atual.tipo == WHILE):
            node = Analisador.analisarWhile()
            if (tokenizador.atual.tipo == PV):
                tokenizador.selecionarProximo()
            

        return node

    def analisarPrint():
        tokenizador = Analisador.tokenizador
        valor = None
        node = None
        if (tokenizador.atual.tipo == PRINTF):
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == PAR):
                tokenizador.selecionarProximo()
                node = Analisador.analisarExpressao()
                if(tokenizador.atual.tipo == PAR):
                    node = Printf(node)
                    tokenizador.selecionarProximo()

        return node


    def analisarScanf():
        tokenizador = Analisador.tokenizador
        nodeid = None
        node = None
        if (tokenizador.atual.tipo == SCANF):
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == PAR):
                tokenizador.selecionarProximo()
                if (tokenizador.atual.tipo == ID_):
                    nodeid = IdVal(tokenizador.atual.valor) 
                    tokenizador.selecionarProximo()
                    if(tokenizador.atual.tipo == PAR):
                        node = Scanf(nodeid)
                        tokenizador.selecionarProximo()

        return node

    def analisarWhile():
        tokenizador = Analisador.tokenizador
        node = None
        if (tokenizador.atual.tipo == WHILE):
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == PAR):
                tokenizador.selecionarProximo()
                boolNode = Analisador.analisarBool()
                if (tokenizador.atual.valor == ")"):
                    tokenizador.selecionarProximo()
                    node = While([boolNode, Analisador.analisarComandos()])
        
        return node


    def analisarIf():
        tokenizador = Analisador.tokenizador
        node = None
        if (tokenizador.atual.tipo == IF):
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == PAR):
                tokenizador.selecionarProximo()
                boolNode = Analisador.analisarBool()
                if (tokenizador.atual.valor == ")"):
                    tokenizador.selecionarProximo()
                    node = Analisador.analisarComandos()
                    if (tokenizador.atual.tipo == ELSE):
                        tokenizador.selecionarProximo()
                        node = If([boolNode, node, Analisador.analisarComandos()])
                    else:
                        node = If([boolNode, node, None])


        return node

    def analisarBool():
        tokenizador = Analisador.tokenizador
        node = None

        if (tokenizador.atual.tipo == NOT):
            tokenizador.selecionarProximo()
            node = NotOp(Analisador.analisarRel())
        else :
            node = Analisador.analisarRel()
        
        if (tokenizador.atual.tipo == BOOL):
            valor_atual = tokenizador.atual.valor
            tokenizador.selecionarProximo()
            node = BoolOp(valor_atual, [node, Analisador.analisarBool()])

        return node



    def analisarRel():
        tokenizador = Analisador.tokenizador                
        exp = Analisador.analisarExpressao()
        relOpNode = None

        if (tokenizador.atual.tipo == REL):
            valor_atual = tokenizador.atual.valor
            tokenizador.selecionarProximo()
            relOpNode = RelOp(valor_atual, [exp, Analisador.analisarExpressao()])
        
        return relOpNode

    def analisarAtribuicao():
        tokenizador = Analisador.tokenizador
        node = None

        if (tokenizador.atual.tipo == ID_):
            symbol = IdVal(tokenizador.atual.valor)
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == EQ):
                tokenizador.selecionarProximo()
                node = Eq(symbol, Analisador.analisarExpressao())

        return node


    def analisarExpressao():
        tokenizador = Analisador.tokenizador
        node = Analisador.analisarTermo()

        while (tokenizador.atual.tipo == OP):
            valor_atual = tokenizador.atual.valor
            tokenizador.selecionarProximo()
            node = BinOp(valor_atual, [node, Analisador.analisarTermo()])

        return node


    def analisarTermo():
        tokenizador = Analisador.tokenizador
        node = Analisador.analisarFator()
        
        while (tokenizador.atual.tipo == OP2):
            valor_atual = tokenizador.atual.valor
            tokenizador.selecionarProximo()
            node = BinOp(valor_atual, [node, Analisador.analisarFator()])

        return node


    def analisarFator():
        tokenizador = Analisador.tokenizador

        if (tokenizador.atual.tipo != EOF):
            if tokenizador.atual.tipo == NUM:
                node = IntVal(tokenizador.atual.valor, None)
            elif (tokenizador.atual.tipo == ID_):
                node = IdVal(tokenizador.atual.valor)
            elif tokenizador.atual.tipo == PAR:
                node = Analisador.analisarExpressao()
                if (tokenizador.atual.tipo != PAR):
                    raise ValueError ("Nao fechou parenteses")
            elif tokenizador.atual.tipo == OP:
                node = UnOp(tokenizador.atual.valor, [Analisador.analisarFator()])
            else:
                raise ValueError ("Token fator ou primeiro token invalido")

        tokenizador.selecionarProximo()
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

            elif (origem[self.posicao:self.posicao+2] == "=="):
                tipo = REL
                valor = origem[self.posicao:self.posicao+2]
                self.atual = Token(tipo, valor)
                self.posicao += 2

            elif (origem[self.posicao] == "="):
                tipo = EQ
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao] == "{" or origem[self.posicao] == "}"):
                tipo = BRA
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao] == ";"):
                tipo = PV
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1
            
            elif (origem[self.posicao] == "!"):
                tipo = NOT
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao] == "i" and origem[self.posicao+1] == "f"):
                tipo = IF
                valor = origem[self.posicao]+origem[self.posicao+1]
                self.atual = Token(tipo, valor)
                self.posicao += 2

            elif (origem[self.posicao:self.posicao+4] == "else"):
                tipo = ELSE
                valor = origem[self.posicao:self.posicao+4]
                self.atual = Token(tipo, valor)
                self.posicao += 4

            elif (origem[self.posicao:self.posicao+5] == "scanf"):
                tipo = SCANF
                valor = origem[self.posicao:self.posicao+5]
                self.atual = Token(tipo, valor)
                self.posicao += 5

            elif (origem[self.posicao:self.posicao+5] == "while"):
                tipo = WHILE
                valor = origem[self.posicao:self.posicao+5]
                self.atual = Token(tipo, valor)
                self.posicao += 5

            elif (origem[self.posicao:self.posicao+2] == "||"):
                tipo = BOOL
                valor = origem[self.posicao:self.posicao+2]
                self.atual = Token(tipo, valor)
                self.posicao += 2

            elif (origem[self.posicao:self.posicao+2] == "&&"):
                tipo = BOOL
                valor = origem[self.posicao:self.posicao+2]
                self.atual = Token(tipo, valor)
                self.posicao += 2

            elif (origem[self.posicao] == "!"):
                tipo = NOT
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao] == ">"):
                tipo = REL
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao] == "<"):
                tipo = REL
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1
                 
            elif (origem[self.posicao].isalpha()):
                tipo = ID_
                valor = origem[self.posicao]
                self.posicao += 1
                while (origem[self.posicao].isalpha() or \
                       origem[self.posicao].isdigit() or \
                       origem[self.posicao] == "_"):
                       valor += origem[self.posicao]
                       self.posicao += 1
                if (valor == "printf"):
                    self.atual = Token(PRINTF, valor)
                else:
                    self.atual = Token(tipo, valor)

code = open("./input", "r").read()
code = code.replace("\n","")
Analisador.inicializarTokenizador(code)
node = (Analisador.analisarComandos())
(node.Evaluate())
