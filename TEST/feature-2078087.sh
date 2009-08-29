#! /usr/bin/env bash
bug=2078087
if [[ $1 == "--hwut-info" ]]; then
    echo "fschaef: $bug (feature) Mode transition shortcuts GOTO, GOSUB, GOUP"
    echo "CHOICES: GOTO, GOTO-2, GOSUB, GOSUB-2;"
    exit
fi

tmp=`pwd`
cd $bug/ 
make INPUT=$1.qx
./lexer $1.txt >& tmp.txt
cat tmp.txt

# cleansening
rm -f Simple Simple-core-engine.cpp Simple.cpp Simple-token_ids lexer *.o tmp.txt Simple-configuration
cd $tmp
