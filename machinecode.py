import pprint

class MCGenerator:
    text = """
segment . data
res RESB 1
section .text
global_start
1
print : ; subrotina print
POP EBX
POP EAX
PUSH EBX
XOR ESI , ESI
print_dec :
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, '0 '
PUSH EDX
INC ESI
CMP EAX, 0
JZ print_next
JMP print_dec
print_next :
CMP ESI , 0
JZ print_exit
DEC ESI
MOV EAX, SYS_WRITE
MOV EBX, STDOUT
POP ECX
MOV [res] , ECX
MOV ECX, r e s
MOV EDX, 1
INT 0 x80
JMP print_next
print_exit :
RET
; subrotinas if / while
binop_ je :
JE binop_true
JMP bi n o p_ f al s e
binop_ jg :
JG binop_true
JMP bi n o p_ f al s e
binop_jl :
JL binop_true
JMP binop_false
binop_false :
MOV EBX, F al s e
JMP bin op_e xi t
binop_true :
MOV EBX, True
bin op_e xi t :
RET
_start:
;codigo gerado pelo compilador
    """
    

    consts = """
; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
    """

    bss = """ 
segment . bss ; variaveis
res RESB 1
    """
        

    data = """
segment . data
    """

    output = """
; interrupcao de saida
MOV EAX, 1
INT 0 x80
    """

    code = ""


    def print_nasm():
        pp = pprint.PrettyPrinter(indent=4)
        print(MCGenerator.consts+MCGenerator.data+MCGenerator.bss+\
                    MCGenerator.text+MCGenerator.code+MCGenerator.output)
    

    