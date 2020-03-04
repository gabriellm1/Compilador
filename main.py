import sys


class Token():

    def __init__(self,tipo,value):

        self.tipo = tipo
        self.value = value


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
        elif self.origin[self.position].isnumeric():
            while self.origin[self.position].isnumeric():
                buf += self.origin[self.position]
                self.position+=1
                if final == self.position:
                    break  
            self.actual = Token(type(1),int(buf))
            
        else:
            raise Exception("Caracter inválido")




        


class Parser():

    @staticmethod
    def parseTerm():
        if Parser.tokens.actual.tipo is int:
            resultado = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while Parser.tokens.actual.tipo == "*ou/":
                if Parser.tokens.actual.value == "*":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tipo is int:
                        resultado *= Parser.tokens.actual.value
                    else:
                        raise Exception("Erro de formatação")
                elif Parser.tokens.actual.value == "/":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tipo is int:
                        resultado //= Parser.tokens.actual.value
                    else:
                        raise Exception("Erro de formatação")
                Parser.tokens.selectNext()
            return resultado     
        else:
                raise Exception("Erro de formatação")

    @staticmethod
    def parseExpression():
        resultado = Parser.parseTerm()
        while (Parser.tokens.actual.tipo == "+ou-"):
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                resultado += Parser.parseTerm()
            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                resultado -= Parser.parseTerm()
        return resultado
            

    @staticmethod
    def run(code):
        Parser.tokens  = Tokenizer(code)
        resultado = Parser.parseExpression()
        if Parser.tokens.actual.value == "EOF":
            return resultado
        else:
            raise Exception("Erro de formatação")

    

if __name__ == "__main__":

    
    conta = sys.argv[1]
    resultado = Parser.run(conta)
    print(resultado)

        

    