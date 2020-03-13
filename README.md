# Compilador

 - Para rodar : ``` python main.py "1+2" ```
 - Comentários: Abrir com `/*` , e fechar com `*/`

### Diagrama sintático:

![alt text](diagrama.jpeg)

### EBNF:


`EXPRESSION = TERM, {("+" | "-"), TERM}; `

`TERM = FACTOR, {("*" | "/"), FACTOR} ;`

`FACTOR = NUMBER | ("+" | "-"), FACTOR | "(",EXPRESSION,")" ;`

`NUMBER = DIGIT, {DIGIT} ; `

`DIGIT = 0 | 1 | ... | 9 ;`
