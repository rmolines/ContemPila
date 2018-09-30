class SymbolTable:
    table = dict()

    def setSymbol(symbol, value):
        SymbolTable.table[symbol] = value

    def getSymbol(symbol):
        return SymbolTable.table[symbol]
