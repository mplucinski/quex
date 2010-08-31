#include <cstdio>
#include <cstdlib>
#include <cstring>
#define QUEX_TYPE_CHARACTER char
#define QUEX_TYPE_TOKEN_ID  int
#define QUEX_OPTION_POST_CATEGORIZER
#include <quex/code_base/test_environment/TestAnalyzer-configuration>
#include <quex/code_base/analyzer/PostCategorizer.i>
#include <quex/code_base/aux-string.i>

using namespace quex;
void post_categorizer_setup(QUEX_NAME(Dictionary)* me, int Seed);
void test(quex::QUEX_NAME(Dictionary)* pc, const char* Name);

int
main(int argc, char** argv)
{
    using namespace quex;

    if( argc < 2 ) return -1;

    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Post Categorizer: Remove Total;\n");
        printf("CHOICES: 1, 2, 3, 4, 5, 6, 7;\n");
        printf("SAME;\n");
        return 0;
    }
    QUEX_NAME(Dictionary)  pc;

    post_categorizer_setup(&pc, atoi(argv[1]));
    
    pc.remove("Ab");
    pc.remove("Ad");
    pc.remove("Af");
    pc.remove("Ah");
    pc.remove("Bb");
    pc.remove("Bd");
    pc.remove("Bf");

    pc.enter("The only node", 77);

    QUEX_NAME(PostCategorizer_print_this)(&pc);
}
