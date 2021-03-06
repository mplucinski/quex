#! /usr/bin/env bash
bug=2002070
if [[ $1 == "--hwut-info" ]]; then
    echo "attardi: $bug Output buffer overflow"
    echo "CHOICES: iconv, icu;"
    echo "SAME;"
    exit
fi

tmp=`pwd`
cd $bug/ 

if [[ $2 == "FIRST" ]]; then
    make clean
fi

make lexer-$1
./lexer-$1 text.345

# cleansening
if [[ $3 == "LAST" ]]; then
   make clean
fi
cd $tmp
