#! /usr/bin/env bash
bug=2161098
if [[ $1 == "--hwut-info" ]]; then
    echo "fschaef: $bug 0.32.1 Range Skipper Line Number Counter"
    echo "CHOICES: c_comments, shell_comments, funny_comments;"
    exit
fi

tmp=`pwd`
cd $bug/ 
make INPUT=$1
./lexer $1.txt

# cleansening
rm -f Simple Simple-core-engine.cpp Simple.cpp Simple-token_ids lexer
cd $tmp
