#include <quex/code_base/buffer/TEST/Buffer_test_common.i>

int
main(int argc, char** argv)
{
    if( cl_has(argc, argv, "--hwut-info") ) {
        printf("Move by Offset: Backward (BPC=%i);\n", sizeof(QUEX_TYPE_CHARACTER));
        printf("CHOICES:  1, 2, 3, 4, 5;\n");
        return 0;
    }
    if( argc == 1 ) {
        printf("Command line argument required.\n");
        return 0;
    }

    QuexBuffer           buffer;
    int                  memory_size   = 12;
    const size_t         StepSize      = atoi(argv[1]);

    assert(QUEX_SETTING_BUFFER_MIN_FALLBACK_N == 5);

    QuexBuffer_construct_wo_filler(&buffer, 0x0, memory_size);
    QuexBuffer_end_of_file_unset(&buffer);

    for(int i = 1; i < memory_size - 2 ; ++i) *(buffer._memory._front + i) = '0' + i;
    *(buffer._memory._back - 1) = '0';

    buffer._input_p = buffer._memory._back - 1;
    QuexBuffer_end_of_file_set(&buffer, buffer._memory._back);

    test_move_backward(&buffer, StepSize);
}
