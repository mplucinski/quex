#include <stdio.h> 

#include "moritz_Lexer"
#include "moritz_Lexer-token.i"
#include "max_Lexer"
#include "max_Lexer-token.i"
#include "boeck_Lexer"
#include "boeck_Lexer-token.i"

int 
main(int argc, char** argv) 
{        
    /* we want to have error outputs in stdout, so that the unit test could see it.  */
    max_Lexer     max_lex;
    moritz_Lexer  moritz_lex;
    boeck_Lexer   boeck_lex;
    max_Token*    max_token    = 0x0;
    moritz_Token* moritz_token = 0x0;
    boeck_Token*  boeck_token  = 0x0;

    const size_t BufferSize = 1024;
    char         buffer[1024];
    char*        iterator = 0x0;
    size_t       i = 0;

    max_Lexer_construct_file_name(&max_lex,       "example-utf16.txt", "UTF16", false);
    moritz_Lexer_construct_file_name(&moritz_lex, "example-ucs2.txt",  "UCS-2", false);
    boeck_Lexer_construct_file_name(&boeck_lex,   "example-utf8.txt",  0x0,     false);

    /* Each lexer reads one token, since the grammars are similar the lexeme 
     * is always the same.                                                           */
    printf("                Max:        Moritz:      Boeck:\n");

    max_token    = max_Lexer_token_p(&max_lex);
    moritz_token = moritz_Lexer_token_p(&moritz_lex);
    boeck_token  = boeck_Lexer_token_p(&boeck_lex);

    do {
        (void)max_Lexer_receive(&max_lex);
        (void)moritz_Lexer_receive(&moritz_lex);
        (void)boeck_Lexer_receive(&boeck_lex);

        /* Lexeme is same for all three. */
        iterator = (char*)boeck_Lexer_utf8_to_utf8_string(boeck_token->text, 
                                                          boeck_Lexer_strlen(boeck_token->text),
                                                          (uint8_t*)buffer,
                                                          BufferSize);
        *iterator = '\0';
        const char* lexeme = (const char*)buffer;
        size_t      preL   = (size_t)strlen(lexeme);
        size_t      L      = preL < 10 ? preL : 10;
        printf("%s", lexeme);

        for(i=0; i < 10 - L ; ++i) printf(" ");

        printf("\t");
        printf("%s   %s   %s\n", 
               max_Token_map_id_to_name(max_token->_id),
               moritz_Token_map_id_to_name(moritz_token->_id),
               boeck_Token_map_id_to_name(boeck_token->_id));

    } while( boeck_token->_id != TKN_TERMINATION );

    return 0;
}
