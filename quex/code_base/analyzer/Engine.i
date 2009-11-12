/* -*- C++ -*- vim: set syntax=cpp: */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__ANALYSER_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__ANALYSER_I

#include <quex/code_base/definitions>
#include <quex/code_base/buffer/Buffer>
#include <quex/code_base/buffer/asserts>

#include <quex/code_base/temporary_macros_on>

QUEX_NAMESPACE_MAIN_OPEN

    TEMPLATE_IN(InputHandleT) void
    QUEX_NAME(Engine_construct)(QUEX_NAME(Engine)* me,
                                QUEX_NAME(AnalyzerFunctionP)  AnalyserFunction,
                                InputHandleT*                input_handle,
                                QUEX_TYPE_CHARACTER*         InputMemory,
                                const size_t                 BufferMemorySize,
                                const char*                  CharacterEncodingName, 
                                const size_t                 TranslationBufferMemorySize,
                                bool                         ByteOrderReversionF)
    /* input_handle == 0x0 means that there is no stream/file to read from. Instead, the 
     *                     user intends to perform the lexical analysis directly on plain
     *                     memory. In this case, the user needs to call the following function
     *                     by hand in order to setup the memory:
     *
     *                     QuexBufferMemory_construct(analyse->buffer._memory, (uint8_t*)MyMemoryP, MyMemorySize); 
     */
    {
#       ifdef QUEX_OPTION_ASSERTS
        /* Initialize everything to 0xFF which is most probably causing an error
         * if a member variable is not initialized before it is used.             */
        __QUEX_STD_memset((uint8_t*)&me->buffer, 0xFF, sizeof(me->buffer));
#       endif

        QUEX_NAME(Buffer_construct)(&me->buffer, input_handle, InputMemory, BufferMemorySize,
                                    CharacterEncodingName, TranslationBufferMemorySize,
                                    ByteOrderReversionF);

        me->current_analyzer_function = AnalyserFunction;

        /* Double check that everything is setup propperly. */
        QUEX_BUFFER_ASSERT_CONSISTENCY(&me->buffer);
        __quex_assert(me->buffer._input_p == me->buffer._memory._front + 1);
    }


    QUEX_INLINE void
    QUEX_NAME(Engine_destruct)(QUEX_NAME(Engine)* me)
    {
        QUEX_NAME(Buffer_destruct)(&me->buffer);
    }

    TEMPLATE_IN(InputHandleT) void
    QUEX_NAME(Engine_reset)(QUEX_NAME(Engine)*           me,
                            QUEX_NAME(AnalyzerFunctionP) AnalyserFunction,
                            InputHandleT*                input_handle, 
                            const char*                  CharacterEncodingName, 
                            const size_t                 TranslationBufferMemorySize)
    {
        me->current_analyzer_function = AnalyserFunction;

        QUEX_NAME(Buffer_reset)(&me->buffer, input_handle, CharacterEncodingName, TranslationBufferMemorySize);

        /* Double check that everything is setup propperly. */
        QUEX_BUFFER_ASSERT_CONSISTENCY(&me->buffer);
        __quex_assert(me->buffer._input_p == me->buffer._memory._front + 1);
    }

    /* NOTE: 'reload_forward()' needs to be implemented for each mode, because
     *       addresses related to acceptance positions need to be adapted. This
     *       is not the case for 'reload_backward()'. In no case of backward
     *       reloading, there are important addresses to keep track. */
    QUEX_INLINE bool 
    QUEX_NAME(Engine_buffer_reload_backward)(QUEX_NAME(Buffer)* buffer)
    {
        if( buffer->filler == 0x0 ) return false;

        const size_t LoadedCharacterN = QUEX_NAME(BufferFiller_load_backward)(buffer);
        if( LoadedCharacterN == 0 ) return false;
        
        /* Backward lexing happens in two cases:
         *
         *  (1) When checking for a pre-condition. In this case, no dedicated acceptance
         *      is involved. No acceptance positions are considered.
         *  (2) When tracing back to get the end of a core pattern in pseudo-ambigous
         *      post conditions. Then, no acceptance positions are involved, because
         *      the start of the lexeme shall not drop before the begin of the buffer 
         *      and the end of the core pattern, is of course, after the start of the 
         *      lexeme. => there will be no reload backwards.                            */
        return true;
    }

    QUEX_INLINE bool 
    QUEX_NAME(Engine_buffer_reload_forward)(QUEX_NAME(Buffer)* buffer, 
                                            QUEX_TYPE_CHARACTER_POSITION* last_acceptance_input_position,
                                            QUEX_TYPE_CHARACTER_POSITION* post_context_start_position,
                                            const size_t                  PostContextN)
    {
        QUEX_TYPE_CHARACTER_POSITION* iterator = 0x0;
        QUEX_TYPE_CHARACTER_POSITION* End = post_context_start_position + PostContextN;

        if( buffer->filler == 0x0 ) return false;
        if( buffer->_memory._end_of_file_p != 0x0 ) return false;
        const size_t LoadedCharacterN = QUEX_NAME(BufferFiller_load_forward)(buffer);
        if( LoadedCharacterN == 0 ) return false;

        if( *last_acceptance_input_position != 0x0 ) { 
            *last_acceptance_input_position -= LoadedCharacterN;
        }                                                                  
        for(iterator = post_context_start_position; iterator != End; ++iterator) {
            /* NOTE: When the post_context_start_position is still undefined the following operation may
             *       underflow. But, do not care, once it is **assigned** to a meaningful value, it won't */
            *iterator -= LoadedCharacterN;
        }
                                                                              
        return true;
    }


QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/temporary_macros_off>

#include <quex/code_base/buffer/Buffer.i>
#include <quex/code_base/buffer/BufferFiller.i>

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__ANALYSER_I */