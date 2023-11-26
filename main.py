from ply.lex import lex
from ply.yacc import yacc

# analisador lexico lex
reservados = ("RECEBA", "DEVOLVA", "HORADOSHOW", "AQUIACABOU", 
              "SE", "ENTAO", "SENAO", "FIMSE", "ENQUANTO",  "FACA", "FIMENQUANTO", "virgula", "igual", 
              "mais", "vezes", "menos", "maiorque", "menorque", "maiorouigualque", "dividido",
              "menorouigualque", "EXECUTE", "abrePa", "fechaPa", "ZERO", "comparacao", "PASSE")

t_RECEBA = r'RECEBA'
t_DEVOLVA = r'DEVOLVA'
t_HORADOSHOW = r'HORADOSHOW'
t_AQUIACABOU = r'AQUIACABOU'
t_FACA = r'FACA'
t_ENQUANTO = r'ENQUANTO'
t_FIMENQUANTO = r'FIMENQUANTO'
t_virgula = r','
t_igual = r'='
t_menos = r'\-'
t_mais = r'\+'
t_vezes = r'\*'
t_dividido = r'\/'
t_maiorque = r'>'
t_menorque = r'<'
t_maiorouigualque = r'>='
t_menorouigualque = r'<='
t_EXECUTE = r'EXECUTE'
t_abrePa = r'\('
t_fechaPa = r'\)'
t_ZERO = r'ZERO'
t_SE = r'SE'
t_ENTAO = r'ENTAO'
t_SENAO = r'SENAO'
t_FIMSE = r'FIMSE'
t_comparacao = r'=='
t_PASSE = r'PASSE'


def t_variavel(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reservados:
        t.type = t.value
    return t

def t_numero(t):
    r'[+-]?\d+(\.\d+)?'
    # t.value = int(t.value)
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
    PROGRAM : RECEBA PARAMETROS DEVOLVA VARLIST HORADOSHOW CMDS AQUIACABOU  
    '''
    regras[0] = f"{regras[1]} {regras[2]} {regras[3]} {regras[4]}\n{regras[5]}\n{regras[6]}\n{regras[7]}"

def p_VARIAVELOUEXPRESSAO(regras):
    '''
    VARIAVELOUEXPRESSAO : variavel
                        | EXPRESSAO
    '''
    regras[0] = f"{regras[1]}"

def p_VARIAVELOUNUMERO(regras):
    '''
    VARIAVELOUNUMERO : variavel
                     | numero
    '''
    regras[0] = f"{regras[1]}"

def p_VARLIST(regras):
    '''
    VARLIST : variavel virgula VARLIST
            | variavel
    '''
    if len(regras) == 2:
        regras[0] = f"{regras[1]}"
    else:
        regras[0] = f"{regras[1]}{regras[2]} {regras[3]}"
    
def p_PARAMETROS(regras):
    '''
    PARAMETROS : variavel igual numero virgula PARAMETROS
               | variavel igual numero 
    '''
    tam = len(regras)
    if tam == 4:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}"
    else:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}{regras[4]} {regras[5]}"


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
    OPERACAO : VARIAVELOUNUMERO mais VARIAVELOUNUMERO
             | VARIAVELOUNUMERO vezes VARIAVELOUNUMERO
             | VARIAVELOUNUMERO menos VARIAVELOUNUMERO
             | VARIAVELOUNUMERO dividido VARIAVELOUNUMERO
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

             | numero comparacao variavel
             | numero comparacao numero

    '''
    regras[0] = f"{regras[1]} {regras[2]} {regras[3]}"

def p_CMD(regras):
    '''
    CMD : variavel igual variavel
        | variavel igual numero
        | variavel igual OPERACAO
        | ENQUANTO variavel FACA CMDS FIMENQUANTO
        | ENQUANTO EXPRESSAO FACA CMDS FIMENQUANTO
        | FUNCAO
        | CONDICIONAL
        | PASSE
    '''
    tam = len(regras)
    if tam == 2:
        regras[0] = f"{regras[1]}"
    elif tam == 4:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}"
    elif tam == 6:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}\n{regras[4]}\n{regras[5]}"

def p_FUNCAO(regras):
    '''
    FUNCAO : EXECUTE abrePa VARIAVELOUNUMERO virgula CMDS fechaPa
           | ZERO abrePa variavel fechaPa
    '''
    tam = len(regras)
    if tam == 5:
        regras[0] = f"{regras[1]}{regras[2]}{regras[3]}{regras[4]}"
    else:
        regras[0] = f"{regras[1]}{regras[2]}{regras[3]}{regras[4]} {regras[5]}{regras[6]}"

def p_CONDICIONAL(regras):
    '''
    CONDICIONAL : SE VARIAVELOUEXPRESSAO ENTAO CMDS FIMSE
                | SE VARIAVELOUEXPRESSAO ENTAO CMDS SENAO CMDS FIMSE
    '''
    tam = len(regras)
    if tam == 6:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}\n{regras[4]}\n{regras[5]}"
    else:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}\n{regras[4]}\n{regras[5]}\n{regras[6]}\n{regras[7]}"

def p_error(regras):
    print("Erro de sintaxe"+ str(regras))

parser = yacc(debug=True) # construção do parser
result = parser.parse(
    '''
        RECEBA X = 2, Y = 3 
        DEVOLVA Z
        HORADOSHOW
        ZERO(X)
        SE z <= x ENTAO
        miguel = -5.8 / z
        EXECUTE(hk, z = z - 1)
        FIMSE
        ENQUANTO z FACA
        PASSE
        FIMENQUANTO
        Z=Y
        AQUIACABOU
    '''
) # execução do parser

print(result)