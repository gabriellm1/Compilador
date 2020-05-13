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
        self.reserveds = ["echo","while","if","else","or","and","readline","true","false"]
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
        elif self.origin[self.position].isalpha():
            while self.origin[self.position].isalpha():
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break
            if buf.lower() in self.reserveds:
                self.actual = Token("reserved",buf.lower())
            else:
                raise "Not reserved word or variable"
    
        else:
            raise "Caracter inválido"


class assembly_gen():

    @staticmethod    
    def init_code():
        with open('inicio.asm', 'r') as inicial:
            assembly_gen.buffer = inicial.read()


    @staticmethod    
    def write_code(code):
        assembly_gen.buffer+=code
        #print(assembly_gen.buffer)

    @staticmethod    
    def flush():

        f = open("program.asm",'w')        

        f.write(assembly_gen.buffer)

        final = "\n\n\n\n; interrupcao de saida\n   POP EBP\n   MOV EAX, 1\n    INT 0x80\n"
        f.write(final)
        f.close()

    




class Node():
    def __init__(self,value,children):
        self.value = value
        self.children = children
    def Evaluate(self,table):
        pass
    id = 0
    @staticmethod
    def newId():
        Node.id += 1
        return Node.id

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
        if table.isNew(self.value):
            assembly_gen.write_code("\nPUSH DWORD 0")
            self.children[0].Evaluate(table)
            table.desloc+=4
            table.Setter(self.value,table.desloc)
            assembly_gen.write_code("\nMOV [EBP-{}], EBX".format(table.desloc))
        else:
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nMOV [EBP-{}], EBX".format(table.Getter(self.value)))


        
class Identifier(Node):
    def __init__(self,value):
        self.value = value
    def Evaluate(self,table):
        #return table.Getter(self.value)
        assembly_gen.write_code("\nMOV EBX, [EBP-{}]".format(table.Getter(self.value)))

class Readline(Node):
    def __init__(self):
        pass
    def Evaluate(self,table):
        return ["int",int(input())]

class IF(Node):
    def __init__(self,children):
        self.children = children
        self.id = Node.newId()
    def Evaluate(self,table):
        assembly_gen.write_code("\nIF_{}:".format(self.id))
        self.children[0].Evaluate(table)
        assembly_gen.write_code("\nCMP EBX, False")
        if len(self.children) == 3:
            assembly_gen.write_code("\nJE ELSE_{}".format(self.id))
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nJMP ENDIF_{}".format(self.id))
            assembly_gen.write_code("\nELSE_{}:".format(self.id))
            self.children[2].Evaluate(table)
            assembly_gen.write_code("\nENDIF_{}:".format(self.id))
        else:
            assembly_gen.write_code("\nJE ENDIF_{}".format(self.id))
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nENDIF_{}:".format(self.id))
        # if self.children[0].Evaluate(table)[1]:
        #     self.children[1].Evaluate(table)
        # elif len(self.children) == 3:
        #     self.children[2].Evaluate(table)

class WHILE(Node):
    def __init__(self,children):
        self.children = children
        self.id = Node.newId()
    def Evaluate(self,table):
        id = self.newId()
        assembly_gen.write_code("\nLOOP_{}:".format(self.id))
        self.children[0].Evaluate(table)
        assembly_gen.write_code("\nCMP EBX, False")
        assembly_gen.write_code("\nJE EXIT_{}".format(self.id))
        self.children[1].Evaluate(table) 
        # while self.children[0].Evaluate(table)[1]:
        #     self.children[1].Evaluate(table)  
        assembly_gen.write_code("\nJMP LOOP_{}".format(self.id))
        assembly_gen.write_code("\nEXIT_{}:".format(self.id))

class Echo(Node):
    def __init__(self,children):
        self.children = children
    def Evaluate(self,table):
        self.children[0].Evaluate(table)
        assembly_gen.write_code("\nPUSH EBX")
        assembly_gen.write_code("\nCALL print")
        assembly_gen.write_code("\nPOP EBX")
        #print(self.children[0].Evaluate(table)[1])

class BinOp(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children
    
    def Evaluate(self,table):
        if self.value == "*":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nIMUL EBX")
            assembly_gen.write_code("\nMOV EBX, EAX")
            #return self.children[0].Evaluate(table) * self.children[1].Evaluate(table)

        elif self.value == "/":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nIDIV EBX")
            assembly_gen.write_code("\nMOV EBX, EAX")
            #return self.children[0].Evaluate(table) // self.children[1].Evaluate(table)

        elif self.value == "+":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nADD EAX, EBX")
            assembly_gen.write_code("\nMOV EBX, EAX")
            #return self.children[0].Evaluate(table) + self.children[1].Evaluate(table)

        elif self.value == "-":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nSUB EAX, EBX")
            assembly_gen.write_code("\nMOV EBX, EAX")
            #return self.children[0].Evaluate(table) - self.children[1].Evaluate(table)
        
        elif self.value == "and":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nAND EAX, EBX")
            assembly_gen.write_code("\nMOV EBX, EAX")
            #return self.children[0].Evaluate(table) and self.children[1].Evaluate(table)
        
        elif self.value == "or":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nOR EAX, EBX")
            assembly_gen.write_code("\nMOV EBX, EAX")
            #return self.children[0].Evaluate(table) or self.children[1].Evaluate(table)

        elif self.value == "==":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nCMP EAX, EBX")
            assembly_gen.write_code("\nCALL binop_je")
            #return self.children[0].Evaluate(table) == self.children[1].Evaluate(table)

        elif self.value == ">":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nCMP EAX, EBX")
            assembly_gen.write_code("\nCALL binop_jg")
            #return self.children[0].Evaluate(table) > self.children[1].Evaluate(table)

        elif self.value == "<":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nPUSH EBX")
            self.children[1].Evaluate(table)
            assembly_gen.write_code("\nPOP EAX")
            assembly_gen.write_code("\nCMP EAX, EBX")
            assembly_gen.write_code("\nCALL binop_jl")
            #return self.children[0].Evaluate(table) < self.children[1].Evaluate(table)



class UnOp(Node):
    def __init__(self,value,children):
        self.value = value
        self.children = children

    def Evaluate(self,table):
        # if self.children[0].Evaluate(table)[0] == "string":
        #     raise "String não é compatível com operação unitária"
        # else:
        if self.value == "+":
            self.children[0].Evaluate(table)
            #return  ["int",+ self.children[0].Evaluate(table)[1]]

        elif self.value == "-":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nNEG EBX")
            #return  ["int",- self.children[0].Evaluate(table)[1]]
        elif self.value == "!":
            self.children[0].Evaluate(table)
            assembly_gen.write_code("\nNOT EBX")
            #return  ["bool",not self.children[0].Evaluate(table)[1]]

class IntVal(Node):
    def __init__(self,value):
        self.value = value
    
    def Evaluate(self,table):
        assembly_gen.write_code("\nMOV EBX, {}".format(self.value))
        #return ["int",self.value]

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
            assembly_gen.write_code("\nMOV EBX, {}".format("1"))
            #return ["bool",True]
        elif self.value == "false":
            assembly_gen.write_code("\nMOV EBX, {}".format("0"))
            #return ["bool",False]

class NoOp(Node):
    def __init__(self):
        pass
    def Evaluate(table):
        pass

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.desloc = 0
    def Setter(self,simbol,value):
        self.table[simbol] = value
    def Getter(self,simbol):
        if simbol not in self.table.keys():
            raise "Variável não inicializada"
        return self.table[simbol]
    def isNew(self,simbol):
        if simbol not in self.table.keys():
            return True




class Parser():

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.tipo is int:
            valor = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return IntVal(valor)
        # elif Parser.tokens.actual.tipo == "string":
        #     valor = Parser.tokens.actual.value
        #     Parser.tokens.selectNext()
        #     return StringVal(valor)
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
            # elif Parser.tokens.actual.value == ".":
            #     Parser.tokens.selectNext()
            #     node = BinOp(".",[node, Parser.parseTerm()])
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
        assembly_gen.init_code()
        
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
    assembly_gen.flush()

        

    
