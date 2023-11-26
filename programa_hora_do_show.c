#include <stdio.h>
int main(void){
    /*PARAMETROS*/
    int x = 4;

    /*VARLIST*/
    int z = 0;
    
    /*COMANDOS*/
    for(int __i__ = 0; __i__ < x; __i__++){
	for(int __i__ = 0; __i__ < x; __i__++){
	z = z + x;
	}
	}

    /*SAIDA*/ 
    printf("SAIDA:\n\tz = %d\n", z);
    return 0;
}
    
