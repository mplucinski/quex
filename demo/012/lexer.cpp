#include<cstdio> 

#include "moritz_Lexer"
#include "max_Lexer"
#include "boeck_Lexer"

using namespace std;


int 
main(int argc, char** argv) 
{        
    // we want to have error outputs in stdout, so that the unit test could see it.
    max::Lexer     max_lex("example-utf16.txt", "UTF16");
    max::Token     max_token;
    moritz::Lexer  moritz_lex("example-ucs2.txt", "UCS-2");
    moritz::Token  moritz_token;
    boeck::Lexer   boeck_lex("example-utf8.txt");
    boeck::Token   boeck_token;


    // Each lexer reads one token, since the grammars are similar the lexeme 
    // is always the same.                                                    
    printf("                Max:        Moritz:      Boeck:\n");

    do {
        max_lex.receive(&max_token);
        moritz_lex.receive(&moritz_token);
        boeck_lex.receive(&boeck_token);

        /* Lexeme is same for all three. */
        char* lexeme = (char*)max_token.utf8_text().c_str();
        int   L      = (int)std::strlen(lexeme);
        printf(lexeme);
        for(int i=0; i < 10 - L ; ++i) printf(" ");
        printf("\t");
        printf("%s   %s   %s\n", 
               max_token.type_id_name().c_str(), 
               moritz_token.type_id_name().c_str(), 
               boeck_token.type_id_name().c_str());

    } while( boeck_token.type_id() != TKN_TERMINATION );

    return 0;
}
