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
            self.actual = Token(type("a"),"EOF")
        elif self.origin[self.position] == " ":
            while self.origin[self.position] == " ":
                self.position+=1
                if final == self.position:
                    break
        if final == self.position:
            self.actual = Token(type("a"),"EOF")
        elif self.origin[self.position] == "+":
            self.actual = Token(type("+"), "+")
            self.position += 1
        elif self.origin[self.position] == "-":
            self.actual = Token(type("-"), "-")
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
    def parseExpression():
        if Parser.tokens.actual.tipo is int:
            resultado = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while (Parser.tokens.actual.value == "+") or (Parser.tokens.actual.value == "-"):
                if Parser.tokens.actual.value == "EOF":
                    break
                elif Parser.tokens.actual.value == "+":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tipo is int:
                        resultado += Parser.tokens.actual.value
                    else:
                        raise Exception("Erro + com simbolo")
                elif Parser.tokens.actual.value == "-":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tipo is int:
                        resultado -= Parser.tokens.actual.value
                    else:
                        raise Exception("Erro - com simbolo")
                Parser.tokens.selectNext()
            return resultado     
        else:
            if Parser.tokens.actual.value == " ":
                Parser.tokens.selectNext()
            else:
                raise Exception("Erro loop principal")

    @staticmethod
    def run(code):
        Parser.tokens  = Tokenizer(code)
        resultado = Parser.parseExpression()
        return resultado

    

if __name__ == "__main__":

    
    conta = sys.argv[1]
    resultado = Parser.run(conta)
    print(resultado)

        

    