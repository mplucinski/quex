/* -*- C++ -*- vim: set syntax=cpp: */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__TEST__BUFFER_TEST_COMMON_I
#define __QUEX_INCLUDE_GUARD__BUFFER__TEST__BUFFER_TEST_COMMON_I

#include <quex/code_base/test_environment/TestAnalyzer-configuration>
#include <quex/code_base/buffer/Buffer.i>
#include <quex/code_base/buffer/BufferFiller.i>
#include <quex/code_base/MemoryManager>
#include <quex/code_base/buffer/Buffer_debug.i>
#include <quex/code_base/converter_helper/from-utf8.i>
#include <quex/code_base/converter_helper/from-utf16.i>
#include <quex/code_base/converter_helper/from-utf32.i>
#include <quex/code_base/converter_helper/from-unicode-buffer>
#include <quex/code_base/converter_helper/from-unicode-buffer.i>
#include <string.h>
#include <cstdio>

using namespace quex;
using namespace std;

inline int 
cl_has(int argc, char** argv, const char* What)
{ 
    /* Ensure, that asserts and exceptions are printed in the output for the unit test. 
     * This has nothing to do with the command line arguments, but its handled here at 
     * a central place, so every unit test passes by here.                             */
    stderr = stdout;

    return argc > 1 && strcmp(argv[1], What) == 0; 
}
#define QUEX_DEFINED_FUNC_cl_has

inline void
show_this(const char* Name, QUEX_NAME(Buffer)* buffer, QUEX_TYPE_CHARACTER* Pos, char Appendix)
{
    static uint8_t  utf8_char_str[7];
    uint8_t*        p = 0x0;
    QUEX_TYPE_CHARACTER UC = *Pos;

    if( UC == '\0' ) { 
        printf("%s= %i (--> '%c')%c", (char*)Name, (int)(Pos - buffer->_memory._front - 1), 
               (char)'\0', Appendix);

    } else if( UC == '\n' ) { 
        printf("%s= %i (--> '\\n')%c", (char*)Name, (int)(Pos - buffer->_memory._front - 1), 
               Appendix);
    } else {
        p = utf8_char_str;
        const QUEX_TYPE_CHARACTER* input_p = Pos;

        switch( sizeof(QUEX_TYPE_CHARACTER) ) {
        case 1:  quex::utf8_to_utf8_character((const uint8_t**)&input_p, &p); break;
        case 2:  quex::utf16_to_utf8_character((const uint16_t**)&input_p, &p); break;
        case 4:  quex::utf32_to_utf8_character((const uint32_t**)&input_p, &p); break;
        default: assert(false);
        }
        *p = '\0';
        printf("%s= %i (--> '%s')%c", 
               (char*)Name,
               (int)(Pos - buffer->_memory._front - 1), 
               (char*)utf8_char_str, 
               Appendix);
    }
}

inline void 
print_this(QUEX_NAME(Buffer)* buffer)
{

    show_this("input_p      ",      buffer, buffer->_input_p, '\t');
    show_this("lexeme start ", buffer, buffer->_lexeme_start_p, '\n');
}

inline void 
test_move_backward(QUEX_NAME(Buffer)* buffer, const size_t StepSize)
{
    print_this(buffer);
    while( buffer->_input_p != buffer->_memory._front + 1 ) {
        QUEX_NAME(Buffer_move_backward)(buffer, StepSize);
        print_this(buffer);
    }
    QUEX_NAME(Buffer_move_backward)(buffer, StepSize);
    print_this(buffer);
}

inline void 
test_move_forward(QUEX_NAME(Buffer)* buffer, size_t StepSize)
{
    print_this(buffer);
    while( ! (QUEX_NAME(Buffer_distance_input_to_text_end)(buffer) == 0 && 
              (buffer->filler == 0x0 || buffer->_memory._end_of_file_p != 0x0) ) ) {
        QUEX_NAME(Buffer_move_forward)(buffer, StepSize);
        print_this(buffer);
    }
    QUEX_NAME(Buffer_move_forward)(buffer, StepSize);
    print_this(buffer);
}

inline void 
test_seek_and_tell(QUEX_NAME(Buffer)* buffer, size_t* SeekIndices)
{
    /* NOTE: SeekIndices must be terminated by '999' */

    print_this(buffer);
    for(size_t* it = SeekIndices; *it != 999; ++it) {
        /**/
        printf("------------------------------\n");
        /**/
        printf("SEEK --> %i\n", (int)*it);
        QUEX_NAME(Buffer_seek)(buffer, *it);
        print_this(buffer);
        printf("TELL:    %i", (int)QUEX_NAME(Buffer_tell)(buffer));
        printf("\n");
    }
}

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__TEST__BUFFER_TEST_COMMON_I */
