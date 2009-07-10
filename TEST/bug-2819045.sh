#! /usr/bin/env bash
bug=2819045
if [[ $1 == "--hwut-info" ]]; then
    echo "wryun: $bug 0.41.2 Some internal assertion fails on..."
    exit
fi

tmp=`pwd`
cd $bug/ 
quex -i error.qx -o Simple

# cleansening
rm -f Simple Simple-core-engine.cpp Simple.cpp Simple-token_ids Simplism
cd $tmp
