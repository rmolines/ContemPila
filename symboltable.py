class SymbolTable:
    valueTable = dict()
    typeTable = dict()

    def setSymbol(symbol, value):
        SymbolTable.valueTable[symbol] = value

    def getSymbol(symbol):
        return SymbolTable.valueTable[symbol]
    
    def setType(tipo, symbol):
        SymbolTable.typeTable[symbol] = tipo

    def getType(symbol):
        return SymbolTable.typeTable[symbol]

