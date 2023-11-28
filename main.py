from ply.lex import lex
from ply.yacc import yacc
import re

# Integrantes: Bruno Pimenta (2110717) e Miguel Angelus (2120640)

# analisador lexico lex
reservados = ("RECEBA", "DEVOLVA", "HORADOSHOW", "AQUIACABOU", 
              "SE", "ENTAO", "SENAO", "FIMSE", "ENQUANTO",  "FACA", "FIMENQUANTO", "virgula", "igual", 
              "mais", "vezes", "menos", "maiorque", "menorque", "maiorouigualque", "dividido",
              "menorouigualque", "EXECUTE", "abrePa", "fechaPa", "ZERO", "comparacao", "int")

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

variaveis_declaradas = set()
def p_PROGRAM(regras):
    '''
    PROGRAM : RECEBA PARAMETROS DEVOLVA VARLIST HORADOSHOW CMDS AQUIACABOU  
    '''
    parametros = regras[2]
    var_parametros = list(filter(lambda x: re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', x), parametros.split()))
    varlist = regras[4].split(", ")
    varlist_str_saida_formato = "".join([f"\\t{var} = %d\\n" for var in varlist])
    varlist_str_saida_args = "".join([f"{var}, " for var in varlist])
    # removendo caracteres indesejados
    varlist_str_saida_args = varlist_str_saida_args[:len(varlist_str_saida_args)-2]
    # removendo variaveis ja declaradas
    varlist_nao_declarado = list(set(varlist) - set(var_parametros))
    varlist_nao_declarado_str = ""
    if len(varlist_nao_declarado) == 1:
        varlist_nao_declarado_str = varlist_nao_declarado[0] + " = 0"
    else:
        for i, var in enumerate(varlist_nao_declarado):
            variaveis_declaradas.add(var)
            if i == len(varlist_nao_declarado) -1:
                varlist_nao_declarado_str += f"{var} = 0"
            else:
                varlist_nao_declarado_str += f"{var} = 0, "
    
    comandos = regras[6].replace("\t", "", 1)
    print("OI", varlist_nao_declarado_str)
    regras[0] = f'''#include <stdio.h>
int main(void){{
    /*PARAMETROS*/
    int {parametros};

    /*VARLIST*/
    {f"int {varlist_nao_declarado_str};" if varlist_nao_declarado_str else ""}
    
    /*COMANDOS*/
    {comandos}

    /*SAIDA*/ 
    printf("SAIDA:\\n{varlist_str_saida_formato}", {varlist_str_saida_args});
    return 0;
}}
    '''

def p_VARLIST(regras):
    '''
    VARLIST : variavel virgula VARLIST
            | variavel
    '''
    # func = lambda var: var not in variaveis_declaradas
    if regras[1] not in variaveis_declaradas:
        variaveis_declaradas.add(regras[1])
    if len(regras) == 2:
        regras[0] = f"{regras[1]}"
    else:
        regras[0] = f"{regras[1]}{regras[2]} {regras[3]}"


def p_VARIAVEL(regras):
    '''
    VARIAVEL : variavel
    '''
    if regras[1] not in variaveis_declaradas:
        variaveis_declaradas.add(regras[1])
        regras[0] = f"int {regras[1]}"
    else:
        regras[0] = f"{regras[1]}"

def p_VARIAVELOUEXPRESSAO(regras):
    '''
    VARIAVELOUEXPRESSAO : VARIAVEL
                        | EXPRESSAO
    '''
    regras[0] = f"{regras[1]}"

def p_VARIAVELOUNUMERO(regras):
    '''
    VARIAVELOUNUMERO : VARIAVEL
                     | numero
    '''
    regras[0] = f"{regras[1]}"
    
def p_PARAMETROS(regras):
    '''
    PARAMETROS : variavel igual numero virgula PARAMETROS
               | variavel igual numero 
    '''
    tam = len(regras)
    variaveis_declaradas.add(regras[1])
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

def p_CMD(regras):
    '''
    CMD : VARIAVEL igual variavel
        | VARIAVEL igual numero
        | VARIAVEL igual OPERACAO
        | ENQUANTO VARIAVELOUEXPRESSAO FACA CMDS FIMENQUANTO
        | FUNCAO
        | CONDICIONAL
    '''
    tam = len(regras)
    if tam == 2:
        regras[0] = f"{regras[1]}"
    elif tam == 4:
        regras[0] = f"\t{regras[1]} {regras[2]} {regras[3]};"
    elif tam == 6:
        regras[0] = f'''\twhile({regras[2]}){{\n{regras[4]}\n\t}}'''

def p_OPERACAO(regras):
    '''
    OPERACAO : VARIAVELOUNUMERO mais VARIAVELOUNUMERO
             | VARIAVELOUNUMERO vezes VARIAVELOUNUMERO
             | VARIAVELOUNUMERO menos VARIAVELOUNUMERO
             | VARIAVELOUNUMERO dividido VARIAVELOUNUMERO
    '''
    regras[0] = f"{regras[1]} {regras[2]} {regras[3]}"

def p_EXPRESSAO(regras):
    '''
    EXPRESSAO : VARIAVELOUNUMERO maiorque VARIAVELOUNUMERO
             | VARIAVELOUNUMERO menorque VARIAVELOUNUMERO
             | VARIAVELOUNUMERO maiorouigualque VARIAVELOUNUMERO
             | VARIAVELOUNUMERO menorouigualque VARIAVELOUNUMERO
             | VARIAVELOUNUMERO comparacao VARIAVELOUNUMERO

    '''
    regras[0] = f"{regras[1]} {regras[2]} {regras[3]}"

def p_FUNCAO(regras):
    '''
    FUNCAO : ZERO abrePa variavel fechaPa 
           | EXECUTE abrePa VARIAVELOUNUMERO virgula CMDS fechaPa
    '''
    tam = len(regras)
    if tam == 5:
        regras[0] = f"\t{regras[3]} = 0;"
    elif tam == 7:
        regras[0] = f"\tfor(int __i__ = 0; __i__ < {regras[3]}; __i__++){{\n{regras[5]}\n\t}}"

def p_CONDICIONAL(regras):
    '''
    CONDICIONAL : SE VARIAVELOUEXPRESSAO ENTAO CMDS FIMSE
                | SE VARIAVELOUEXPRESSAO ENTAO CMDS SENAO CMDS FIMSE
    '''
    tam = len(regras)
    if tam == 6:
        regras[0] = f"\tif({regras[2]}){{\n{regras[4]}\n\t}}"
    elif tam == 8:
        regras[0] = f"\tif({regras[2]}){{\n{regras[4]}\n\t}}\n\telse{{\n{regras[6]}\n\t}}"

def p_error(regras):
    print("Erro de sintaxe"+ str(regras))

parser = yacc(debug=True) # construção do parser
with open("hora_do_show_teste.hds", "r") as arquivoLeitura:
    programa = arquivoLeitura.read()


result = parser.parse(programa)
if result == None:
    print("ERRO!")
    exit(-1)

with open("programa_hora_do_show.c", "w") as arquivoEscrita:
    print(result, file=arquivoEscrita)
print(variaveis_declaradas)
print("Execução do programa: \n")