#include <cstdio>
#include <cstdlib>
#include <cstring>
#define QUEX_TYPE_CHARACTER char
#define QUEX_TYPE_TOKEN_WITH_NAMESPACE_ID  int
#define QUEX_OPTION_POST_CATEGORIZER
#include <quex/code_base/test_environment/default_configuration>
#include <quex/code_base/analyzer/PostCategorizer.i>

/* See: post-categorizer-common.c */
using namespace quex;
void post_categorizer_setup(QUEX_TYPE_POST_CATEGORIZER* me, int Seed);

int
main(int argc, char** argv)
{

    if( argc < 2 ) return -1;

    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Post Categorizer: Enter;\n");
        printf("CHOICES: 0, 1, 2, 3, 4, 5, 6;\n");
        return 0;
    }
    const int Start = atoi(argv[1]);
    QUEX_TYPE_POST_CATEGORIZER  pc;

    post_categorizer_setup(&pc, Start);

    QuexPostCategorizer_print_tree(pc.root, 0);
}
