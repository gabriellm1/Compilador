; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  ; codigo gerado pelo compilador

PUSH DWORD 0
MOV EBX, 8
MOV [EBP-4], EBX
PUSH DWORD 0
MOV EBX, 1
MOV [EBP-8], EBX
PUSH DWORD 0
MOV EBX, 1
MOV [EBP-12], EBX
PUSH DWORD 0
MOV EBX, 4
MOV [EBP-16], EBX
MOV EBX, [EBP-4]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP-8]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP-12]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP-16]
PUSH EBX
CALL print
POP EBX
LOOP_3:
MOV EBX, [EBP-8]
PUSH EBX
MOV EBX, [EBP-4]
POP EAX
CMP EAX, EBX
CALL binop_jl
PUSH EBX
MOV EBX, [EBP-8]
PUSH EBX
MOV EBX, [EBP-4]
POP EAX
CMP EAX, EBX
CALL binop_je
POP EAX
OR EAX, EBX
MOV EBX, EAX
CMP EBX, False
JE EXIT_3
IF_2:
MOV EBX, [EBP-12]
PUSH EBX
MOV EBX, [EBP-16]
POP EAX
CMP EAX, EBX
CALL binop_jg
CMP EBX, False
JE ELSE_2
MOV EBX, [EBP-16]
PUSH EBX
MOV EBX, 1
POP EAX
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-16], EBX
JMP ENDIF_2
ELSE_2:
IF_1:
MOV EBX, [EBP-12]
PUSH EBX
MOV EBX, [EBP-16]
POP EAX
CMP EAX, EBX
CALL binop_jl
CMP EBX, False
JE ELSE_1
MOV EBX, [EBP-12]
PUSH EBX
MOV EBX, 1
POP EAX
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-12], EBX
JMP ENDIF_1
ELSE_1:
MOV EBX, [EBP-12]
PUSH EBX
MOV EBX, 1
POP EAX
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-12], EBX
ENDIF_1:
ENDIF_2:
MOV EBX, [EBP-8]
PUSH EBX
MOV EBX, 1
POP EAX
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-8], EBX
JMP LOOP_3
EXIT_3:
MOV EBX, [EBP-4]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP-8]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP-12]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP-16]
PUSH EBX
CALL print
POP EBX
PUSH DWORD 0
MOV EBX, 0
MOV [EBP-20], EBX
PUSH DWORD 0
MOV EBX, 1
MOV [EBP-24], EBX
PUSH DWORD 0
MOV EBX, 0
MOV [EBP-28], EBX
LOOP_6:
MOV EBX, [EBP-20]
NOT EBX
PUSH EBX
MOV EBX, [EBP-24]
POP EAX
AND EAX, EBX
MOV EBX, EAX
CMP EBX, False
JE EXIT_6
IF_4:
MOV EBX, [EBP-20]
PUSH EBX
MOV EBX, [EBP-24]
POP EAX
OR EAX, EBX
MOV EBX, EAX
CMP EBX, False
JE ENDIF_4
MOV EBX, [EBP-28]
PUSH EBX
MOV EBX, 1
POP EAX
ADD EAX, EBX
MOV EBX, EAX
MOV [EBP-28], EBX
ENDIF_4:
IF_5:
MOV EBX, [EBP-28]
PUSH EBX
MOV EBX, 5
POP EAX
CMP EAX, EBX
CALL binop_je
CMP EBX, False
JE ENDIF_5
MOV EBX, 1
MOV [EBP-20], EBX
MOV EBX, 0
MOV [EBP-24], EBX
ENDIF_5:
JMP LOOP_6
EXIT_6:
MOV EBX, [EBP-28]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP-20]
PUSH EBX
CALL print
POP EBX
MOV EBX, [EBP-24]
PUSH EBX
CALL print
POP EBX



; interrupcao de saida
   POP EBP
   MOV EAX, 1
    INT 0x80
