class SymbolTable():

    def __init__(self, ancestor):
        self.ancestor = ancestor
        self.valueTable = dict()
        self.typeTable = dict()
        self.ancestor = ancestor

    def setSymbol(self, symbol, value):
        self.valueTable[symbol] = value

    def getSymbol(self, symbol):
        st = self
        while(symbol not in st.valueTable):
            st = st.ancestor
            if (st is None):
                raise ValueError("id nao existe")

        return (st.valueTable[symbol], st.typeTable[symbol])
    
    def setType(self, tipo, symbol):
        self.typeTable[symbol] = tipo

    def getType(self, symbol):
        st = self
        while(symbol not in st.typeTable):
            st = st.ancestor
            if (st is None):
                raise ValueError("id nao existe")

        return st.typeTable[symbol]

        

