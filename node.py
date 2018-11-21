from symboltable import *
from machinecode import *

class Node:
    value = None
    children = None

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id_ = IDGenerator.getID()

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

    def EvaluateCode(self):
        self.children[0].EvaluateCode()
        MCGenerator.code += "PUSH EBX\n"
        self.children[1].EvaluateCode()
        MCGenerator.code += "POP EAX\n"
        

        if self.value == '+':
            MCGenerator.code += "ADD EAX, EBX\n"
        elif self.value == '*':
            MCGenerator.code += "IMUL EBX\n"
        elif self.value == '/':
            MCGenerator.code += "IDIV EBX\n"
        elif self.value == "-":
            MCGenerator.code += "SUB EAX, EBX\n"
        
        MCGenerator.code += "MOV EBX, EAX\n"


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
    
    def EvaluateCode(self):
        self.children[0].EvaluateCode()
        MCGenerator.code += "PUSH EBX\n"
        self.children[1].EvaluateCode()
        MCGenerator.code += "POP EAX\n"

        result = False
        if (self.value == ">"):
            MCGenerator.code += "CMP EAX, EBX\nCALL binop_jl\nCMP EBX, False\n"
        elif (self.value == "<"):
            MCGenerator.code += "CMP EAX, EBX\nCALL binop_jg\nCMP EBX, False\n"
        elif (self.value == "=="):
            MCGenerator.code += "CMP EAX, EBX\nCALL binop_je\nCMP EBX, False\n"
        
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

    def EvaluateCode(self):
        MCGenerator.code += "MOV EBX, %s\n" % int(self.value)


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
    
    def EvaluateCode(self):
        MCGenerator.code += "MOV EBX, [%s]\n" % self.value

class VarDec(Node):
    def __init__(self, tipo, symbol):
        Node.__init__(self, tipo, symbol)

    def Evaluate(self):
        for i in self.children:
            SymbolTable.setType(self.value, i)
    
    def EvaluateCode(self):
        for i in self.children:
            MCGenerator.bss += "%s RESD 1\n" % i
    
    def PushSymbol(self, symbol):
        self.children.append(symbol)

class Printf(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self):
        print(self.children.Evaluate()[0])

    def EvaluateCode(self):
        self.children.EvaluateCode()
        MCGenerator.code += "PUSH EBX\nCALL print\n"

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

    def EvaluateCode(self):
        self.children[0].EvaluateCode()
        MCGenerator.code += "JE EXIT_%s\n" % self.id_

        self.children[1].EvaluateCode()

        if (self.children[2]):
            MCGenerator.code += "JE EXIT_%s_2\n" % self.id_

            MCGenerator.code += "EXIT_%s\n" % self.id_

            self.children[2].EvaluateCode()

            MCGenerator.code += "EXIT_%s_2\n" % self.id_

        else:
            MCGenerator.code += "EXIT_%s\n" % self.id_

        
        

class While(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)
    
    def  Evaluate(self):
        while(self.children[0].Evaluate()):
            self.children[1].Evaluate()
    
    def EvaluateCode(self):
        MCGenerator.code += "LOOP_%s\n" % self.id_
        self.children[0].EvaluateCode()
        MCGenerator.code += "JE EXIT_%s\n" % self.id_
        self.children[1].EvaluateCode()
        MCGenerator.code += "JMP LOOP_%s\n" % self.id_
        MCGenerator.code += "EXIT_%s\n" % self.id_

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

    def EvaluateCode(self):
        self.children.EvaluateCode()
        MCGenerator.code += "MOV [%s], EBX\n" % (self.value.value)

class Commands(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self):
        for i in self.children:
            i.Evaluate()

    def EvaluateCode(self):
        for i in self.children:
            i.EvaluateCode()