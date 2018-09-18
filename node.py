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
        left_val = self.children[0].Evaluate()
        right_val = self.children[1].Evaluate()
        result = None

        if self.value == '+':
            result = left_val+right_val
        elif self.value == '*':
            result = left_val*right_val
        elif self.value == '/':
            result = left_val/right_val
        elif self.value == "-":
            result = left_val-right_val

        return result

class UnOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self):
        result = None

        if self.value == "-":
            result = self.children[0].Evaluate() * -1
        elif self.value == "+":
            result = self.children[0].Evaluate()

        return result

class IntVal(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self):
        return int(self.value)


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

class Printf(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self):
        print(self.children.Evaluate())

class Eq(Node):
    def __init__(self, symbol, children):
        Node.__init__(self, symbol, children)

    def Evaluate(self):
        SymbolTable.setSymbol(self.value.value, self.children.Evaluate())

class Commands(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self):
        for i in self.children:
            i.Evaluate()
