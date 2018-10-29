from symboltable import *

class Node:
    value = None
    children = None

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self):
        left_val = self.children[0].Evaluate()[0]
        right_val = self.children[1].Evaluate()[0]
        result = None

        if self.value == '+':
            result = left_val+right_val
        elif self.value == '*':
            result = left_val*right_val
        elif self.value == '/':
            result = left_val/right_val
        elif self.value == "-":
            result = left_val-right_val

        return (result, 'int')

class RelOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self):
        exp1 = self.children[0].Evaluate()[0]
        exp2 = self.children[1].Evaluate()[0]
        result = False
        if (self.value == ">"):
            result = exp1>exp2
        elif (self.value == "<"):
            result = exp1<exp2
        elif (self.value == "=="):
            result = exp1==exp2
        
        return result
            
                
class NotOp(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)
    
    def Evaluate(self):
        return (not self.children)

class BoolOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)
    
    def Evaluate(self):
        result = None

        if (self.value == "&&"):
            result = self.children[0].Evaluate() and self.children[1].Evaluate()
        elif (self.value == "||"):
            result = self.children[0].Evaluate() or self.children[1].Evaluate()

        return result

class UnOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self):
        result = None

        if self.value == "-":
            result = self.children[0].Evaluate()[0] * -1
        elif self.value == "+":
            result = self.children[0].Evaluate()[0]

        return result

class IntVal(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self):
        return (int(self.value), 'int')

class BoolVal(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self):
        return (bool(self.value), 'char')


class NoOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self):
        pass

class IdVal(Node):
    def __init__(self, symbol):
        Node.__init__(self, symbol, None)

    def Evaluate(self):
        return SymbolTable.getSymbol(self.value)

class VarDec(Node):
    def __init__(self, tipo, symbol):
        Node.__init__(self, tipo, symbol)

    def Evaluate(self):
        for i in self.children:
            SymbolTable.setType(self.value, i)
    
    def PushSymbol(self, symbol):
        self.children.append(symbol)

class Printf(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self):
        print(self.children.Evaluate()[0])

class Scanf(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)
    
    def Evaluate(self):
        temp = int(input())
        tipo = SymbolTable.getType(self.children.value)

        SymbolTable.setSymbol(self.children.value, temp)

class If(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self):
        if (self.children[0].Evaluate()):
            self.children[1].Evaluate()
        else:
            if (self.children[2]):
                self.children[2].Evaluate()

class While(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)
    
    def  Evaluate(self):
        while(self.children[0].Evaluate()):
            self.children[1].Evaluate()


class Eq(Node):
    def __init__(self, symbol, children):
        Node.__init__(self, symbol, children)

    def Evaluate(self):
        tipo = SymbolTable.getType(self.value.value)
        valor = self.children.Evaluate()
        if (valor[1] == tipo):
            SymbolTable.setSymbol(self.value.value, valor[0])
        else:
            raise ValueError ('Erro de tipagem')

class Commands(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self):
        for i in self.children:
            i.Evaluate()
