#include <stdio.h>

#include "tiny_lexer"
#include "tiny_lexer-token.i"
#include "messaging-framework.h"

int 
main(int argc, char** argv) 
{        
    QUEX_TYPE_TOKEN    token;
    tiny_lexer         qlex;
    size_t             BufferSize = 1024;
    char               buffer[1024];
    size_t             receive_n = (size_t)-1;
    int                i = 0;

    QUEX_NAME_TOKEN(construct)(&token);
    QUEX_NAME(construct_memory)(&qlex, 
                                MESSAGING_FRAMEWORK_BUFFER, 
                                MESSAGING_FRAMEWORK_BUFFER_SIZE, 
                                MESSAGING_FRAMEWORK_BUFFER + 1, 
                                0x0, false);


    /* Iterate 3 times doing the same thing in order to illustrate
     * the repeated activation of the same chunk of memory.        */
    for(i = 0; i < 3; ++i ) {
        /* -- Call the low lever driver to fill the fill region */
        receive_n = messaging_framework_receive_to_internal_buffer();

        /* -- Inform the buffer about the number of loaded characters NOT NUMBER OF BYTES! */
        QUEX_NAME(buffer_fill_region_finish)(&qlex, receive_n-1);
        /* -- Each time the buffer is filled, the input pointer must be reset
         *    (Here, it is just to display the principle, ...)                */
        QUEX_NAME(buffer_input_pointer_set)(&qlex, MESSAGING_FRAMEWORK_BUFFER + 1);

        /* -- Loop until the 'termination' token arrives                      */
        QUEX_NAME(token_p_switch)(&qlex, &token);
        do {
            QUEX_NAME(receive)(&qlex);

            if( token._id != QUEX_TKN_TERMINATION )
                printf("Consider: %s \n", QUEX_NAME_TOKEN(get_utf8_string)(&token, buffer, BufferSize));

            if( token._id == QUEX_TKN_BYE ) 
                printf("##\n");
            
        } while( token._id != QUEX_TKN_TERMINATION );
    }

    QUEX_NAME(destruct)(&qlex);
    QUEX_NAME_TOKEN(destruct)(&token);
    return 0;
}

