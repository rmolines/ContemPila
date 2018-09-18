class SymbolTable:
    table = dict()

    def setSymbol(symbol, value):
        SymbolTable.table[symbol] = value

    def getSymbol(symbol):
        print(SymbolTable.table.keys())
        return SymbolTable.table[symbol]
