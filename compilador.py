import re
from node import *
from tokenizador import *

class Analisador:
    tokenizador = None
    raiz = None

    def inicializarTokenizador(codigoFonte):
        Analisador.tokenizador = Tokenizador(codigoFonte)
        Analisador.tokenizador.selecionarProximo()
        st = SymbolTable(None)
        Analisador.raiz = Program(st, [])

    def analisarFuncDec():
        tokenizador = Analisador.tokenizador
        nodes = []
        node = None
        tipo = None
        has_more_args = True
        arg_tipo = None
        arg_id = None

        while (tokenizador.atual.tipo == TYPE):
            args = []

            tipo = tokenizador.atual.valor
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == ID_):
                func = (tipo, tokenizador.atual.valor)
                tokenizador.selecionarProximo()
                if(tokenizador.atual.valor == "("):
                    tokenizador.selecionarProximo()
                    if(tokenizador.atual.tipo == TYPE):  
                        while(has_more_args):
                            arg_tipo = tokenizador.atual.valor
                            tokenizador.selecionarProximo()
                            if(tokenizador.atual.tipo == ID_):
                                arg_id = tokenizador.atual.valor
                                args.append(VarDec(arg_tipo, [arg_id]))
                                tokenizador.selecionarProximo()
                                if(tokenizador.atual.valor == ")"):
                                    tokenizador.selecionarProximo()
                                    has_more_args = False
                                elif(tokenizador.atual.tipo == COMMA):
                                    tokenizador.selecionarProximo()
                            else:
                                raise ValueError("Erro de declaracao de argumento")
                    elif (tokenizador.atual.valor == ")"):
                        tokenizador.selecionarProximo()

                    node = Analisador.analisarComandos()
                    args.append(node)
                    node = FuncDec(func, args)
                    Analisador.raiz.pushChild(node)
    
        Analisador.raiz.pushChild(Analisador.analisarFuncCall()) 
            
        

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

    def analisarFuncCall():
        tokenizador = Analisador.tokenizador
        id_ = None
        children = []

        if (tokenizador.atual.tipo == ID_):
            id_ = tokenizador.atual.valor
            tokenizador.selecionarProximo()
            if (tokenizador.atual.valor == "("):
                tokenizador.selecionarProximo()
                while(True):
                    if (tokenizador.atual.valor == ")"):
                        tokenizador.selecionarProximo()
                        break
                    elif (tokenizador.atual.tipo == ID_):
                        children.append(IdVal(tokenizador.atual.valor))
                        tokenizador.selecionarProximo()
                    elif (tokenizador.atual.tipo == NUM):
                        children.append(IntVal(tokenizador.atual.valor, None))
                        tokenizador.selecionarProximo()
                    if(tokenizador.atual.tipo == COMMA):
                        tokenizador.selecionarProximo()
                if (tokenizador.atual.valor is not ';'):
                    raise ValueError("falta ponto e virgula")


        node = FuncCall(id_, children) 
        return (node)           


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
            # if (tokenizador.atual.tipo == PV):
            #     tokenizador.selecionarProximo()
            
        elif (tokenizador.atual.tipo == IF):
            node = Analisador.analisarIf()
            
        elif (tokenizador.atual.tipo == WHILE):
            node = Analisador.analisarWhile()
            # if (tokenizador.atual.tipo == PV):
            #     tokenizador.selecionarProximo()
            
        elif (tokenizador.atual.tipo == TYPE):
            node = Analisador.analisarVarDec()
            if (tokenizador.atual.tipo == PV):
                tokenizador.selecionarProximo()
        
        elif (tokenizador.atual.tipo == RETURN):
            node = Analisador.analisarReturn()
            if (tokenizador.atual.tipo == PV):
                tokenizador.selecionarProximo()

            
            

        return node
    
    def analisarReturn():
        tokenizador = Analisador.tokenizador
        child = None

        if (tokenizador.atual.tipo == RETURN):
            tokenizador.selecionarProximo()
            child = Analisador.analisarExpressao()
        node = Return([child])
        return node


    def analisarVarDec():
        tokenizador = Analisador.tokenizador
        node = None
        tipo = None

        if (tokenizador.atual.tipo == TYPE):
            tipo = tokenizador.atual.valor
            tokenizador.selecionarProximo()
            if (tokenizador.atual.tipo == ID_):
                node = VarDec(tipo, [tokenizador.atual.valor])
                tokenizador.selecionarProximo()
                while (tokenizador.atual.tipo == COMMA):
                    tokenizador.selecionarProximo()
                    if (tokenizador.atual.tipo == ID_):
                        node.PushSymbol(tokenizador.atual.valor)
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
                if(tokenizador.espiarProximo().valor == "("):
                    node = Eq(symbol, Analisador.analisarFuncCall())
                else:
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




code = open("./input", "r").read()
code = code.replace("\n","")
Analisador.inicializarTokenizador(code)
Analisador.analisarFuncDec()
(Analisador.raiz.Evaluate(SymbolTable(None)))
