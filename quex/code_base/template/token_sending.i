// -*- C++ -*- vim:set syntax=cpp:
#ifndef __INCLUDE_GUARD_QUEX__CODE_BASE__QUEX_TOKEN_SENDING_H__
#define __INCLUDE_GUARD_QUEX__CODE_BASE__QUEX_TOKEN_SENDING_H__

#ifdef QUEX_OPTION_TOKEN_SENDING_VIA_QUEUE
#    define QUEX_TOKEN_VALUE_SET(X)                    *(_token_queue->write_iterator) = (X);
#    define QUEX_TOKEN_VALUE_SET_1(X0)                  _token_queue->write_iterator->set(X0);
#    define QUEX_TOKEN_VALUE_SET_2(X0, X1)              _token_queue->write_iterator->set(X0, X1);
#    define QUEX_TOKEN_VALUE_SET_3(X0, X1, X2)          _token_queue->write_iterator->set(X0, X1, X2);
#    define QUEX_TOKEN_VALUE_SET_4(X0, X1, X2, X3)      _token_queue->write_iterator->set(X0, X1, X2, X3);
#    define QUEX_TOKEN_VALUE_SET_5(X0, X1, X2, X3, X4)  _token_queue->write_iterator->set(X0, X1, X2, X3, X4);

#    define QUEX_TOKEN_PREPARE_NEXT() \
            ++(_token_queue->write_iterator); \
            __quex_assert(_token_queue->write_iterator <= _token_queue->end);

#    define QUEX_SET_REMAINING_REPETITION_NUMBER_SET(N) \
            _token_queue->remaining_repetitions_of_last_token_n = N;

#else
#    define QUEX_TOKEN_VALUE_SET(X)                    *_token = (X);
#    define QUEX_TOKEN_VALUE_SET_1(X0)                  token->set(X0);
#    define QUEX_TOKEN_VALUE_SET_2(X0, X1)              token->set(X0, X1);
#    define QUEX_TOKEN_VALUE_SET_3(X0, X1, X2)          token->set(X0, X1, X2);
#    define QUEX_TOKEN_VALUE_SET_4(X0, X1, X2, X3)      token->set(X0, X1, X2, X3);
#    define QUEX_TOKEN_VALUE_SET_5(X0, X1, X2, X3, X4)  token->set(X0, X1, X2, X3, X4);

#    define QUEX_TOKEN_PREPARE_NEXT()  \
            /* empty */

#    define QUEX_SET_REMAINING_REPETITION_NUMBER_SET(N) \
            token_repetion_n->remaining_repetitions_of_last_token_n = N;
#endif

namespace quex { 

    inline void   
    CLASS::send(const QUEX_TYPE_TOKEN& That) 
    {
        QUEX_TOKEN_VALUE_SET(That);
        QUEX_TOKEN_PREPARE_NEXT();
    }

    inline void   
    CLASS::send(const QUEX_TYPE_TOKEN_ID ID) 
    {
        QUEX_TOKEN_VALUE_SET_1(ID);
        QUEX_TOKEN_PREPARE_NEXT();
    }

    inline void   
    CLASS::send_n(const int RepetitionN, QUEX_TYPE_TOKEN_ID ID) 
    {
#       ifdef QUEX_OPTION_TOKEN_SENDING_VIA_QUEUE
        const int AvailableN = QuexTokenQueue_available_n(_token_queue);
        const int N = RepetitionN > AvailableN ? AvailableN : RepetitionN;
        __quex_assert(N > 0);

        QUEX_TOKEN_QUEUE_ASSERT(_token_queue);

        for(int n=0; n < N; n++) {
            QUEX_TOKEN_VALUE_SET_1(ID);
        }
        if( N - AvailableN ) {
            _token_queue->remaining_repetitions_of_last_token_n = N - AvailableN;
        }
#       else
        QUEX_TOKEN_VALUE_SET_1(That);
        QUEX_TOKEN_SET_REMAINING_REPETITION_NUMBER(N);
#       endif
    }

    template <typename X0_T> inline void   
    CLASS::send(const QUEX_TYPE_TOKEN_ID ID, X0_T X0) 
    {
        QUEX_TOKEN_VALUE_SET_2(ID, X0);
        QUEX_TOKEN_PREPARE_NEXT();
    }

#   if 0
    template <typename X0_T, typename X1_T> inline void   
    CLASS::send(const QUEX_TYPE_TOKEN_ID ID, X0_T X0, X1_T X1) 
    {
        QUEX_TOKEN_VALUE_SET_3(ID, X0, X1);
        QUEX_TOKEN_PREPARE_NEXT();
    }

    template <typename X0_T, typename X1_T, typename X2_T> inline void   
    CLASS::send(const QUEX_TYPE_TOKEN_ID ID, X0_T X0, X1_T X1, X2_T X2) 
    {
        QUEX_TOKEN_VALUE_SET_4(ID, X0, X1, X2);
        QUEX_TOKEN_PREPARE_NEXT();
    }

    template <typename X0_T, typename X1_T, typename X2_T, typename X3_T> inline void   
    CLASS::send(const QUEX_TYPE_TOKEN_ID ID, X0_T X0, X1_T X1, X2_T X2, X3_T) 
    {
        QUEX_TOKEN_VALUE_SET_5(ID, X0, X1, X2, X3);
        QUEX_TOKEN_PREPARE_NEXT();
    }
#   endif
}

#endif /* __INCLUDE_GUARD_QUEX__CODE_BASE__QUEX_TOKEN_SENDING_H__ */
