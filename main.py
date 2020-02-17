#/usr/bin/python
import sys
conta = sys.argv[1]

last_char_isspace = False
last_valid_isnumeric = False
# resolver espaço duplo
for cha in conta:
    if last_char_isspace:
        if last_valid_isnumeric and cha.isnumeric():
            print("ERRO: espaço entre números")
            exit()
    if cha == " ":
        last_char_isspace = True
    else:
        last_char_isspace = False
        if cha.isnumeric():
            last_valid_isnumeric = True
        else:
            last_valid_isnumeric = False

conta = conta.replace(" ","")

if not conta:
    print("ERRO: String vazia")
    exit()

sep = list(conta)

if not sep[0].isnumeric() or not sep[-1].isnumeric():
    print("ERRO: Formatação inválida")
    exit()


begin = 0
end = 0
first = True

for i in range(len(conta)):
    
    if conta[i].isnumeric():
        end+=1

    else:
        if first == True:
            result = int(conta[begin:end])
            
            first = False
            sig = conta[i]
        
        elif sig == "+":
            result+=int(conta[begin:end])
            sig = conta[i]
        elif sig == "-":
            result-=int(conta[begin:end])
            sig=conta[i]
        else:
            print("ERRO: Sinal inválido")
            exit()

        begin = i+1
        end+=1

    if i == (len(conta)-1):
        if sig == "+":
            result+=int(conta[begin:len(conta)])
        else:
            result-=int(conta[begin:len(conta)])

print('Resultado final: ',result)
    
 



        

    



