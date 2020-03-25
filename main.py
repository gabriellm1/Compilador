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
        self.actual = Token(type(1),0)
        self.selectNext()

    def selectNext(self):
        buf = ""
        final = len(self.origin)
        if final == self.position:
            self.actual = Token(type("EOF"),"EOF")
        elif self.origin[self.position] == " ":
            while self.origin[self.position] == " ":
                self.position+=1
                if final == self.position:
                    break
        if final == self.position:
            self.actual = Token(type("EOF"),"EOF")
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
        elif self.origin[self.position] == "(":
            self.actual = Token("abre(", "(")
            self.position += 1
        elif self.origin[self.position] == ")":
            self.actual = Token("fecha)", ")")
            self.position += 1
        elif self.origin[self.position].isnumeric():
            while self.origin[self.position].isnumeric():
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break  
            self.actual = Token(type(1),int(buf))
            
        else:
            raise "Caracter inválido"


class Node():
    def __init__(self,value,children):
        self.value = value
        self.children = children
    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children
    
    def Evaluate(self):
        if self.value == "*":
            return self.children[0].Evaluate() * self.children[1].Evaluate()

        elif self.value == "/":
            return self.children[0].Evaluate() // self.children[1].Evaluate()

        elif self.value == "+":
            return self.children[0].Evaluate() + self.children[1].Evaluate()

        elif self.value == "-":
            return self.children[0].Evaluate() - self.children[1].Evaluate()

class UnOp(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children

    def Evaluate(self):
        if self.value == "+":
            return  + self.children[0].Evaluate()

        elif self.value == "-":
            return  - self.children[0].Evaluate()

class IntVal(Node):
    def __init__(self,value):
        self.value = value
    
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self):
        pass
    def Evaluate():
        pass

class Parser():


    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.tipo is int:
            resultado = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return IntVal(resultado)
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
    def run(code):
        Parser.prepro = PrePro()
        pp_code = Parser.prepro.filter(code)
        Parser.tokens  = Tokenizer(pp_code)
        root = Parser.parseExpression()
        if Parser.tokens.actual.value == "EOF":
            return root
        else:
            raise "Erro de EOF"
    

if __name__ == "__main__":


    file = sys.argv[1]
    if os.path.splitext(file)[1] != ".php":
        raise "Arquivo não do tipo .php"
    else:
        with open(file, "r") as source:
            conta = source.read()
    
    root = Parser.run(conta)
    print(root.Evaluate())

        

    
