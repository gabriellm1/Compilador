import os
import sys

class Token():

    def __init__(self,tipo,value):

        self.tipo = tipo
        self.value = value


class PrePro():

    @staticmethod
    def filter(precode):
        list_comments = []
        i=0
        while i<len(precode)-1:
            if precode[i]=="/" and precode[i+1]=="*":
                for j in range(i,len(precode)-1):
                    if precode[j]=="*" and precode[j+1]=="/":
                        list_comments.append((i,j))
                        i=(j+2)
                        break
                i+=1
            else:
                i+=1
        length = 0
        for cm in list_comments:
            s = cm[0]-length
            f = cm[1]-length
            precode =  precode[:s] + precode[f+2:]
            length+= (cm[1]-cm[0])+2
        return precode

class Tokenizer():

    def __init__(self,origin):

        self.origin = origin
        self.position = 0
        self.reserveds = ["echo","while","if","else","or","and","readline","true","false","function","return"]
        self.functions = []
        self.actual = Token(type(1),0)
        self.selectNext()

    def selectNext(self):
        buf = ""
        final = len(self.origin)
        if final == self.position:
            self.actual = Token(type("EOF"),"EOF")
        elif self.origin[self.position] == " " or self.origin[self.position] == "\n":
            while self.origin[self.position] == " " or self.origin[self.position] == "\n":
                self.position+=1
                if final == self.position:
                    break
        if final == self.position:
            self.actual = Token(type("EOF"),"EOF")
        elif  self.origin[self.position] == '"':
            self.position+=1
            while (self.origin[self.position] != '"'):
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break
            self.position+=1
            self.actual = Token("string",buf)
        elif self.origin[self.position] == "$":
            buf="$"
            self.position+=1
            if self.origin[self.position].isalpha():
                buf+=self.origin[self.position]
                self.position+=1
            else:
                raise "Variável mal formatada"
            while self.origin[self.position].isalpha() or self.origin[self.position].isnumeric() or self.origin[self.position] == "_":
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break
            self.actual = Token("var",buf)
        elif self.origin[self.position] == "+":
            self.actual = Token("+ou-", "+")
            self.position += 1
        elif self.origin[self.position] == "-":
            self.actual = Token("+ou-", "-")
            self.position += 1
        elif self.origin[self.position] == "!":
            self.actual = Token("+ou-", "!")
            self.position += 1
        elif self.origin[self.position] == ".":
            self.actual = Token("concat", ".")
            self.position += 1
        elif self.origin[self.position] == "*":
            self.actual = Token("*ou/", "*")
            self.position += 1
        elif self.origin[self.position] == "/":
            self.actual = Token("*ou/", "/")
            self.position += 1
        elif self.origin[self.position] == ">":
            self.actual = Token("rel", ">")
            self.position += 1    
        elif self.origin[self.position] == "<":
            if self.origin[self.position+1] == "?" and self.origin[self.position+2] == "p" and self.origin[self.position+3] == "h" and self.origin[self.position+4] == "p":
                self.actual = Token("init_prog", "<?php")
                self.position += 5
            else:
                self.actual = Token("rel", "<")
                self.position += 1    
        elif self.origin[self.position] == "=":
            if self.origin[self.position+1] == "=":
                self.actual = Token("rel", "==")
                self.position += 2
            else:
                self.actual = Token("igual", "=")
                self.position += 1
        elif self.origin[self.position] == "(":
            self.actual = Token("abre(", "(")
            self.position += 1
        elif self.origin[self.position] == ")":
            self.actual = Token("fecha)", ")")
            self.position += 1
        elif self.origin[self.position] == "{":
            self.actual = Token("abre{", "{")
            self.position += 1
        elif self.origin[self.position] == "}":
            self.actual = Token("fecha}", "}")
            self.position += 1
        elif self.origin[self.position] == ";":
            self.actual = Token("fim", ";")
            self.position += 1
        elif self.origin[self.position] == "?" and self.origin[self.position+1] == ">":
            self.actual = Token("end_prog", "?>")
            self.position += 2        
        elif self.origin[self.position].isnumeric():
            while self.origin[self.position].isnumeric():
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break
            self.actual = Token(type(1),int(buf))
        elif self.origin[self.position] == ",":
            self.actual = Token("separador",",")
            self.position+=1
        elif self.origin[self.position].isalpha():
            while self.origin[self.position].isalpha():
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break
            if buf.lower() in self.reserveds:
                self.actual = Token("reserved",buf.lower())
            elif self.actual.value == "function":
                self.actual = Token("func_name",buf.lower())
            else:
                self.actual = Token("pos_func",buf.lower())
                #raise "Not reserved word or variable"
    
        else:
            raise "Caracter inválido"


class Node():
    def __init__(self,value,children):
        self.value = value
        self.children = children
    def Evaluate(self,table):
        pass

class FuncDec(Node):
    def __init__(self,value,children):
        self.value = value # nome funcao
        self.children = children # n - ident / n+1 - return
    def Evaluate(self,table):
        table.FuncSet(self.value,self.children)

class FuncCall(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children
    def Evaluate(self,table):
        func = table.FuncGet(self.value) # self.children do funcdec
        parameters = func[:-1]
        if (len(parameters) == len(self.children)):
            local_table = SymbolTable()
            for i in range(len(parameters)):
                local_table.Setter(parameters[i].value,self.children[i].Evaluate(table))
            func[-1].Evaluate(local_table)
            if "return" in local_table.table.keys():
                return local_table.table["return"]
            else:
                return ["string",""]
        else:
            raise "Quantidade de parâmetros errada"

class Return(Node):
    def __init__(self,value):
        self.value = value
    def Evaluate(self,table):
        table.Setter("return",self.value.Evaluate(table))

class Command(Node):
    def __init__(self,children):
        self.children = children
    def Evaluate(self,table):
        for node in self.children:
            node.Evaluate(table)
            if "return" in table.table.keys():
                break

class Assingnment(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children
    def Evaluate(self,table):
        table.Setter(self.value,self.children[0].Evaluate(table))
        
class Identifier(Node):
    def __init__(self,value):
        self.value = value
    def Evaluate(self,table):
        return table.Getter(self.value)

class Readline(Node):
    def __init__(self):
        pass
    def Evaluate(self,table):
        return ["int",int(input())]

class IF(Node):
    def __init__(self,children):
        self.children = children
    def Evaluate(self,table):
        if self.children[0].Evaluate(table)[1]:
            self.children[1].Evaluate(table)
        elif len(self.children) == 3:
            self.children[2].Evaluate(table)

class WHILE(Node):
    def __init__(self,children):
        self.children = children
    def Evaluate(self,table):
        while self.children[0].Evaluate(table)[1]:
            self.children[1].Evaluate(table)  

class Echo(Node):
    def __init__(self,children):
        self.children = children
    def Evaluate(self,table):
        print(self.children[0].Evaluate(table)[1])

class BinOp(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children
    
    def Evaluate(self,table):
        if self.value == "and" or self.value == "or":
            if self.children[0].Evaluate(table)[0] == 'int':
                if self.children[0].Evaluate(table)[1] != 0:
                    first = ["int",True]
                else:
                    first = ["int",False]
            elif self.children[0].Evaluate(table)[0] == 'string':
                raise "Tipos de variáveis incompatíveis"
            else:
                first = self.children[0].Evaluate(table)
            if self.children[1].Evaluate(table)[0] == 'int':
                if self.children[1].Evaluate(table)[1] != 0:
                    second = ["int",True]
                else:
                    second = ["int",False]
            elif self.children[1].Evaluate(table)[0] == 'string':
                raise "Tipos de variáveis incompatíveis"
            else:
                second = self.children[1].Evaluate(table)
        else:
            if self.children[0].Evaluate(table)[0] == 'bool':
                if self.children[0].Evaluate(table)[1] == True:
                    first = ["bool",1]
                else:
                    first = ["bool",0]
            else:
                first = self.children[0].Evaluate(table)
            if self.children[1].Evaluate(table)[0] == 'bool':
                if self.children[1].Evaluate(table)[1] == True:
                    second = ["bool",1]
                else:
                    second = ["bool",0]
            else:
                second = self.children[1].Evaluate(table)

        if self.value == "*":
            if first[0] == "string" or second[0] == "string":
                raise "Tipos de variáveis incompatíveis"
            return ["int",first[1] * second[1]]

        elif self.value == "/":
            if first[0] == "string" or second[0] == "string":
                raise "Tipos de variáveis incompatíveis"
            return ["int",first[1] // second[1]]

        elif self.value == "+":
            if first[0] == "string" or second[0] == "string":
                raise "Tipos de variáveis incompatíveis"
            return ["int",first[1] + second[1]]

        elif self.value == "-":
            if first[0] == "string" or second[0] == "string":
                raise "Tipos de variáveis incompatíveis"
            return ["int",first[1] - second[1]]
        
        elif self.value == "and":
            return ["bool",first[1] and second[1]]
        
        elif self.value == "or":
            return ["bool",first[1] or second[1]]

        elif self.value == "==":
            if (first[0] == "string" and second[0] != "string") or (first[0] != "string" and second[0] == "string"):
                raise "Tipos de variáveis incompatíveis"
            return ["bool",first[1] == second[1]]

        elif self.value == ">":
            if first[0] == "string" or second[0] == "string":
                raise "Tipos de variáveis incompatíveis"
            return ["bool",first[1] > second[1]]

        elif self.value == "<":
            if first[0] == "string" or second[0] == "string":
                raise "Tipos de variáveis incompatíveis"
            return ["bool",first[1] < second[1]]

        elif self.value == ".":
            return ["string",str(first[1]) + str(second[1])]

class UnOp(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children

    def Evaluate(self,table):
        if self.children[0].Evaluate(table)[0] == "string":
            raise "String não é compatível com operação unitária"
        else:
            if self.value == "+":
                return  ["int",+ self.children[0].Evaluate(table)[1]]

            elif self.value == "-":
                return  ["int",- self.children[0].Evaluate(table)[1]]
            elif self.value == "!":
                return  ["bool",not self.children[0].Evaluate(table)[1]]

class IntVal(Node):
    def __init__(self,value):
        self.value = value
    
    def Evaluate(self,table):
        return ["int",self.value]

class StringVal(Node):
    def __init__(self,value):
        self.value = value
    
    def Evaluate(self,table):
        return ["string",self.value]

class BoolVal(Node):
    def __init__(self,value):
        self.value = value
    
    def Evaluate(self,table):
        if self.value == "true":
            return ["bool",True]
        elif self.value == "false":
            return ["bool",False]

class NoOp(Node):
    def __init__(self):
        pass
    def Evaluate(table):
        pass

class SymbolTable:

    func = {}

    def __init__(self):
        self.table = {}
        
    def Setter(self,simbol,value):
        self.table[simbol] = value
    def Getter(self,simbol):
        if simbol not in self.table.keys():
            raise "Variável não inicializada"
        return self.table[simbol]
    @staticmethod
    def FuncSet(simbol,value):
        if simbol in SymbolTable.func.keys():
            raise "Função já declarada"
        SymbolTable.func[simbol] = value
    @staticmethod
    def FuncGet(simbol):
        if simbol not in SymbolTable.func.keys():
            raise "Função não declarada"
        return SymbolTable.func[simbol]




class Parser():

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.tipo is int:
            valor = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return IntVal(valor)
        elif Parser.tokens.actual.tipo == "string":
            valor = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return StringVal(valor)
        elif Parser.tokens.actual.tipo == "var":
            var_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return Identifier(var_name)
        elif (Parser.tokens.actual.tipo == "+ou-"):
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                return UnOp("+",[Parser.parseFactor()])
            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                return UnOp("-",[Parser.parseFactor()])
            elif Parser.tokens.actual.value == "!":
                Parser.tokens.selectNext()
                return UnOp("!",[Parser.parseFactor()])
        elif Parser.tokens.actual.tipo == "abre(":
            Parser.tokens.selectNext()
            node = Parser.parseRelexpression()
            if Parser.tokens.actual.tipo != "fecha)":
                raise "Parênteses não fechado"
            Parser.tokens.selectNext()
            return node
        elif Parser.tokens.actual.tipo == "reserved":
            if Parser.tokens.actual.value == "readline":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tipo == "abre(":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tipo == "fecha)":
                        Parser.tokens.selectNext()
                        return Readline()
                    else:
                        raise "Parênteses não fechado"
                else:
                    raise "Parênteses não aberto"     
            elif Parser.tokens.actual.value == "true" or Parser.tokens.actual.value == "false":
                node = BoolVal(Parser.tokens.actual.value)
                Parser.tokens.selectNext()
                return node
        elif Parser.tokens.actual.tipo == "pos_func":
            func_name = Parser.tokens.actual.value
            parameters = []
            Parser.tokens.selectNext()
            if Parser.tokens.actual.tipo == "abre(":    
                Parser.tokens.selectNext()
                while Parser.tokens.actual.tipo != "fecha)":
                    if Parser.tokens.actual.tipo == "separador":
                        Parser.tokens.selectNext()
                    parameters.append(Parser.parseRelexpression())
                Parser.tokens.selectNext()
                return FuncCall(func_name,parameters)
            else:
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tipo == "igual":
                    raise "Variável mal formatada"
                else:
                    raise "Chamada de função mal formatada"
        else:
            raise "Erro de formatação"


    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        while (Parser.tokens.actual.tipo == "*ou/") or (Parser.tokens.actual.value == "and"):
            if Parser.tokens.actual.value == "*":
                Parser.tokens.selectNext()
                node = BinOp("*",[node, Parser.parseFactor()])
            elif Parser.tokens.actual.value == "/":
                Parser.tokens.selectNext()
                node = BinOp("/",[node, Parser.parseFactor()])
            elif Parser.tokens.actual.value == "and":
                Parser.tokens.selectNext()
                node = BinOp("and",[node, Parser.parseFactor()])
        return node


    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
        while (Parser.tokens.actual.tipo == "+ou-") or (Parser.tokens.actual.value == "or") or (Parser.tokens.actual.value == "."):
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                node = BinOp("+",[node, Parser.parseTerm()])
            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                node = BinOp("-",[node, Parser.parseTerm()])
            elif Parser.tokens.actual.value == "or":
                Parser.tokens.selectNext()
                node = BinOp("or",[node, Parser.parseTerm()])
            elif Parser.tokens.actual.value == ".":
                Parser.tokens.selectNext()
                node = BinOp(".",[node, Parser.parseTerm()])
        return node

    @staticmethod
    def parseRelexpression():
        node = Parser.parseExpression()
        while (Parser.tokens.actual.tipo == "rel"):
            if Parser.tokens.actual.value == "==":
                Parser.tokens.selectNext()
                node = BinOp("==",[node, Parser.parseExpression()])
            elif Parser.tokens.actual.value == ">":
                Parser.tokens.selectNext()
                node = BinOp(">",[node, Parser.parseExpression()])
            elif Parser.tokens.actual.value == "<":
                Parser.tokens.selectNext()
                node = BinOp("<",[node, Parser.parseExpression()])
        return node

    @staticmethod
    def parseCommand():
        if Parser.tokens.actual.tipo == "var":
            var_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.tipo == "igual":
                Parser.tokens.selectNext()
                node = Assingnment(var_name,[Parser.parseRelexpression()])
            else:
                raise "Erro de formatação"
            if Parser.tokens.actual.tipo == "fim":
                Parser.tokens.selectNext()
                return node
            else:
                raise "Falta ; no fim da linha"
        elif Parser.tokens.actual.tipo == "pos_func":
            func_name = Parser.tokens.actual.value
            parameters = []
            Parser.tokens.selectNext()
            if Parser.tokens.actual.tipo == "abre(":    
                Parser.tokens.selectNext()
                while Parser.tokens.actual.tipo != "fecha)":
                    if Parser.tokens.actual.tipo == "separador":
                        Parser.tokens.selectNext()
                    parameters.append(Parser.parseRelexpression())
                Parser.tokens.selectNext()
                node = FuncCall(func_name,parameters)
            else:
                if Parser.tokens.actual.tipo == "igual":
                    raise "Variável mal formatada"
                else:
                    raise "Chamada de função mal formatada"
            if Parser.tokens.actual.tipo == "fim":
                Parser.tokens.selectNext()
                return node
            else:
                raise "Falta ; no fim da linha"
        elif Parser.tokens.actual.tipo == "reserved":
            if Parser.tokens.actual.value == "echo":
                Parser.tokens.selectNext()
                node = Echo([Parser.parseRelexpression()])

            elif Parser.tokens.actual.value == "if":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tipo == "abre(":
                    Parser.tokens.selectNext()
                    cond = Parser.parseRelexpression()
                    if Parser.tokens.actual.tipo == "fecha)":
                        Parser.tokens.selectNext()
                        ifnode = Parser.parseCommand()
                        if Parser.tokens.actual.value == "else":
                            Parser.tokens.selectNext()
                            return IF([cond,ifnode,Parser.parseCommand()])
                        else:
                            return IF([cond,ifnode])
                    else:
                        raise "Parênteses não fechado"
                else:
                    raise "Parênteses não aberto"
            elif Parser.tokens.actual.value == "while":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tipo == "abre(":
                    Parser.tokens.selectNext()
                    cond = Parser.parseRelexpression()
                    if Parser.tokens.actual.tipo == "fecha)":
                        Parser.tokens.selectNext()
                        return WHILE([cond,Parser.parseCommand()])
                    else:
                        raise "Parênteses não fechado"
                else:
                    raise "Parênteses não aberto"

            elif Parser.tokens.actual.value == "function":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.tipo == "func_name":
                    func_name = Parser.tokens.actual.value
                    parameters = []
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tipo == "abre(":
                        Parser.tokens.selectNext()
                        while Parser.tokens.actual.tipo != "fecha)":
                            if Parser.tokens.actual.tipo == "separador":
                                Parser.tokens.selectNext()
                            parameters.append(Parser.parseRelexpression())
                        Parser.tokens.selectNext()
                        parameters.append(Parser.parseBlock())
                        return FuncDec(func_name,parameters)
                    else:
                        raise "Função mal formatada"
            
            elif Parser.tokens.actual.value == "return":
                Parser.tokens.selectNext()
                node = Return(Parser.parseRelexpression())


            if Parser.tokens.actual.tipo == "fim":
                Parser.tokens.selectNext()
                return node
            else:
                raise "Falta ; no fim da linha"
        else:
            return Parser.parseBlock()

    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.tipo == "abre{":
            list_cmd = []
            Parser.tokens.selectNext()
            while Parser.tokens.actual.tipo != "fecha}":
                list_cmd.append(Parser.parseCommand())
            if Parser.tokens.actual.tipo == "fecha}":
                Parser.tokens.selectNext()
                return Command(list_cmd)
            else:
                raise "Chaves não fechadas (})"
        else:
            raise "Bloco não aberto com chaves({)"


    @staticmethod
    def parseProgram():
        list_cmd = []
        if Parser.tokens.actual.tipo == "init_prog":
            Parser.tokens.selectNext()
            while Parser.tokens.actual.tipo != "end_prog":
                list_cmd.append(Parser.parseCommand())
            if Parser.tokens.actual.tipo == "end_prog":
                Parser.tokens.selectNext()
                return Command(list_cmd)
            else:
                raise "Program não fechado"
        else:
            raise "Programa não aberto"


    @staticmethod
    def run(code):
        Parser.prepro = PrePro()
        pp_code = Parser.prepro.filter(code)
        Parser.tokens  = Tokenizer(pp_code)
        root = Parser.parseProgram()
        Parser.Table = SymbolTable()
        
        if Parser.tokens.actual.value == "EOF":
            return root.Evaluate(Parser.Table)
        else:
            raise "Erro de EOF"
    

if __name__ == "__main__":


    file = sys.argv[1]
    if os.path.splitext(file)[1] != ".php":
        raise "Arquivo não do tipo .php"
    else:
        with open(file, "r") as source:
            conta = source.read()
    Parser.run(conta)

        

    
