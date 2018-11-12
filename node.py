from symboltable import *

class Node:
    value = None
    children = None

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

<<<<<<< HEAD
    def Evaluate(self, st):
        left_val = self.children[0].Evaluate(st)[0]
        right_val = self.children[1].Evaluate(st)[0]
=======
    def Evaluate(self):
        left_val = self.children[0].Evaluate()
        right_val = self.children[1].Evaluate()
>>>>>>> parent of 53d4024... asdads
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

class RelOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

<<<<<<< HEAD
    def Evaluate(self, st):
        exp1 = self.children[0].Evaluate(st)[0]
        exp2 = self.children[1].Evaluate(st)[0]
=======
    def Evaluate(self):
        exp1 = self.children[0].Evaluate()
        exp2 = self.children[1].Evaluate()
>>>>>>> parent of 53d4024... asdads
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
    
    def Evaluate(self, st):
        return (not self.children)

class BoolOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)
    
    def Evaluate(self, st):
        result = None

        if (self.value == "&&"):
            result = self.children[0].Evaluate(st) and self.children[1].Evaluate(st)
        elif (self.value == "||"):
            result = self.children[0].Evaluate(st) or self.children[1].Evaluate(st)

        return result

class UnOp(Node):
    def __init__(self, value, children):
        Node.__init__(self, value, children)

    def Evaluate(self, st):
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

    def Evaluate(self, st):
        pass


class IdVal(Node):
    def __init__(self, symbol):
        Node.__init__(self, symbol, None)

    def Evaluate(self, st):
        return st.getSymbol(self.value)


class VarDec(Node):
    def __init__(self, tipo, symbol):
        Node.__init__(self, tipo, symbol)

    def Evaluate(self, st):
        for i in self.children:
            st.setType(self.value, i)
    
    def PushSymbol(self, symbol):
        self.children.append(symbol)


class FuncDec(Node):
    def __init__(self, func, children):
        Node.__init__(self, func, children)

    def Evaluate(self, st):
        st.setType(self.value[0], self.value[1])
        st.setSymbol(self.value[1], self)


class FuncCall(Node):
    def __init__(self, name, children):
        Node.__init__(self, name, children)

    def Evaluate(self, st):
        new_st = SymbolTable(st)
        func = st.getSymbol(self.value)

        if (func[0].value[1] != 'main' and func[1] != 'int'):
            raise ValueError("erro de tipo de funcao")
        elif(func[0].value[1] == 'main' and func[1] != 'int'):
            raise ValueError("main tem que ser void")

        counter = 0

        while (counter < len(func[0].children)-1):
            func[0].children[counter].Evaluate(new_st)
            symbol = func[0].children[counter].children[0]
            new_st.setSymbol(symbol, self.children[counter].Evaluate(st)[0])
            counter += 1
        
        return func[0].children[len(func[0].children)-1].Evaluate(new_st)



class Return(Node):
    def __init__(self, child):
        Node.__init__(self, None, child)

    def Evaluate(self, st):
        val = (self.children[0].Evaluate(st))
        if (val[1] != 'int'):
            raise ValueError("funcao nao retorna int")
        return val
        

class Printf(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self):
        print(self.children.Evaluate())

class Scanf(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)
    
    def Evaluate(self, st):
        temp = int(input())
        SymbolTable.setSymbol(self.children.value, temp)

class If(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self, st):
        if (self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)
        else:
            if (self.children[2]):
                self.children[2].Evaluate(st)

class While(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)
    
    def Evaluate(self, st):
        while(self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)


class Eq(Node):
    def __init__(self, symbol, children):
        Node.__init__(self, symbol, children)

    def Evaluate(self):
        tipo = SymbolTable.getType(self.value.value)
        valor = self.children.Evaluate()
        if (type(valor) == int and tipo == 'int'):
            SymbolTable.setSymbol(self.value.value, valor)
        elif (type(valor) == str and tipo == 'str'):
            SymbolTable.setSymbol(self.value.value, valor)
        elif(type(valor) == 'char' and tipo == 'char'):
            SymbolTable.setSymbol(self.value.value, valor)
        else:
            raise ValueError

class Commands(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def Evaluate(self, st):
        for i in self.children:
            if (isinstance(i, Return)):
                return i.Evaluate(st)

            i.Evaluate(st)
    
    def pushChild(self, child):
        self.children.append(child)

class Program(Node):
    def __init__(self, st, children):
        Node.__init__(self, st, children)

    def Evaluate(self, st):
        for i in self.children:
            i.Evaluate(self.value)
    
    def pushChild(self, child):
        self.children.append(child)
