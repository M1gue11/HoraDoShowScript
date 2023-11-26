from ply.lex import lex
from ply.yacc import yacc

# analisador lexico lex
reservados = ("RECEBA", "DEVOLVA", "HORADOSHOW", "AQUIACABOU", 
              "SE", "ENTAO", "SENAO", "FIMSE", "ENQUANTO",  "FACA", "FIMENQUANTO", "virgula", "igual", 
              "mais", "vezes", "menos", "maiorque", "menorque", "maiorouigualque", "dividido",
              "menorouigualque", "EXECUTE", "abrePa", "fechaPa", "ZERO", "comparacao", "PASSE", "int")

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

variaveis_declaradas = set()
def p_PROGRAM(regras):
    '''
    PROGRAM : RECEBA PARAMETROS DEVOLVA VARLIST HORADOSHOW CMDS AQUIACABOU  
    '''
    parametros = regras[2]
    varlist = regras[4].split(", ")
    print("parametros", parametros)
    print("REGRA 4", regras[4])
    print("variaveis declaradas", variaveis_declaradas)
    varlist_str_saida_formato = "".join([f"\\t{var} = %d\\n" for var in varlist])
    varlist_str_saida_args = "".join([f"{var}, " for var in varlist])
    # removendo caracteres indesejados
    varlist_str_saida_args = varlist_str_saida_args[:len(varlist_str_saida_args)-2]
    # removendo variaveis ja declaradas
    varlist_nao_declarado = list(set(varlist) - set(variaveis_declaradas))
    print("varlist nao declarado", varlist_nao_declarado)
    varlist_nao_declarado_str = ""
    if len(varlist_nao_declarado) == 1:
        varlist_nao_declarado_str = varlist_nao_declarado[0]
        variaveis_declaradas.add(varlist_nao_declarado[0])
        print("AQUI FOI")
    else:
        for i, var in enumerate(varlist_nao_declarado):
            variaveis_declaradas.add(var)
            if i == len(varlist_nao_declarado) -1:
                varlist_nao_declarado_str += var
            else:
                varlist_nao_declarado_str += f"{var}, "
    
    comandos = regras[6]
    regras[0] = f'''#include <stdio.h>
int main(void){{
    /*PARAMETROS*/
    int {parametros};

    /*VARLIST*/
    int {regras[4]};
    
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
    func = lambda var: var not in variaveis_declaradas
    variaveis_declaradas.add(regras[1])
    print("ADICIONEI")
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
        | PASSE
    '''
    tam = len(regras)
    if tam == 2:
        regras[0] = f"{regras[1]}"
    elif tam == 4:
        regras[0] = f"\t{regras[1]} {regras[2]} {regras[3]};"
    elif tam == 6:
        regras[0] = f"{regras[1]} {regras[2]} {regras[3]}\n{regras[4]}\n{regras[5]}"

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
with open("hora_do_show_teste.hds", "r") as arquivoLeitura:
    programa = arquivoLeitura.read()
result = parser.parse(programa)

with open("programa_hora_do_show.c", "w") as arquivoEscrita:
    print(result, file=arquivoEscrita)
print(result)
print(variaveis_declaradas)
print("Execução do programa: \n")