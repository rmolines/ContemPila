class SymbolTable:
    valueTable = dict()
    typeTable = dict()

    def setSymbol(symbol, value):
        SymbolTable.valueTable[symbol] = value

    def getSymbol(symbol):
        return (SymbolTable.valueTable[symbol], SymbolTable.typeTable[symbol])
    
    def setType(tipo, symbol):
        SymbolTable.typeTable[symbol] = tipo

    def getType(symbol):
        return SymbolTable.typeTable[symbol]
    
class IDGenerator:
    token_id = 0

    def getID():
        current_id = IDGenerator.token_id
        IDGenerator.token_id += 1
        return current_id
    

