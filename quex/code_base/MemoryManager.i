/* -*- C++ -*- vim: set syntax=cpp: */
#ifndef __INCLUDE_GUARD_QUEX__CODE_BASE__MEMORY_MANAGER_I__
#define __INCLUDE_GUARD_QUEX__CODE_BASE__MEMORY_MANAGER_I__

#include <quex/code_base/definitions>
#include <quex/code_base/buffer/plain/BufferFiller_Plain>
#include <quex/code_base/buffer/converter/BufferFiller_Converter>
#if defined (QUEX_OPTION_ENABLE_ICU)
#   include <quex/code_base/buffer/converter/icu/Converter_ICU>
#endif
#if defined (QUEX_OPTION_ENABLE_ICONV)
#   include <quex/code_base/buffer/converter/iconv/Converter_IConv>
#endif

#include <quex/code_base/temporary_macros_on>
 
#if ! defined(__QUEX_SETTING_PLAIN_C)
namespace quex { 
#endif
    struct __QuexBufferFiller_tag;

    QUEX_INLINE QUEX_TYPE_CHARACTER*
    MemoryManager_BufferMemory_allocate(const size_t CharacterN)
    {
        return (QUEX_TYPE_CHARACTER*)__QUEX_ALLOCATE_MEMORY((size_t)(CharacterN * sizeof(QUEX_TYPE_CHARACTER)));
    }

    QUEX_INLINE void
    MemoryManager_BufferMemory_free(QUEX_TYPE_CHARACTER* memory)
    { if( memory != 0x0 ) __QUEX_FREE_MEMORY((uint8_t*)memory); }

    TEMPLATE_IN(InputHandleT) TEMPLATED(QuexBufferFiller_Plain)*
    MemoryManager_BufferFiller_Plain_allocate()
    {
        const size_t     MemorySize = sizeof(TEMPLATED(QuexBufferFiller_Plain));
        return (TEMPLATED(QuexBufferFiller_Plain)*)__QUEX_ALLOCATE_MEMORY(MemorySize);
    }

    TEMPLATE_IN(InputHandleT) void
    MemoryManager_BufferFiller_Plain_free(TEMPLATED(QuexBufferFiller_Plain)* memory)
    { if( memory != 0x0 ) __QUEX_FREE_MEMORY((uint8_t*)memory); }


    TEMPLATE_IN(InputHandleT) TEMPLATED(QuexBufferFiller_Converter)*
    MemoryManager_BufferFiller_Converter_allocate()
    {
        const size_t     MemorySize = sizeof(TEMPLATED(QuexBufferFiller_Converter));
        return (TEMPLATED(QuexBufferFiller_Converter)*)__QUEX_ALLOCATE_MEMORY(MemorySize);
    }

    TEMPLATE_IN(InputHandleT) void
    MemoryManager_BufferFiller_Converter_free(TEMPLATED(QuexBufferFiller_Converter)* memory)
    { if( memory != 0x0 ) __QUEX_FREE_MEMORY((uint8_t*)memory); }

    QUEX_INLINE uint8_t*
    MemoryManager_BufferFiller_RawBuffer_allocate(const size_t ByteN)
    { return __QUEX_ALLOCATE_MEMORY(ByteN); }

    QUEX_INLINE void
    MemoryManager_BufferFiller_RawBuffer_free(uint8_t* memory)
    { if( memory != 0x0 ) __QUEX_FREE_MEMORY(memory); }

#   if defined (QUEX_OPTION_ENABLE_ICONV)
    QUEX_INLINE QuexConverter_IConv*
    MemoryManager_Converter_IConv_allocate()
    {
        const size_t     MemorySize = sizeof(QuexConverter_IConv);
        return (QuexConverter_IConv*)__QUEX_ALLOCATE_MEMORY(MemorySize);
    }

    QUEX_INLINE void
    MemoryManager_Converter_IConv_free(QuexConverter_IConv* memory)
    { if( memory != 0x0 ) __QUEX_FREE_MEMORY((uint8_t*)memory); }
#   endif

#   if defined (QUEX_OPTION_ENABLE_ICU)
    QUEX_INLINE QuexConverter_ICU*
    MemoryManager_Converter_ICU_allocate()
    {
        const size_t     MemorySize = sizeof(QuexConverter_ICU);
        return (QuexConverter_ICU*)__QUEX_ALLOCATE_MEMORY(MemorySize);
    }

    QUEX_INLINE void
    MemoryManager_Converter_ICU_free(QuexConverter_ICU* memory)
    { if( memory != 0x0 ) __QUEX_FREE_MEMORY((uint8_t*)memory); }
#   endif

#   if defined(QUEX_OPTION_TOKEN_POLICY_QUEUE) || defined(QUEX_OPTION_TOKEN_POLICY_USERS_QUEUE)
    QUEX_INLINE size_t 
    MemoryManager_TokenArray_allocate(QUEX_TYPE_TOKEN** memory, size_t RequiredSize)
    {
        const size_t     MemorySize = sizeof(QUEX_TYPE_TOKEN) * RequiredSize;
        *memory = (QUEX_TYPE_TOKEN*)__QUEX_ALLOCATE_MEMORY(MemorySize);
        return RequiredSize;
    }
    QUEX_INLINE void 
    MemoryManager_TokenArray_free(QUEX_TYPE_TOKEN* memory, size_t Size)
    {
        { if( memory != 0x0 ) __QUEX_FREE_MEMORY((uint8_t*)memory); }
    }
#   endif

#   if defined (QUEX_OPTION_INCLUDE_STACK)
    /* NOTE: The macro 'QUEX_MACRO_STRING_CONCATINATE' is used to generate a function
     *       name. For example, if the macro CLASS_MEMENTO is defined as 'LexerMemento',
     *       then the macro call
     *
     *           QUEX_NAMER(MemoryManager_, CLASS_MEMENTO, _allocate)
     *
     *       generates the function name:
     *
     *           MemoryManager_LexerMemento_allocate
     *
     *       Results of C-Preprocessing can always be viewed with 'gcc -E'.
     *                                                                                    */
    QUEX_INLINE CLASS_MEMENTO*
    QUEX_NAMER(MemoryManager_, CLASS_MEMENTO, _allocate)()
    {
        const size_t     MemorySize = sizeof(CLASS_MEMENTO);
        return (CLASS_MEMENTO*)__QUEX_ALLOCATE_MEMORY(MemorySize);
    }

    QUEX_INLINE void
    QUEX_NAMER(MemoryManager_, CLASS_MEMENTO, _free)(CLASS_MEMENTO* memory)
    { if( memory != 0x0 ) __QUEX_FREE_MEMORY((uint8_t*)memory); }
#   endif


#if ! defined(__QUEX_SETTING_PLAIN_C)
} // namespace quex
#endif
 
#include <quex/code_base/temporary_macros_off>

#endif /* __INCLUDE_GUARD_QUEX__CODE_BASE__MEMORY_MANAGER_I__ */
