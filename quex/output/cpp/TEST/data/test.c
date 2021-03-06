#include <data/check.h>

#ifdef __QUEX_OPTION_COUNTER
void
QUEX_NAME(TEST_MODE_counter)(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_CHARACTER* LexemeBegin, QUEX_TYPE_CHARACTER* LexemeEnd)
{
#   define self (*me)
/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */
#   define QUEX_LABEL_STATE_ROUTER _42
    QUEX_TYPE_CHARACTER            input                          = (QUEX_TYPE_CHARACTER)(0x00);
    QUEX_TYPE_GOTO_LABEL           target_state_else_index        = QUEX_GOTO_LABEL_VOID;
    QUEX_TYPE_GOTO_LABEL           target_state_index             = QUEX_GOTO_LABEL_VOID;
    QUEX_TYPE_CHARACTER_POSITION   character_begin_p              = (QUEX_TYPE_CHARACTER_POSITION)0x0;
    (void)me;
    __QUEX_IF_COUNT_SHIFT_VALUES();
    /* Allow LexemeBegin == LexemeEnd (e.g. END_OF_STREAM)
     * => Caller does not need to check
     * BUT, if so quit immediately after 'shift values'. */
    __quex_assert(LexemeBegin <= LexemeEnd);
    if(LexemeBegin == LexemeEnd) return;
    me->buffer._input_p = LexemeBegin;

    /* (78 from BEFORE_ENTRY)  */
    input = *(me->buffer._input_p);

    __quex_debug("Init State\n");
    __quex_debug_state(78);
_20:
    character_begin_p = (me->buffer._input_p);

    __quex_debug("Init State\n");
    __quex_debug_state(78);

    __quex_debug("Init State\n");
    __quex_debug_state(78);
switch( input ) {
case 0x9: goto _5;
case 0xA: goto _12;
case 0x30: case 0x31: case 0x32: case 0x33: case 0x34: case 0x35: case 0x36: case 0x37: 
case 0x38: case 0x39: goto _4;
case 0x80: case 0x81: case 0x82: case 0x83: case 0x84: case 0x85: case 0x86: case 0x87: 
case 0x88: case 0x89: case 0x8A: case 0x8B: case 0x8C: case 0x8D: case 0x8E: case 0x8F: 
case 0x90: case 0x91: case 0x92: case 0x93: case 0x94: case 0x95: case 0x96: case 0x97: 
case 0x98: case 0x99: case 0x9A: case 0x9B: case 0x9C: case 0x9D: case 0x9E: case 0x9F: 
case 0xA0: case 0xA1: case 0xA2: case 0xA3: case 0xA4: case 0xA5: case 0xA6: case 0xA7: 
case 0xA8: case 0xA9: case 0xAA: case 0xAB: case 0xAC: case 0xAD: case 0xAE: case 0xAF: 
case 0xB0: case 0xB1: case 0xB2: case 0xB3: case 0xB4: case 0xB5: case 0xB6: case 0xB7: 
case 0xB8: case 0xB9: case 0xBA: case 0xBB: case 0xBC: case 0xBD: case 0xBE: case 0xBF: 
case 0xC0: case 0xC1: goto _13;
case 0xC2: case 0xC3: case 0xC4: case 0xC5: case 0xC6: case 0xC7: 
case 0xC8: case 0xC9: case 0xCA: case 0xCB: case 0xCC: case 0xCD: case 0xCE: case 0xCF: 
case 0xD0: case 0xD1: case 0xD2: case 0xD3: case 0xD4: case 0xD5: case 0xD6: case 0xD7: 
case 0xD8: case 0xD9: case 0xDA: case 0xDB: case 0xDC: case 0xDD: case 0xDE: case 0xDF: goto _8;
case 0xE0: goto _11;
case 0xE1: case 0xE2: case 0xE3: case 0xE4: case 0xE5: case 0xE6: case 0xE7: 
case 0xE8: case 0xE9: case 0xEA: case 0xEB: case 0xEC: case 0xED: case 0xEE: case 0xEF: goto _9;
case 0xF0: goto _10;
case 0xF1: case 0xF2: case 0xF3: goto _7;
case 0xF4: goto _3;
case 0xF5: case 0xF6: case 0xF7: 
case 0xF8: case 0xF9: case 0xFA: case 0xFB: case 0xFC: case 0xFD: case 0xFE: case 0xFF: goto _13;
default: goto _6;
}


    __quex_assert_no_passage();
_18:
    /* (78 from 89)  */
    __quex_debug_state(78);
    goto _20;


    __quex_assert_no_passage();
_13:
    /* (DROP_OUT from 78) (DROP_OUT from 85) (DROP_OUT from 79) (DROP_OUT from 86) (DROP_OUT from 87) (DROP_OUT from 83) (DROP_OUT from 84)  */
    __quex_debug("Drop-Out Catcher\n");

        me->buffer._input_p = me->buffer._lexeme_start_p + 1;
goto _23;
    __quex_debug("Drop-Out Catcher\n");

    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_15:
    /* (DROP_OUT from 81)  */
    goto _24;
    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_17:
    /* (DROP_OUT from 88)  */
    goto _25;
    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_14:
    /* (DROP_OUT from 80)  */
    goto _26;
    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_16:
    /* (DROP_OUT from 82)  */
    goto _27;
    __quex_debug("Drop-Out Catcher\n");


    __quex_assert_no_passage();
_3:
    /* (79 from 78)  */
    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(79);

    __quex_debug_state(79);
if     ( input >= 0x90 )  goto _13;
else if( input >= 0x80 )  goto _9;
else                      goto _13;


    __quex_assert_no_passage();
_4:
    /* (80 from 78)  */
    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(80);

    __quex_debug_state(80);
goto _14;


    __quex_assert_no_passage();
_5:
    /* (81 from 78)  */
    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(81);

    __quex_debug_state(81);
goto _15;


    __quex_assert_no_passage();
_6:
    /* (82 from 84) (82 from 78)  */
    __quex_debug_state(82);

    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(82);

    __quex_debug_state(82);
goto _16;


    __quex_assert_no_passage();
_7:
    /* (83 from 78)  */
    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(83);

    __quex_debug_state(83);
if     ( input >= 0xC0 )  goto _13;
else if( input >= 0x80 )  goto _9;
else                      goto _13;


    __quex_assert_no_passage();
_8:
    /* (84 from 87) (84 from 78) (84 from 85)  */
    __quex_debug_state(84);

    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(84);

    __quex_debug_state(84);
if     ( input >= 0xC0 )  goto _13;
else if( input >= 0x80 )  goto _6;
else                      goto _13;


    __quex_assert_no_passage();
_9:
    /* (85 from 86) (85 from 79) (85 from 78) (85 from 83)  */
    __quex_debug_state(85);

    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(85);

    __quex_debug_state(85);
if     ( input >= 0xC0 )  goto _13;
else if( input >= 0x80 )  goto _8;
else                      goto _13;


    __quex_assert_no_passage();
_10:
    /* (86 from 78)  */
    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(86);

    __quex_debug_state(86);
if     ( input >= 0xC0 )  goto _13;
else if( input >= 0x90 )  goto _9;
else                      goto _13;


    __quex_assert_no_passage();
_11:
    /* (87 from 78)  */
    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(87);

    __quex_debug_state(87);
if     ( input >= 0xC0 )  goto _13;
else if( input >= 0xA0 )  goto _8;
else                      goto _13;


    __quex_assert_no_passage();
_12:
    /* (88 from 78)  */
    ++(me->buffer._input_p);

    input = *(me->buffer._input_p);

    __quex_debug_state(88);

    __quex_debug_state(88);
goto _17;

    /* (*) Terminal states _______________________________________________________
     *
     * States that implement actions of the 'winner patterns.                     */
_25:
    __quex_debug("* TERMINAL LINE\n");
__QUEX_IF_COUNT_LINES_ADD((size_t)1);

    __QUEX_IF_COUNT_COLUMNS((me->counter._column_number_at_end) = (size_t)1);

if( me->buffer._input_p != LexemeEnd ) goto _18;

goto _1;

_24:
    __quex_debug("* TERMINAL GRID\n");
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end -= 1);
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end &= ~ ((size_t)0x3));
__QUEX_IF_COUNT_COLUMNS(self.counter._column_number_at_end += 4 + 1);

if( me->buffer._input_p != LexemeEnd ) goto _18;

goto _1;

_26:
    __quex_debug("* TERMINAL COLUMN\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)10);

if( me->buffer._input_p != LexemeEnd ) goto _18;

goto _1;

_27:
    __quex_debug("* TERMINAL COLUMN\n");
__QUEX_IF_COUNT_COLUMNS_ADD((size_t)1);

if( me->buffer._input_p != LexemeEnd ) goto _18;

goto _1;

_41:
    __quex_debug("* TERMINAL <BEYOND>\n");
    (me->buffer._input_p) = character_begin_p;

goto _1;

_23: /* TERMINAL: FAILURE */
goto _41;
_1:
     __quex_assert(me->buffer._input_p == LexemeEnd); /* Otherwise, lexeme violates codec character boundaries. */
    return;
#   ifndef QUEX_OPTION_COMPUTED_GOTOS
    __quex_assert_no_passage();
_42:
#   endif /* QUEX_OPTION_COMPUTED_GOTOS */
#   undef self
#   undef QUEX_LABEL_STATE_ROUTER
#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)
     goto _42; /* in QUEX_GOTO_STATE       */
#    endif
    /* Avoid compiler warning: Unused label for 'TERMINAL <BEYOND>' */
    goto _41;
    goto _23;
    (void)target_state_index;
    (void)target_state_else_index;
}
#endif /* __QUEX_OPTION_COUNTER */
