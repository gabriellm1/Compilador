# Compilador

 - Para rodar : ``` python main.py exemplo.php ```
 - Comentários: Abrir com `/*` , e fechar com `*/`
 - Para criar um bloco abrir chaves `{`
 - Inserir comandos como echo(para imprimir valor) ou assignment(atribuir valor a variável, exemplo: `$x = 10;`)
 - Sempre terminar um comando com `;`
 - Fechar o bloco com chaves `}`
 - Blocos podem ser criados dentro de outros blocos.
 
 - O arquivo `test.php` possui comentários de parte de códigos que deveriam falhar 

### Diagrama sintático:

![alt text](ds_compilador.png)

### EBNF:

`PROGRAM = "<?php" , {COMMAND} , "?>" ;`

`BLOCK = "{", { COMMAND }, "}" ;`

`COMMAND = ( λ | ASSIGNMENT | PRINT | RETURN | name , "(" , {RELEXPR {"," , RELEXPR} } , ")"), ";" | BLOCK | WHILE | IF | FUNCTION;`

`FUNCTION = "function" , name , "(" , {IDENTIFIER {"," , IDENTIFIER} } , ")" , BLOCK ;` 

`WHILE = "while" , "(" , RELEXPR , ")" , COMMAND ;`

`IF = "if" , "(" , RELEXPR , ")" , {"else" , COMMAND} ;`

`ASSIGNMENT = IDENTIFIER, "=", RELEXPR ;`

`PRINT = "echo", RELEXPR ;`

`RETURN = "return", RELEXPR ;`

`RELEXPR = EXPRESSION, {("==" | ">" | "<"), EXPRESSION}; `

`EXPRESSION = TERM, {("+" | "-" | "or" | "."), TERM}; `

`TERM = FACTOR, {("*" | "/" | "and"), FACTOR} ;`

`FACTOR = NUMBER | STRING | BOOL | ("+" | "-" | "!"), FACTOR | "(",RELEXPR,")" | readline , "(" , ")" | IDENTIFIER | name , "(" , {RELEXPR {"," , RELEXPR} } , ")" ;`

`IDENTIFIER = "$", LETTER, { LETTER | DIGIT | "_" };`

`STRING = """ (LETTER | NUMBER | SYMBOL), {LETTER | NUMBER | SYMBOL} """;`

`LETTER = ( a | ... | z | A | ... | Z ) ;`

`BOOL = True | False`

`NUMBER = DIGIT, {DIGIT} ; `

`DIGIT = 0 | 1 | ... | 9 ;`
