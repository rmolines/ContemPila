import re
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
COMMA = ","
TYPE = "TYPE"
RETURN = "RETURN"


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


    def espiarProximo(self):
        pos = self.posicao
        atual = self.atual

        self.selecionarProximo()
        
        token_espiado = self.atual

        self.posicao = pos
        self.atual = atual

        return (token_espiado)

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
            
            elif (origem[self.posicao] == ","):
                tipo = COMMA
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao += 1

            elif (origem[self.posicao] == "i" and origem[self.posicao+1] == "f"):
                tipo = IF
                valor = origem[self.posicao]+origem[self.posicao+1]
                self.atual = Token(tipo, valor)
                self.posicao += 2

            elif (origem[self.posicao:self.posicao+6] == "return"):
                tipo = RETURN
                valor = origem[self.posicao:self.posicao+6]
                self.atual = Token(tipo, valor)
                self.posicao += 6

            elif (origem[self.posicao:self.posicao+4] == "else"):
                tipo = ELSE
                valor = origem[self.posicao:self.posicao+4]
                self.atual = Token(tipo, valor)
                self.posicao += 4

            elif (origem[self.posicao:self.posicao+4] == "char"):
                tipo = TYPE
                valor = origem[self.posicao:self.posicao+4]
                self.atual = Token(tipo, valor)
                self.posicao += 4

            elif (origem[self.posicao:self.posicao+4] == "void"):
                tipo = TYPE
                valor = origem[self.posicao:self.posicao+4]
                self.atual = Token(tipo, valor)
                self.posicao += 4

            elif (origem[self.posicao:self.posicao+3] == "int"):
                tipo = TYPE
                valor = origem[self.posicao:self.posicao+3]
                self.atual = Token(tipo, valor)
                self.posicao += 3

            elif (origem[self.posicao:self.posicao+4] == "main"):
                tipo = ID_
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
