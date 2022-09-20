class Node(object):
    def __init__(self, *args, **kwargs):
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.key = None
        self.data = None
        self.height = None

    def __str__(self):
        if str(self.data):
            return 'Key: ' + str(self.key) + ' Data: ' + str(self.data)

    def getMax(self):
        if self.rightChild:
            return self.rightChild.getMax()
        else:
            return self

    def getMin(self):
        if self.leftChild:
            return self.leftChild.getMin()
        else:
            return self

    def insert(self, node):
        if type(node) == type(Node()):
            if self.key > node.key:
                if not self.leftChild:
                    self.leftChild = node
                    node.parent = self
                else:
                    node.height += 1
                    self.leftChild.insert(node)
            elif self.key < node.key:
                if not self.rightChild:
                    self.rightChild = node
                    node.parent = self
                else:
                    node.height += 1
                    self.rightChild.insert(node)
            else:
                self.data = node.data
        else:
            print('gimme no shit to eat!')

    def findNodeByKey(self, key):
        if self.key == key:
            return self
        elif self.key > key:
            if self.leftChild:
                return self.leftChild.findNodeByKey(key)
        else:
            if self.rightChild:
                return self.rightChild.findNodeByKey(key)

    def getDescendant(self):
        # black magic...keep eye on!
        if self.rightChild:
            return self.rightChild.getMin()
        y = self.parent

        while y and self == y.rightChild:
            self = y
            y = y.parent
        return y

    def preOrder(self):
        print(self)
        print(self.height)
        if self.leftChild:
            self.leftChild.preOrder()
        if self.rightChild:
            self.rightChild.preOrder()

    def update(self, key, value):
        if self.key == key:
            self.data = value
            return self
        elif self.key > key:
            if self.leftChild:
                return self.leftChild.update(key, value)
        else:
            if self.rightChild:
                return self.rightChild.update(key, value)

    def findByName(self, SearchValue):
        if self:
            if self.data["name"] == SearchValue:
                print(self.data)
            if self.leftChild:
                self.leftChild.findByName(SearchValue)
            if self.rightChild:
                self.rightChild.findByName(SearchValue)


class Tree(object):
    def __init__(self):
        self.root = None
        self.count = 0
        self.search = []

    def getMax(self):
        if self.root:
            return self.root.getMax()
        else:
            print('Tree is empty (brought to you by getMax() (tm))')
            return None

    def getMin(self):
        if self.root:
            return self.root.getMin()
        else:
            print('Tree is empty (brought to you by getMin() (tm))')
            return None

    def findNodeByKey(self, key):
        if self.root:
            return self.root.findNodeByKey(key)
        else:
            return None

    def update(self, key, value):
        if self.root:
            return self.root.update(key, value)
        else:
            return None

    def deleteNodeByKey(self, key):
        if self.root:
            # le smart way
            x = None
            y = None
            n = self.root.findNodeByKey(key)
            if not n.leftChild or not n.rightChild:
                x = n
            else:
                x = n.getDescendant()
            if x.leftChild:
                y = x.leftChild
            else:
                y = x.rightChild
            if y:
                y.parent = x.parent
            if not x.parent:
                self.root = y
            elif x == x.parent.leftChild:
                x.parent.leftChild = y
            else:
                x.parent.rightChild = y
            n.key = x.key
            n.data = x.data
        else:
            return None

    def insert(self, key, data):
        n = Node()
        n.key = key
        n.data = data
        if not self.root:
            self.root = n
            n.height = 0
            self.count += 1
        else:
            n.height = 1
            self.root.insert(n)
            self.count += 1

    def preOrder(self):
        if self.root:
            print(self.root)
            if self.root.leftChild:
                self.root.leftChild.preOrder()
            if self.root.rightChild:
                self.root.rightChild.preOrder()
        else:
            print('No hay nada.')

    def findByName(self, SearchValue):
        if self.root:
            if self.root.data["name"] == SearchValue:
                print(self.root.data)
            if self.root.leftChild:
                self.root.leftChild.findByName(SearchValue)
            if self.root.rightChild:
                self.root.rightChild.findByName(SearchValue)

def compression(string):  # string is your input text
    dict = {}
    entry = ''
    index = 1
    for i in range(len(string)):
        entry += string[i]
        if entry not in dict:
            lst = [index]
            encoder = [dict[entry[0:len(entry) - 1]][0] if entry[0:len(entry) - 1] in dict else 0, entry[-1]]
            lst.append(encoder)
            dict[entry] = lst
            index += 1
            entry = ''
    ans = ''
    for x in dict:
        ans += f'<{dict[x][1][0]},{dict[x][1][1]}>'

    return dict, ans  # 'dict' is a dictionary of each symbol with its encoded value, 'ans' is a final encoded version of input


# This function is used to convert your inputed string into an usable dictionary object
def parse(string):
    dict = {}
    index = 1
    incorrect = False
    for i in range(len(string)):
        if string[i] == '<':
            encoderIndex = ''
            encoderTail = ''
            comma = False
            i += 1
            while string[i] != '>':
                if string[i] == ',':
                    comma = True
                    i += 1
                    continue
                if comma:
                    encoderTail += string[i]
                    i += 1
                    continue
                encoderIndex += string[i]
                i += 1

            lst = [[int(encoderIndex), encoderTail], '']
            dict[index] = lst
            index += 1

    return dict


def decompression(string):  # Your input string should be in format <'index', 'entry'>,... . Ex: <0,A><0,B><2,C>
    error = False
    ans, entry = '', ''
    try:
        parse(string)
    except BaseException:
        error = True  # 'error' is true if your input string was not in the correct format.
        return error, ans, {}

    dict = parse(string)
    for x in dict:
        value = dict[x]
        entry += dict[value[0][0]][1] if value[0][0] != 0 else ''
        entry += value[0][1]

        value[1] = entry
        ans += entry
        entry = ''

    return error, ans, dict

def main():
    from csv import reader
    import json
    import re
    print('Por favor ingrese la direccion del archivo CSV:')
    x = input()

    FileArray = []

    # open file
    with open(x, "r") as my_file:
        file_reader = reader(my_file)
        ArbolDPI = Tree();
        for i in file_reader:
            cont = 1;
            persona = ''
            newObject = {"Operacion": '', "Persona": ''}

            SplitComas = i[0].split(";")
            newObject["Operacion"] = SplitComas[0]
            persona += SplitComas[1] + ","
            pass_valid = True
            while (cont < len(i)):
                if cont < 4:
                    AddComas = i[cont].split(":");
                    if (len(AddComas) == 2):
                        persona += "\"" + AddComas[0] + "\":" + AddComas[1]
                    else:
                        persona += "\"" + AddComas[0] + "\":" + AddComas[1] + ":" + AddComas[2] + ":" + AddComas[3]
                    if (cont != len(i) - 1):
                        persona += ","
                else:
                    if pass_valid:
                        AddComas = i[cont].split(":");
                        persona += "\"" + AddComas[0] + "\":" + AddComas[1]
                        pass_valid = False
                    else:
                        if i[cont][0] != " ":
                            persona += "\""
                            if cont == len(i) - 1:
                                value = i[cont].replace("]", "\"]")
                                persona += value
                            else:
                                persona += i[cont] + "\""
                        else:
                            persona += i[cont]
                    if (cont != len(i) - 1):
                        persona += ","
                cont += 1
            newObject["Persona"] = json.loads(persona)
            FileArray.append(newObject)

        for Object in FileArray:
            Object_Companies = {}
            arrayCompanies = Object["Persona"]["companies"]
            for compania in arrayCompanies:
                text_compress = Object["Persona"]["dpi"] + " " + compania
                dictWithSymbols, encoded = compression(text_compress)
                Object_Companies[compania] = encoded
            Object["Persona"]["companies"] = Object_Companies


        for Object in FileArray:
            if (Object["Operacion"] == "INSERT"):
                ArbolDPI.insert(int(Object["Persona"]["dpi"]), Object["Persona"])
            elif (Object["Operacion"] == "DELETE"):
                ArbolDPI.deleteNodeByKey(int(Object["Persona"]["dpi"]))
            elif (Object["Operacion"] == "PATCH"):
                ArbolDPI.update(int(Object["Persona"]["dpi"]), Object["Persona"])

        while True:
            print('Quieres buscar por DPI o por Nombre?')
            print('')
            print('Escribe D si es por DPI')
            print('Escribe N si es por Nombre')
            print('Escribe E si quieres Descodificar')
            Op1 = input()
            if Op1 == 'D' or Op1 == 'd':
                print('')
                print('Solo deben ser numeros')
                x = input()
                print(ArbolDPI.findNodeByKey(int(x)))
            elif Op1 == 'N' or Op1 == 'n':
                print('')
                print('Si no se imprime nada en pantalla es por que no hay nodos con ese nombre')
                print('Solo letras minusculas')
                name = input()
                ArbolDPI.findByName(name)
            else:
                print('')
                print('Ingresa el DPI codificado')
                codificacion = input()
                error, decoded, dictWithSymbolsDECODED = decompression(codificacion)
                print(decoded)

            print('Preciona Enter Para Repetir el proceso')
            input()

if __name__ == '__main__':
    main()