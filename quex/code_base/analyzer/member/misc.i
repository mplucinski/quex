/* -*- C++ -*-   vim: set syntax=cpp:
 *
 * No include guards, the header might be included from multiple lexers.
 *
 * NOT: #ifndef __INCLUDE_GUARD__QUEX_LEXER_CLASS_MISC_I__
 * NOT: #define __INCLUDE_GUARD__QUEX_LEXER_CLASS_MISC_I__       */

QUEX_NAMESPACE_COMPONENTS_OPEN

QUEX_INLINE void    
QUEX_MEMFUNC(ANALYZER, move_forward)(const size_t CharacterN)
{
    QuexBuffer_move_forward(&this->base.buffer, CharacterN);
}

QUEX_INLINE void    
QUEX_MEMFUNC(ANALYZER, move_backward)(const size_t CharacterN)
{
    QuexBuffer_move_backward(&this->base.buffer, CharacterN);
}


QUEX_INLINE size_t  
QUEX_MEMFUNC(ANALYZER, tell)()
{
    return QuexBuffer_tell(&this->base.buffer);
}

QUEX_INLINE void    
QUEX_MEMFUNC(ANALYZER, seek)(const size_t CharacterIndex)
{
    QuexBuffer_seek(&this->base.buffer, CharacterIndex);
}

QUEX_INLINE QUEX_TYPE_TOKEN*  
QUEX_MEMFUNC(ANALYZER, token_object)()
{
#   define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)this)
    return __QUEX_CURRENT_TOKEN_P;
#   undef self
}

QUEX_INLINE const char* 
QUEX_MEMFUNC(ANALYZER, version)() const
{ 
return          QUEX_STRING(QUEX_TYPE_ANALYZER)           \
       ": Version "         QUEX_SETTING_ANALYZER_VERSION \
       ". Date "            QUEX_SETTING_BUILD_DATE       \
       "Generated by Quex " QUEX_SETTING_VERSION ".";
}

QUEX_INLINE void
QUEX_MEMFUNC(ANALYZER, print_this)()
{
    __QUEX_STD_printf("   CurrentMode = %s;\n", base.__current_mode_p == 0x0 ? "0x0" : 
                                                                               base.__current_mode_p->name);

    QuexBuffer_print_this(&this->base.buffer);

#   ifdef QUEX_OPTION_STRING_ACCUMULATOR
    accumulator.print_this();
#   endif
#   ifdef __QUEX_OPTION_COUNTER
    QUEX_FIX(COUNTER, _print_this)(&counter);
#   endif
#   ifdef QUEX_OPTION_POST_CATEGORIZER
    post_categorizer.print_this();
#   endif
    __QUEX_STD_printf("   Mode Stack (%i/%i) = [", 
                      (int)(_mode_stack.end        - _mode_stack.begin),
                      (int)(_mode_stack.memory_end - _mode_stack.begin));
    for(QUEX_TYPE_MODE** iterator=_mode_stack.end-1; iterator >= _mode_stack.begin; --iterator)
        __QUEX_STD_printf("%s, ", (*iterator)->name);

    __QUEX_STD_printf("]\n");
    __QUEX_STD_printf("   ByteOrderInversion = %s;\n", byte_order_reversion() ? "true" : "false");
}

QUEX_INLINE bool
QUEX_MEMFUNC(ANALYZER, byte_order_reversion)()
{ return base.buffer._byte_order_reversion_active_f; }

QUEX_INLINE void     
QUEX_MEMFUNC(ANALYZER, byte_order_reversion_set)(bool Value)
{ base.buffer._byte_order_reversion_active_f = Value; }

QUEX_NAMESPACE_COMPONENTS_CLOSE
