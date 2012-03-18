/* vim: set filetype=cpp:  -*- C++ -*-
 *
 * Declaration of all converter functions towards 'utf8', 'utf16', 'utf32',
 * 'char', and 'wchar_t': 
 *
 *    QUEX_CONVERTER_CHAR_DEF(cp1256, utf8)(...)
 *    QUEX_CONVERTER_CHAR_DEF(cp1256, utf16)(...)
 *    QUEX_CONVERTER_CHAR_DEF(cp1256, utf32)(...)
 *    QUEX_CONVERTER_CHAR_DEF(cp1256, char)(...)
 *    QUEX_CONVERTER_CHAR_DEF(cp1256, wchar_t)(...)
 *
 *    QUEX_CONVERTER_STRING_DEF(cp1256, utf8)(...)     for string and buffer 
 *    QUEX_CONVERTER_STRING_DEF(cp1256, utf16)(...)    for string and buffer 
 *    QUEX_CONVERTER_STRING_DEF(cp1256, utf32)(...)    for string and buffer 
 *    QUEX_CONVERTER_STRING_DEF(cp1256, char)(...)     for string and buffer 
 *    QUEX_CONVERTER_STRING_DEF(cp1256, wchar_t)(...)  for string and buffer 
 *
 * The declarations are generated by the file:
 *
 *             ../generator/declarations.g
 *
 * These functions ARE DEPENDENT on QUEX_TYPE_CHARACTER.
 * => Thus, they are placed in the analyzer's namespace.
 *
 * (C) 2012 Frank-Rene Schaefer. 
 *     ABSOLUTELY NO WARRANTY                                                */
/* 2010 (C) Frank-Rene Schaefer; ABSOLUTELY NO WARRANTY */
#ifndef __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256__
#define __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256__

#include <quex/code_base/converter_helper/common.h>

QUEX_NAMESPACE_MAIN_OPEN

#define __QUEX_FROM                cp1256
#define __QUEX_FROM_TYPE           QUEX_TYPE_CHARACTER

#include <quex/code_base/converter_helper/generator/declarations.g>

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256__ */

/* -*- C++ -*- vim: set syntax=cpp:
 * PURPOSE: 
 *
 * Provide the implementation of character and string converter functions
 * FROM the buffer's cp1256 to utf8, utf16, utf32, char, and wchar_t.
 *
 * STEPS:
 *
 * (1) Implement the character converters from buffer's cp1256 to 
 *     utf8, utf16, utf32. Those come out of quex's code generator.
 *
 * (1b) Derive the converts from cp1256 to char and wchar_t from
 *      those converters. For this use:
 *
 *          "../generator/character-converter-char-wchar_t.gi"
 *
 * (2) Generate the implementation of the string converters in terms
 *     of those character converters.
 *
 *     Use: "../generator/implementation-string-converters.gi"
 *
 *          which uses
 *
 *              "../generator/string-converter.gi"
 *
 *          to implement each string converter from the given 
 *          character converters. 
 *
 * These functions ARE DEPENDENT on QUEX_TYPE_CHARACTER.
 * => Thus, they are placed in the analyzer's namespace.
 *
 * 2010 (C) Frank-Rene Schaefer; 
 * ABSOLUTELY NO WARRANTY                                                    */
#ifndef __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256_I
#define __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256_I

#include "converter-tester.h"

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void
QUEX_CONVERTER_CHAR_DEF(cp1256, utf32)(const QUEX_TYPE_CHARACTER** input_pp,
                                          uint32_t**                  output_pp)
{
    uint16_t             unicode = (uint32_t)0;
    QUEX_TYPE_CHARACTER  input   = *(*input_pp)++;
    if( input < 0x0000A1 ) {
        if( input < 0x00008E ) {
            if( input < 0x000086 ) {
                if( input < 0x000082 ) {
                    if( input < 0x000080 ) {
                        unicode = (uint32_t)input;
                    } else {
                    
                        if( input < 0x000081 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00202C;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x0005FD;
                        }
                    }
                } else {
                
                    if( input < 0x000084 ) {
                        if( input < 0x000083 ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F98;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x00010F;
                        }
                    } else {
                    
                        if( input < 0x000085 ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F9A;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001FA1;
                        }
                    }
                }
            } else {
            
                if( input < 0x00008A ) {
                    if( input < 0x000088 ) {
                        unicode = (uint32_t)input + (uint32_t)0x001F9A;
                    } else {
                    
                        if( input < 0x000089 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00023E;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001FA7;
                        }
                    }
                } else {
                
                    if( input < 0x00008C ) {
                        if( input < 0x00008B ) {
                            unicode = (uint32_t)input + (uint32_t)0x0005EF;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001FAE;
                        }
                    } else {
                    
                        if( input < 0x00008D ) {
                            unicode = (uint32_t)input + (uint32_t)0x0000C6;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x0005F9;
                        }
                    }
                }
            }
        } else {
        
            if( input < 0x000098 ) {
                if( input < 0x000091 ) {
                    if( input < 0x00008F ) {
                        unicode = (uint32_t)input + (uint32_t)0x00060A;
                    } else {
                    
                        if( input < 0x000090 ) {
                            unicode = (uint32_t)input + (uint32_t)0x0005F9;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x00061F;
                        }
                    }
                } else {
                
                    if( input < 0x000095 ) {
                        if( input < 0x000093 ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F87;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001F89;
                        }
                    } else {
                    
                        if( input < 0x000096 ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F8D;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001F7D;
                        }
                    }
                }
            } else {
            
                if( input < 0x00009C ) {
                    if( input < 0x00009A ) {
                        if( input < 0x000099 ) {
                            unicode = (uint32_t)input + (uint32_t)0x000611;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x002089;
                        }
                    } else {
                    
                        if( input < 0x00009B ) {
                            unicode = (uint32_t)input + (uint32_t)0x0005F7;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001F9F;
                        }
                    }
                } else {
                
                    if( input < 0x00009F ) {
                        if( input < 0x00009D ) {
                            unicode = (uint32_t)input + (uint32_t)0x0000B7;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001F6F;
                        }
                    } else {
                    
                        if( input < 0x0000A0 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00061B;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }
                }
            }
        }
    } else {
    
        if( input < 0x0000E2 ) {
            if( input < 0x0000C0 ) {
                if( input < 0x0000AB ) {
                    if( input < 0x0000A2 ) {
                        unicode = (uint32_t)input + (uint32_t)0x00056B;
                    } else {
                    
                        if( input < 0x0000AA ) {
                            unicode = (uint32_t)input;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000614;
                        }
                    }
                } else {
                
                    if( input < 0x0000BB ) {
                        if( input < 0x0000BA ) {
                            unicode = (uint32_t)input;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000561;
                        }
                    } else {
                    
                        if( input < 0x0000BF ) {
                            unicode = (uint32_t)input;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000560;
                        }
                    }
                }
            } else {
            
                if( input < 0x0000D8 ) {
                    if( input < 0x0000C1 ) {
                        unicode = (uint32_t)input + (uint32_t)0x000601;
                    } else {
                    
                        if( input < 0x0000D7 ) {
                            unicode = (uint32_t)input + (uint32_t)0x000560;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }
                } else {
                
                    if( input < 0x0000E0 ) {
                        if( input < 0x0000DC ) {
                            unicode = (uint32_t)input + (uint32_t)0x00055F;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000564;
                        }
                    } else {
                    
                        if( input < 0x0000E1 ) {
                            unicode = (uint32_t)input;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000563;
                        }
                    }
                }
            }
        } else {
        
            if( input < 0x0000F5 ) {
                if( input < 0x0000EC ) {
                    if( input < 0x0000E3 ) {
                        unicode = (uint32_t)input;
                    } else {
                    
                        if( input < 0x0000E7 ) {
                            unicode = (uint32_t)input + (uint32_t)0x000562;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }
                } else {
                
                    if( input < 0x0000F0 ) {
                        if( input < 0x0000EE ) {
                            unicode = (uint32_t)input + (uint32_t)0x00055D;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    } else {
                    
                        if( input < 0x0000F4 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00055B;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }
                }
            } else {
            
                if( input < 0x0000FA ) {
                    if( input < 0x0000F8 ) {
                        if( input < 0x0000F7 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00055A;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    } else {
                    
                        if( input < 0x0000F9 ) {
                            unicode = (uint32_t)input + (uint32_t)0x000559;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }
                } else {
                
                    if( input < 0x0000FD ) {
                        if( input < 0x0000FB ) {
                            unicode = (uint32_t)input + (uint32_t)0x000558;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    } else {
                    
                        if( input < 0x0000FF ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F11;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x0005D3;
                        }
                    }
                }
            }
        }
    }
    *(*output_pp)++ = unicode;

}

QUEX_INLINE void
QUEX_CONVERTER_CHAR_DEF(cp1256, utf16)(const QUEX_TYPE_CHARACTER** input_pp,
                                          uint16_t**                  output_pp)
{
    uint32_t   unicode   = (uint32_t)0;
    uint32_t*  unicode_p = &unicode;

    QUEX_CONVERTER_CHAR(cp1256, utf32)(input_pp, &unicode_p);
    *(*output_pp)++ = unicode;

}

QUEX_INLINE void
QUEX_CONVERTER_CHAR_DEF(cp1256, utf8)(const QUEX_TYPE_CHARACTER**  input_pp, 
                                         uint8_t**                    output_pp)
{
    uint32_t            unicode = (uint32_t)-1;
    QUEX_TYPE_CHARACTER input   = *(*input_pp)++;
    
    if( input < 0x0000A1 ) {
        if( input < 0x00008E ) {
            if( input < 0x000086 ) {
                if( input < 0x000082 ) {
                    if( input < 0x000080 ) {
                        unicode = (uint32_t)input;
                        goto one_byte;
                    } else {
                    
                        if( input < 0x000081 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00202C;
                            goto three_bytes;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x0005FD;
                            goto two_bytes;
                        }
                    }
                } else {
                
                    if( input < 0x000084 ) {
                        if( input < 0x000083 ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F98;
                            goto three_bytes;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x00010F;
                            goto two_bytes;
                        }
                    } else {
                    
                        if( input < 0x000085 ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F9A;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001FA1;
                        }goto three_bytes;
                    }
                }
            } else {
            
                if( input < 0x00008A ) {
                    if( input < 0x000088 ) {
                        unicode = (uint32_t)input + (uint32_t)0x001F9A;
                        goto three_bytes;
                    } else {
                    
                        if( input < 0x000089 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00023E;
                            goto two_bytes;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001FA7;
                            goto three_bytes;
                        }
                    }
                } else {
                
                    if( input < 0x00008C ) {
                        if( input < 0x00008B ) {
                            unicode = (uint32_t)input + (uint32_t)0x0005EF;
                            goto two_bytes;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001FAE;
                            goto three_bytes;
                        }
                    } else {
                    
                        if( input < 0x00008D ) {
                            unicode = (uint32_t)input + (uint32_t)0x0000C6;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x0005F9;
                        }goto two_bytes;
                    }
                }
            }
        } else {
        
            if( input < 0x000098 ) {
                if( input < 0x000091 ) {
                    if( input < 0x00008F ) {
                        unicode = (uint32_t)input + (uint32_t)0x00060A;
                    } else {
                    
                        if( input < 0x000090 ) {
                            unicode = (uint32_t)input + (uint32_t)0x0005F9;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x00061F;
                        }
                    }goto two_bytes;
                } else {
                
                    if( input < 0x000095 ) {
                        if( input < 0x000093 ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F87;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001F89;
                        }
                    } else {
                    
                        if( input < 0x000096 ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F8D;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001F7D;
                        }
                    }goto three_bytes;
                }
            } else {
            
                if( input < 0x00009C ) {
                    if( input < 0x00009A ) {
                        if( input < 0x000099 ) {
                            unicode = (uint32_t)input + (uint32_t)0x000611;
                            goto two_bytes;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x002089;
                            goto three_bytes;
                        }
                    } else {
                    
                        if( input < 0x00009B ) {
                            unicode = (uint32_t)input + (uint32_t)0x0005F7;
                            goto two_bytes;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001F9F;
                            goto three_bytes;
                        }
                    }
                } else {
                
                    if( input < 0x00009F ) {
                        if( input < 0x00009D ) {
                            unicode = (uint32_t)input + (uint32_t)0x0000B7;
                            goto two_bytes;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x001F6F;
                            goto three_bytes;
                        }
                    } else {
                    
                        if( input < 0x0000A0 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00061B;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }goto two_bytes;
                    }
                }
            }
        }
    } else {
    
        if( input < 0x0000E2 ) {
            if( input < 0x0000C0 ) {
                if( input < 0x0000AB ) {
                    if( input < 0x0000A2 ) {
                        unicode = (uint32_t)input + (uint32_t)0x00056B;
                    } else {
                    
                        if( input < 0x0000AA ) {
                            unicode = (uint32_t)input;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000614;
                        }
                    }
                } else {
                
                    if( input < 0x0000BB ) {
                        if( input < 0x0000BA ) {
                            unicode = (uint32_t)input;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000561;
                        }
                    } else {
                    
                        if( input < 0x0000BF ) {
                            unicode = (uint32_t)input;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000560;
                        }
                    }
                }
            } else {
            
                if( input < 0x0000D8 ) {
                    if( input < 0x0000C1 ) {
                        unicode = (uint32_t)input + (uint32_t)0x000601;
                    } else {
                    
                        if( input < 0x0000D7 ) {
                            unicode = (uint32_t)input + (uint32_t)0x000560;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }
                } else {
                
                    if( input < 0x0000E0 ) {
                        if( input < 0x0000DC ) {
                            unicode = (uint32_t)input + (uint32_t)0x00055F;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000564;
                        }
                    } else {
                    
                        if( input < 0x0000E1 ) {
                            unicode = (uint32_t)input;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x000563;
                        }
                    }
                }
            }goto two_bytes;
        } else {
        
            if( input < 0x0000F5 ) {
                if( input < 0x0000EC ) {
                    if( input < 0x0000E3 ) {
                        unicode = (uint32_t)input;
                    } else {
                    
                        if( input < 0x0000E7 ) {
                            unicode = (uint32_t)input + (uint32_t)0x000562;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }
                } else {
                
                    if( input < 0x0000F0 ) {
                        if( input < 0x0000EE ) {
                            unicode = (uint32_t)input + (uint32_t)0x00055D;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    } else {
                    
                        if( input < 0x0000F4 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00055B;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }
                }goto two_bytes;
            } else {
            
                if( input < 0x0000FA ) {
                    if( input < 0x0000F8 ) {
                        if( input < 0x0000F7 ) {
                            unicode = (uint32_t)input + (uint32_t)0x00055A;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    } else {
                    
                        if( input < 0x0000F9 ) {
                            unicode = (uint32_t)input + (uint32_t)0x000559;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }
                    }goto two_bytes;
                } else {
                
                    if( input < 0x0000FD ) {
                        if( input < 0x0000FB ) {
                            unicode = (uint32_t)input + (uint32_t)0x000558;
                        } else {
                        
                            unicode = (uint32_t)input;
                        }goto two_bytes;
                    } else {
                    
                        if( input < 0x0000FF ) {
                            unicode = (uint32_t)input + (uint32_t)0x001F11;
                            goto three_bytes;
                        } else {
                        
                            unicode = (uint32_t)input + (uint32_t)0x0005D3;
                            goto two_bytes;
                        }
                    }
                }
            }
        }
    }


one_byte:
*((*output_pp)++) = (uint8_t)unicode;
return;
two_bytes:
*((*output_pp)++) = (uint8_t)(0xC0 | (unicode >> 6)); 
*((*output_pp)++) = (uint8_t)(0x80 | (unicode & (uint32_t)0x3f));
return;
three_bytes:
*((*output_pp)++) = (uint8_t)(0xE0 | unicode           >> 12);
*((*output_pp)++) = (uint8_t)(0x80 | (unicode & (uint32_t)0xFFF) >> 6);
*((*output_pp)++) = (uint8_t)(0x80 | (unicode & (uint32_t)0x3F));
return;

}

#define __QUEX_FROM           cp1256
#define __QUEX_FROM_TYPE      QUEX_TYPE_CHARACTER

/* (1b) Derive converters to char and wchar_t from the given set 
 *      of converters. (Generator uses __QUEX_FROM and QUEX_FROM_TYPE)      */
#include <quex/code_base/converter_helper/generator/character-converter-to-char-wchar_t.gi>

/* (2) Generate string converters to utf8, utf16, utf32 based on the
 *     definitions of the character converters.                             */
#include <quex/code_base/converter_helper/generator/implementations.gi>

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256_I */

