from ply.lex import lex
from ply.yacc import yacc

# analisador lexico lex
reservados = ("RECEBA", "DEVOLVA", "HORADOSHOW", "AQUIACABOU", 
              "SE", "FACA", "ENQUANTO", "FIM", "virgula", "igual", 
              "mais", "vezes", "menos", "maiorque", "menorque",
              "maiorouigualque", "menorouigualque")

t_RECEBA = r'RECEBA'
t_DEVOLVA = r'DEVOLVA'
t_HORADOSHOW = r'HORADOSHOW'
t_AQUIACABOU = r'AQUIACABOU'
t_SE = r'SE'
t_FACA = r'FACA'
t_ENQUANTO = r'ENQUANTO'
t_FIM = r'FIM'
t_virgula = r','
t_igual = r'='
t_menos = r'\-'
t_mais = r'\+'
t_vezes = r'\*'
t_maiorque = r'>'
t_menorque = r'<'
t_maiorouigualque = r'>='
t_menorouigualque = r'<='

def t_variavel(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reservados: # igual
        t.type = t.value
    return t

def t_numero(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n' # ignora espaços e tabs

def t_error(t): # nos dizer qual caractere ilegal e se tem erro
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)

tokens = reservados + ("variavel", "numero")

lexer = lex(debug=True) # construção do lexer


# analisador sintatico Yacc

def p_PROGRAM(regras):
    '''
    PROGRAM : RECEBA VARLIST DEVOLVA VARLIST HORADOSHOW CMDS AQUIACABOU
        
    '''
    regras[0] = f"{regras[1]} {regras[2]} {regras[3]} {regras[4]}\n{regras[5]}\n{regras[6]}\n{regras[7]}"

def p_VARLIST(regras):
    '''
    VARLIST : variavel virgula VARLIST 
            | variavel
    '''

    if len(regras) == 2:
        regras[0] = f"{regras[1]}"
    else:
        regras[0] = f"{regras[1]}{regras[2]} {regras[3]}"

def p_CMDS(regras):
    '''
    CMDS : CMD CMDS 
         | CMD
    '''
    if len(regras) == 2:
        regras[0] = f"{regras[1]}"
    else:
        regras[0] = f"{regras[1]}\n{regras[2]}"

def p_OPERACAO(regras):
    '''
    OPERACAO : variavel mais variavel
             | variavel mais numero
             | numero mais variavel
             | numero mais numero
             | variavel vezes variavel
             | variavel vezes numero
             | numero vezes variavel
             | numero vezes numero
             | variavel menos variavel
             | variavel menos numero
             | numero menos variavel
             | numero menos numero
    '''
    regras[0] = f"{regras[1]} {regras[2]} {regras[3]} "

def p_EXPRESSAO(regras):
    '''
    EXPRESSAO : variavel maiorque variavel
             | variavel maiorque numero
             | numero maiorque variavel

             | variavel menorque variavel
             | variavel menorque numero
             | numero menorque variavel

             | variavel maiorouigualque variavel
             | variavel maiorouigualque numero
             | numero maiorouigualque variavel

             | variavel menorouigualque variavel
             | variavel menorouigualque numero
             | numero menorouigualque variavel
    '''
    if len(regras) == 2:
        regras[0] = regras[1]
    else:
        regras[0] = f"{regras[1]} {regras[2]}"

def p_CMD(regras):
    '''
    CMD : variavel igual variavel
        | variavel igual numero 
        | variavel igual OPERACAO
        | ENQUANTO variavel FACA CMDS FIM
        | ENQUANTO EXPRESSAO FACA CMDS FIM
    '''
    tam = len(regras)
    if tam == 4:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}"
    elif tam == 6:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}\n{regras[4]}\n{regras[5]}"

def p_error(regras):
    print("Erro de sintaxe"+ str(regras))

parser = yacc(debug=True) # construção do parser
result = parser.parse(
    '''
        RECEBA v1 DEVOLVA v2, v3 
        HORADOSHOW 
        ENQUANTO miguel > v3 FACA v1 = v1 + 1 FIM
        AQUIACABOU
    '''
) # execução do parser

print(result)