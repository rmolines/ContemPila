class Analisador:
    tokenizador = None

    def inicializarTokenizador(self, codigoFonte):
        Analisador.tokenizador = Tokenizador(codigoFonte)
        self.resultado = 0

    def analisarExpressao(self):
        tokenizador = Analisador.tokenizador
        tokenizador.selecionarProximo()
        if tokenizador.atual.tipo == "NUM":
            self.resultado += int(tokenizador.atual.valor)
            tokenizador.selecionarProximo()
            while (tokenizador.atual.tipo != "EOF"):
                if (tokenizador.atual.valor == "+"):
                    tokenizador.selecionarProximo()
                    if (tokenizador.atual.tipo == "NUM"):
                        self.resultado += int(tokenizador.atual.valor)
                    else:
                        raise ValueError ("Erro de sintaxe")
                elif (tokenizador.atual.valor == "-"):
                    tokenizador.selecionarProximo()
                    if tokenizador.atual.tipo == "NUM":
                        self.resultado -= int(tokenizador.atual.valor)
                    else:
                        raise ValueError ("Erro de sintaxe")
                else:
                    raise ValueError ("Erro de sintaxe")
                tokenizador.selecionarProximo()
        else:
            raise ValueError ("Erro no primeiro token")

        return self.resultado


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Tokenizador:

    def __init__(self, codigoFonte):
        self.origem = codigoFonte
        self.posicao = 0
        self.atual = None

    def selecionarProximo(self):
        origem = self.origem
        valor = ""

        while(self.posicao < len(origem) and origem[self.posicao] == ' '):
            self.posicao+=1

        print(self.posicao)
        if (self.posicao == len(origem)):
            valor = ""
            tipo = "EOF"
            self.atual = Token(tipo, valor)
        else:
            if(origem[self.posicao].isdigit()):
                tipo = "NUM"
                while(self.posicao < len(origem) and origem[self.posicao].isdigit()):
                    valor = valor + origem[self.posicao]
                    self.posicao+=1
                self.atual = Token(tipo, valor)

            elif(origem[self.posicao] == "+" or origem[self.posicao] == "-"):
                tipo = "OP"
                valor = origem[self.posicao]
                self.atual = Token(tipo, valor)
                self.posicao+=1


anal = Analisador()
anal.inicializarTokenizador("2   -   22   +  1  ")
print (anal.analisarExpressao())
