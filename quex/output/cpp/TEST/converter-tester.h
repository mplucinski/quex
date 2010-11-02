#ifndef __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256__
#define __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256__

/* 2005-2010 (C) Frank-Rene Schaefer; ABSOLUTELY NO WARRANTY */

/* Converter Functions: ____________________________________________________________________
 *
 *   cp1256_to_utf8(...)         -- character to utf8
 *   cp1256_to_utf8_string(...)  -- string to utf8
 *   cp1256_to_utf8_string(C++)  -- C++ string to utf8 (std::string)
 *
 *   cp1256_to_wchar(...)        -- character to utf8
 *   cp1256_to_wstring(...)      -- string to utf8
 *   cp1256_to_wstring(C++)      -- C++ string to utf8 (std::wstring)
 *__________________________________________________________________________________________*/

#define  __QUEX_CONVERTER_FROM         cp1256
#include <quex/code_base/converter_helper/base.g>

#endif /* __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256__ */

/* -*- C++ -*- vim: set syntax=cpp:
 * 
 * ACKNOWLEDGEMENT: Parts of the following utf8 conversion have been derived from 
 *                  segments of the utf8 conversion library of Alexey Vatchenko 
 *                  <av@bsdua.org>.    
 *
 * (C) 2005-2009 Frank-Rene Schaefer                                                */
#ifndef __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256_I
#define __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256_I

#include <quex/code_base/definitions>
#include <quex/code_base/compatibility/inttypes.h>
#include <quex/code_base/asserts>

/* Converter Functions: ____________________________________________________________________
 *
 *   cp1256_to_utf8(...)         -- character to utf8
 *   cp1256_to_utf8_string(...)  -- string to utf8
 *   cp1256_to_utf8_string(C++)  -- C++ string to utf8 (std::string)
 *
 *   cp1256_to_wchar(...)        -- character to utf8
 *   cp1256_to_wstring(...)      -- string to utf8
 *   cp1256_to_wstring(C++)      -- C++ string to utf8 (std::wstring)
 *__________________________________________________________________________________________*/

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void
QUEX_NAME(cp1256_to_utf8)(const QUEX_TYPE_CHARACTER**  input_pp, 
                             uint8_t**                    output_pp)
{
    const int NEXT = 0x80;
    const int LEN2 = 0x0C0;
    const int LEN3 = 0x0E0;

    uint32_t   unicode  = 0xFFFF;
    uint8_t*   output_p = *output_pp;
    uint8_t*   p        = output_p;

    QUEX_TYPE_CHARACTER input = **input_pp;
    
    /* The unicode range simply does not go beyond 0x10FFFF */
    __quex_assert(input < 0x110000);
    /* If the following assert fails, then QUEX_TYPE_CHARACTER needs to be chosen
     * of 'unsigned' type, e.g. 'unsigned char' instead of 'char'.                */
    /* __quex_assert(input >= 0); */

#if 0
#   if defined(__QUEX_OPTION_LITTLE_ENDIAN)
#   define QUEX_BYTE_0  (*( ((uint8_t*)&unicode) + 3 ))
#   define QUEX_BYTE_1  (*( ((uint8_t*)&unicode) + 2 ))
#   define QUEX_BYTE_2  (*( ((uint8_t*)&unicode) + 1 ))
#   define QUEX_BYTE_3  (*( ((uint8_t*)&unicode) + 0 ))
#   else                             
#   define QUEX_BYTE_0  (*( ((uint8_t*)&unicode) + 0 ))
#   define QUEX_BYTE_1  (*( ((uint8_t*)&unicode) + 1 ))
#   define QUEX_BYTE_2  (*( ((uint8_t*)&unicode) + 2 ))
#   define QUEX_BYTE_3  (*( ((uint8_t*)&unicode) + 3 ))
#   endif
#else
#   define QUEX_BYTE_0  ((uint8_t)((unicode & 0xFF)))
#   define QUEX_BYTE_1  ((uint8_t)((unicode & 0xFF00) >> 8))
#   define QUEX_BYTE_2  ((uint8_t)((unicode & 0xFF0000) >> 16))
#   define QUEX_BYTE_3  ((uint8_t)((unicode & 0xFF000000) >> 24))
#endif

    if( input < 0x0000A1) {
        if( input < 0x00008E) {
            if( input < 0x000086) {
                if( input < 0x000082) {
                    if( input < 0x000080) {
                        unicode = 0x000000 + (input - 0x000000);
                        *p = QUEX_BYTE_0; ++p;
                    } else {
                    
                        if( input < 0x000081) {
                            unicode = 0x0020AC + (input - 0x000080);
                            *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                            *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        } else {
                        
                            unicode = 0x00067E + (input - 0x000081);
                            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        }
                    }
                } else {
                
                    if( input < 0x000084) {
                        if( input < 0x000083) {
                            unicode = 0x00201A + (input - 0x000082);
                            *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                            *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        } else {
                        
                            unicode = 0x000192 + (input - 0x000083);
                            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        }
                    } else {
                    
                        if( input < 0x000085) {
                            unicode = 0x00201E + (input - 0x000084);
                        } else {
                        
                            unicode = 0x002026 + (input - 0x000085);
                        }
                        *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                        *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                        *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                    }
                }
            } else {
            
                if( input < 0x00008A) {
                    if( input < 0x000088) {
                        unicode = 0x002020 + (input - 0x000086);
                        *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                        *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                        *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                    } else {
                    
                        if( input < 0x000089) {
                            unicode = 0x0002C6 + (input - 0x000088);
                            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        } else {
                        
                            unicode = 0x002030 + (input - 0x000089);
                            *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                            *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        }
                    }
                } else {
                
                    if( input < 0x00008C) {
                        if( input < 0x00008B) {
                            unicode = 0x000679 + (input - 0x00008A);
                            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        } else {
                        
                            unicode = 0x002039 + (input - 0x00008B);
                            *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                            *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        }
                    } else {
                    
                        if( input < 0x00008D) {
                            unicode = 0x000152 + (input - 0x00008C);
                        } else {
                        
                            unicode = 0x000686 + (input - 0x00008D);
                        }
                        *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                        *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                    }
                }
            }
        } else {
        
            if( input < 0x000098) {
                if( input < 0x000091) {
                    if( input < 0x00008F) {
                        unicode = 0x000698 + (input - 0x00008E);
                    } else {
                    
                        if( input < 0x000090) {
                            unicode = 0x000688 + (input - 0x00008F);
                        } else {
                        
                            unicode = 0x0006AF + (input - 0x000090);
                        }
                    }
                    *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                    *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                } else {
                
                    if( input < 0x000095) {
                        if( input < 0x000093) {
                            unicode = 0x002018 + (input - 0x000091);
                        } else {
                        
                            unicode = 0x00201C + (input - 0x000093);
                        }
                    } else {
                    
                        if( input < 0x000096) {
                            unicode = 0x002022 + (input - 0x000095);
                        } else {
                        
                            unicode = 0x002013 + (input - 0x000096);
                        }
                    }
                    *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                    *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                    *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                }
            } else {
            
                if( input < 0x00009C) {
                    if( input < 0x00009A) {
                        if( input < 0x000099) {
                            unicode = 0x0006A9 + (input - 0x000098);
                            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        } else {
                        
                            unicode = 0x002122 + (input - 0x000099);
                            *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                            *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        }
                    } else {
                    
                        if( input < 0x00009B) {
                            unicode = 0x000691 + (input - 0x00009A);
                            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        } else {
                        
                            unicode = 0x00203A + (input - 0x00009B);
                            *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                            *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        }
                    }
                } else {
                
                    if( input < 0x00009F) {
                        if( input < 0x00009D) {
                            unicode = 0x000153 + (input - 0x00009C);
                            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        } else {
                        
                            unicode = 0x00200C + (input - 0x00009D);
                            *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                            *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        }
                    } else {
                    
                        if( input < 0x0000A0) {
                            unicode = 0x0006BA + (input - 0x00009F);
                        } else {
                        
                            unicode = 0x0000A0 + (input - 0x0000A0);
                        }
                        *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                        *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                    }
                }
            }
        }
    } else {
    
        if( input < 0x0000E2) {
            if( input < 0x0000C0) {
                if( input < 0x0000AB) {
                    if( input < 0x0000A2) {
                        unicode = 0x00060C + (input - 0x0000A1);
                    } else {
                    
                        if( input < 0x0000AA) {
                            unicode = 0x0000A2 + (input - 0x0000A2);
                        } else {
                        
                            unicode = 0x0006BE + (input - 0x0000AA);
                        }
                    }
                } else {
                
                    if( input < 0x0000BB) {
                        if( input < 0x0000BA) {
                            unicode = 0x0000AB + (input - 0x0000AB);
                        } else {
                        
                            unicode = 0x00061B + (input - 0x0000BA);
                        }
                    } else {
                    
                        if( input < 0x0000BF) {
                            unicode = 0x0000BB + (input - 0x0000BB);
                        } else {
                        
                            unicode = 0x00061F + (input - 0x0000BF);
                        }
                    }
                }
            } else {
            
                if( input < 0x0000D8) {
                    if( input < 0x0000C1) {
                        unicode = 0x0006C1 + (input - 0x0000C0);
                    } else {
                    
                        if( input < 0x0000D7) {
                            unicode = 0x000621 + (input - 0x0000C1);
                        } else {
                        
                            unicode = 0x0000D7 + (input - 0x0000D7);
                        }
                    }
                } else {
                
                    if( input < 0x0000E0) {
                        if( input < 0x0000DC) {
                            unicode = 0x000637 + (input - 0x0000D8);
                        } else {
                        
                            unicode = 0x000640 + (input - 0x0000DC);
                        }
                    } else {
                    
                        if( input < 0x0000E1) {
                            unicode = 0x0000E0 + (input - 0x0000E0);
                        } else {
                        
                            unicode = 0x000644 + (input - 0x0000E1);
                        }
                    }
                }
            }
            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
        } else {
        
            if( input < 0x0000F5) {
                if( input < 0x0000EC) {
                    if( input < 0x0000E3) {
                        unicode = 0x0000E2 + (input - 0x0000E2);
                    } else {
                    
                        if( input < 0x0000E7) {
                            unicode = 0x000645 + (input - 0x0000E3);
                        } else {
                        
                            unicode = 0x0000E7 + (input - 0x0000E7);
                        }
                    }
                } else {
                
                    if( input < 0x0000F0) {
                        if( input < 0x0000EE) {
                            unicode = 0x000649 + (input - 0x0000EC);
                        } else {
                        
                            unicode = 0x0000EE + (input - 0x0000EE);
                        }
                    } else {
                    
                        if( input < 0x0000F4) {
                            unicode = 0x00064B + (input - 0x0000F0);
                        } else {
                        
                            unicode = 0x0000F4 + (input - 0x0000F4);
                        }
                    }
                }
                *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
            } else {
            
                if( input < 0x0000FA) {
                    if( input < 0x0000F8) {
                        if( input < 0x0000F7) {
                            unicode = 0x00064F + (input - 0x0000F5);
                        } else {
                        
                            unicode = 0x0000F7 + (input - 0x0000F7);
                        }
                    } else {
                    
                        if( input < 0x0000F9) {
                            unicode = 0x000651 + (input - 0x0000F8);
                        } else {
                        
                            unicode = 0x0000F9 + (input - 0x0000F9);
                        }
                    }
                    *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                    *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                } else {
                
                    if( input < 0x0000FD) {
                        if( input < 0x0000FB) {
                            unicode = 0x000652 + (input - 0x0000FA);
                        } else {
                        
                            unicode = 0x0000FB + (input - 0x0000FB);
                        }
                        *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                        *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                    } else {
                    
                        if( input < 0x0000FF) {
                            unicode = 0x00200E + (input - 0x0000FD);
                            *(p++) = LEN3 | ((QUEX_BYTE_1 & 0xf0) >> 4);
                            *(p++) = NEXT | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x0f) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        } else {
                        
                            unicode = 0x0006D2 + (input - 0x0000FF);
                            *(p++) = LEN2 | (QUEX_BYTE_0 >> 6) | ((QUEX_BYTE_1 & 0x07) << 2);
                            *(p++) = NEXT | (QUEX_BYTE_0 & 0x3f);
                        }
                    }
                }
            }
        }
    }

    __quex_assert(p - output_p < (ptrdiff_t)7);
    __quex_assert(p > output_p);
    *output_pp = p;
    ++(*input_pp);

#   undef QUEX_BYTE_0 
#   undef QUEX_BYTE_1 
#   undef QUEX_BYTE_2 
#   undef QUEX_BYTE_3 
}

#if ! defined(__QUEX_OPTION_WCHAR_T_DISABLED)

QUEX_INLINE void
QUEX_NAME(cp1256_to_wchar)(const QUEX_TYPE_CHARACTER** input_pp,
                              wchar_t**                   output_pp)
{
    uint32_t             unicode = 0L;
    QUEX_TYPE_CHARACTER  input = **input_pp;
    if( input < 0x0000A1) {
        if( input < 0x00008E) {
            if( input < 0x000086) {
                if( input < 0x000082) {
                    if( input < 0x000080) {
                        unicode = 0x000000 + (input - 0x000000);
                    } else {
                    
                        if( input < 0x000081) {
                            unicode = 0x0020AC + (input - 0x000080);
                        } else {
                        
                            unicode = 0x00067E + (input - 0x000081);
                        }
                    }
                } else {
                
                    if( input < 0x000084) {
                        if( input < 0x000083) {
                            unicode = 0x00201A + (input - 0x000082);
                        } else {
                        
                            unicode = 0x000192 + (input - 0x000083);
                        }
                    } else {
                    
                        if( input < 0x000085) {
                            unicode = 0x00201E + (input - 0x000084);
                        } else {
                        
                            unicode = 0x002026 + (input - 0x000085);
                        }
                    }
                }
            } else {
            
                if( input < 0x00008A) {
                    if( input < 0x000088) {
                        unicode = 0x002020 + (input - 0x000086);
                    } else {
                    
                        if( input < 0x000089) {
                            unicode = 0x0002C6 + (input - 0x000088);
                        } else {
                        
                            unicode = 0x002030 + (input - 0x000089);
                        }
                    }
                } else {
                
                    if( input < 0x00008C) {
                        if( input < 0x00008B) {
                            unicode = 0x000679 + (input - 0x00008A);
                        } else {
                        
                            unicode = 0x002039 + (input - 0x00008B);
                        }
                    } else {
                    
                        if( input < 0x00008D) {
                            unicode = 0x000152 + (input - 0x00008C);
                        } else {
                        
                            unicode = 0x000686 + (input - 0x00008D);
                        }
                    }
                }
            }
        } else {
        
            if( input < 0x000098) {
                if( input < 0x000091) {
                    if( input < 0x00008F) {
                        unicode = 0x000698 + (input - 0x00008E);
                    } else {
                    
                        if( input < 0x000090) {
                            unicode = 0x000688 + (input - 0x00008F);
                        } else {
                        
                            unicode = 0x0006AF + (input - 0x000090);
                        }
                    }
                } else {
                
                    if( input < 0x000095) {
                        if( input < 0x000093) {
                            unicode = 0x002018 + (input - 0x000091);
                        } else {
                        
                            unicode = 0x00201C + (input - 0x000093);
                        }
                    } else {
                    
                        if( input < 0x000096) {
                            unicode = 0x002022 + (input - 0x000095);
                        } else {
                        
                            unicode = 0x002013 + (input - 0x000096);
                        }
                    }
                }
            } else {
            
                if( input < 0x00009C) {
                    if( input < 0x00009A) {
                        if( input < 0x000099) {
                            unicode = 0x0006A9 + (input - 0x000098);
                        } else {
                        
                            unicode = 0x002122 + (input - 0x000099);
                        }
                    } else {
                    
                        if( input < 0x00009B) {
                            unicode = 0x000691 + (input - 0x00009A);
                        } else {
                        
                            unicode = 0x00203A + (input - 0x00009B);
                        }
                    }
                } else {
                
                    if( input < 0x00009F) {
                        if( input < 0x00009D) {
                            unicode = 0x000153 + (input - 0x00009C);
                        } else {
                        
                            unicode = 0x00200C + (input - 0x00009D);
                        }
                    } else {
                    
                        if( input < 0x0000A0) {
                            unicode = 0x0006BA + (input - 0x00009F);
                        } else {
                        
                            unicode = 0x0000A0 + (input - 0x0000A0);
                        }
                    }
                }
            }
        }
    } else {
    
        if( input < 0x0000E2) {
            if( input < 0x0000C0) {
                if( input < 0x0000AB) {
                    if( input < 0x0000A2) {
                        unicode = 0x00060C + (input - 0x0000A1);
                    } else {
                    
                        if( input < 0x0000AA) {
                            unicode = 0x0000A2 + (input - 0x0000A2);
                        } else {
                        
                            unicode = 0x0006BE + (input - 0x0000AA);
                        }
                    }
                } else {
                
                    if( input < 0x0000BB) {
                        if( input < 0x0000BA) {
                            unicode = 0x0000AB + (input - 0x0000AB);
                        } else {
                        
                            unicode = 0x00061B + (input - 0x0000BA);
                        }
                    } else {
                    
                        if( input < 0x0000BF) {
                            unicode = 0x0000BB + (input - 0x0000BB);
                        } else {
                        
                            unicode = 0x00061F + (input - 0x0000BF);
                        }
                    }
                }
            } else {
            
                if( input < 0x0000D8) {
                    if( input < 0x0000C1) {
                        unicode = 0x0006C1 + (input - 0x0000C0);
                    } else {
                    
                        if( input < 0x0000D7) {
                            unicode = 0x000621 + (input - 0x0000C1);
                        } else {
                        
                            unicode = 0x0000D7 + (input - 0x0000D7);
                        }
                    }
                } else {
                
                    if( input < 0x0000E0) {
                        if( input < 0x0000DC) {
                            unicode = 0x000637 + (input - 0x0000D8);
                        } else {
                        
                            unicode = 0x000640 + (input - 0x0000DC);
                        }
                    } else {
                    
                        if( input < 0x0000E1) {
                            unicode = 0x0000E0 + (input - 0x0000E0);
                        } else {
                        
                            unicode = 0x000644 + (input - 0x0000E1);
                        }
                    }
                }
            }
        } else {
        
            if( input < 0x0000F5) {
                if( input < 0x0000EC) {
                    if( input < 0x0000E3) {
                        unicode = 0x0000E2 + (input - 0x0000E2);
                    } else {
                    
                        if( input < 0x0000E7) {
                            unicode = 0x000645 + (input - 0x0000E3);
                        } else {
                        
                            unicode = 0x0000E7 + (input - 0x0000E7);
                        }
                    }
                } else {
                
                    if( input < 0x0000F0) {
                        if( input < 0x0000EE) {
                            unicode = 0x000649 + (input - 0x0000EC);
                        } else {
                        
                            unicode = 0x0000EE + (input - 0x0000EE);
                        }
                    } else {
                    
                        if( input < 0x0000F4) {
                            unicode = 0x00064B + (input - 0x0000F0);
                        } else {
                        
                            unicode = 0x0000F4 + (input - 0x0000F4);
                        }
                    }
                }
            } else {
            
                if( input < 0x0000FA) {
                    if( input < 0x0000F8) {
                        if( input < 0x0000F7) {
                            unicode = 0x00064F + (input - 0x0000F5);
                        } else {
                        
                            unicode = 0x0000F7 + (input - 0x0000F7);
                        }
                    } else {
                    
                        if( input < 0x0000F9) {
                            unicode = 0x000651 + (input - 0x0000F8);
                        } else {
                        
                            unicode = 0x0000F9 + (input - 0x0000F9);
                        }
                    }
                } else {
                
                    if( input < 0x0000FD) {
                        if( input < 0x0000FB) {
                            unicode = 0x000652 + (input - 0x0000FA);
                        } else {
                        
                            unicode = 0x0000FB + (input - 0x0000FB);
                        }
                    } else {
                    
                        if( input < 0x0000FF) {
                            unicode = 0x00200E + (input - 0x0000FD);
                        } else {
                        
                            unicode = 0x0006D2 + (input - 0x0000FF);
                        }
                    }
                }
            }
        }
    }
    **output_pp = unicode;

    ++(*input_pp);
    ++(*output_pp);
}
#endif

QUEX_NAMESPACE_MAIN_CLOSE

#define __QUEX_CONVERTER_FROM     cp1256
#include <quex/code_base/converter_helper/base.gi>



#endif /* __QUEX_INCLUDE_GUARD__CONVERTER_HELPER__cp1256_I */

