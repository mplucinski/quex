#include<fstream>    
#include<iostream> 

// (*) include lexical analyser header
#include "ISLexer"
#include "ISLexer-token_ids"

using namespace std;

QUEX_TYPE_CHARACTER  EmptyLexeme = 0x0000;  /* Only the terminating zero */

void    print(quex::ISLexer& qlex, quex::Token& Token, bool TextF = false);
void    print(quex::ISLexer& qlex, const char* Str1, const char* Str2=0x0, const char* Str3=0x0);

#ifdef QUEX_OPTION_TOKEN_POLICY_USERS_QUEUE
     void get_token_from_users_queue(quex::ISLexer&, quex::Token&);
#    define RECEIVE(Token)   get_token_from_users_queue(qlex, Token)
#else
#    define RECEIVE(Token)   qlex.receive(&Token)
#endif

int 
main(int argc, char** argv) 
{        
    quex::Token       Token;

    if( argc < 2 ) {
        printf("Need at least one argument.\n");
        return -1;
    }
    else if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Include Stack: Misc Scenarios;\n");
        printf("CHOICES: empty, 1, 2, 3, 4, 5, 20;");
        return 0;
    }

    string         Directory("example/");
    string         Filename(argv[1]);
    ifstream       istr((Directory + Filename + ".txt").c_str());
    quex::ISLexer  qlex(&istr);

    qlex.file_name = Directory + Filename + ".txt";
    delete sh;
    cout << "[START]\n";

    do {
        RECEIVE(Token);

        print(qlex, Token, true);

    } while( Token.type_id() != QUEX_TKN_TERMINATION );

    cout << "[END]\n";

    return 0;
}

string  space(int N)
{ string tmp; for(int i=0; i<N; ++i) tmp += "    "; return tmp; }

void  print(quex::ISLexer& qlex, quex::Token& Token, bool TextF /* = false */)
{ 
    cout << space(qlex.include_depth) << Token.line_number() << ": (" << Token.column_number() << ")";
    cout << Token.type_id_name();
    if( TextF ) cout << "\t'" << Token.text().c_str() << "'";
    cout << endl;
}

void print(quex::ISLexer& qlex, const char* Str1, const char* Str2 /* = 0x0 */, const char* Str3 /* = 0x0*/)
{
    cout << space(qlex.include_depth) << Str1;
    if( Str2 != 0x0 ) cout << Str2;
    if( Str3 != 0x0 ) cout << Str3;
    cout << endl;
}

#ifdef QUEX_OPTION_TOKEN_POLICY_USERS_QUEUE
void get_token_from_users_queue(quex::ISLexer& qlex, quex::Token& Token)
{
    static quex::Token   Begin[3];
    static quex::Token*  End  = Begin + 3;
    
    if( QuexTokenQueue_is_empty(qlex._token_queue) ) {
        qlex.receive(Begin, End);
    }
    Token = *qlex._token_queue.read_iterator++;
}
#endif
