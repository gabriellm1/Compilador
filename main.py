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
        self.reserveds = ["echo"]
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
        elif self.origin[self.position] == "*":
            self.actual = Token("*ou/", "*")
            self.position += 1
        elif self.origin[self.position] == "/":
            self.actual = Token("*ou/", "/")
            self.position += 1
        elif self.origin[self.position] == "=":
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
        elif self.origin[self.position].isnumeric():
            while self.origin[self.position].isnumeric():
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break
            self.actual = Token(type(1),int(buf))
        elif self.origin[self.position].isalpha():
            while self.origin[self.position].isalpha():
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break
            self.actual = Token("echo",buf)
            if buf.lower() in self.reserveds:
                self.actual = Token("echo",buf.lower())
            else:
                raise "Not reserved word or variable"
    
        else:
            raise "Caracter inválido"


class Node():
    def __init__(self,value,children):
        self.value = value
        self.children = children
    def Evaluate(self,table):
        pass

class Command(Node):
    def __init__(self,children):
        self.children = children
    def Evaluate(self,table):
        for node in self.children:
            node.Evaluate(table)

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

class Echo(Node):
    def __init__(self,children):
        self.children = children
    def Evaluate(self,table):
        print(self.children[0].Evaluate(table))

class BinOp(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children
    
    def Evaluate(self,table):
        if self.value == "*":
            return self.children[0].Evaluate(table) * self.children[1].Evaluate(table)

        elif self.value == "/":
            return self.children[0].Evaluate(table) // self.children[1].Evaluate(table)

        elif self.value == "+":
            return self.children[0].Evaluate(table) + self.children[1].Evaluate(table)

        elif self.value == "-":
            return self.children[0].Evaluate(table) - self.children[1].Evaluate(table)

class UnOp(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children

    def Evaluate(self,table):
        if self.value == "+":
            return  + self.children[0].Evaluate(table)

        elif self.value == "-":
            return  - self.children[0].Evaluate(table)

class IntVal(Node):
    def __init__(self,value):
        self.value = value
    
    def Evaluate(self,table):
        return self.value

class NoOp(Node):
    def __init__(self):
        pass
    def Evaluate(table):
        pass

class SymbolTable:
    def __init__(self):
        self.table = {}
    def Setter(self,simbol,value):
        self.table[simbol] = value
    def Getter(self,simbol):
        if simbol not in self.table.keys():
            raise "Variável não inicializada"
        return self.table[simbol]




class Parser():

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.tipo is int:
            resultado = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return IntVal(resultado)
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
        elif Parser.tokens.actual.tipo == "abre(":
            Parser.tokens.selectNext()
            node = Parser.parseExpression()
            if Parser.tokens.actual.tipo != "fecha)":
                raise "Parênteses não fechado"
            Parser.tokens.selectNext()
            return node
        else:
            raise "Erro de formatação"


    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        while (Parser.tokens.actual.tipo == "*ou/"):
            if Parser.tokens.actual.value == "*":
                Parser.tokens.selectNext()
                node = BinOp("*",[node, Parser.parseFactor()])
            elif Parser.tokens.actual.value == "/":
                Parser.tokens.selectNext()
                node = BinOp("/",[node, Parser.parseFactor()])
        return node


    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
        while (Parser.tokens.actual.tipo == "+ou-"):
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                node = BinOp("+",[node, Parser.parseTerm()])
            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                node = BinOp("-",[node, Parser.parseTerm()])
        return node

    @staticmethod
    def parseCommand():
        if Parser.tokens.actual.tipo == "var":
            var_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.tipo == "igual":
                Parser.tokens.selectNext()
                node = Assingnment(var_name,[Parser.parseExpression()])
            else:
                raise "Erro de formatação"
            if Parser.tokens.actual.tipo == "fim":
                Parser.tokens.selectNext()
                return node
            else:
                raise "Falta ; no fim da linha"
        elif Parser.tokens.actual.tipo == "echo":
            Parser.tokens.selectNext()
            node = Echo([Parser.parseExpression()])
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
    def run(code):
        Parser.prepro = PrePro()
        pp_code = Parser.prepro.filter(code)
        Parser.tokens  = Tokenizer(pp_code)
        root = Parser.parseBlock()
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

        

    
