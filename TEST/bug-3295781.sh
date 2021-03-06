#! /usr/bin/env bash
bug=3295781
if [[ $1 == "--hwut-info" ]]; then
    echo "remcobloemen1: $bug Duplicate label with Template and Path Compression"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex -i test.qx -o Simple --path-compression-uniform --template-compression --language C  --debug-exception >&1
awk '(/QUEX_NAME/ && /_analyzer_function/ && ! /=/) || /__quex_debug_path_walker_state/ || /__quex_debug_template_state/' Simple.c

echo "## Compile: No output is good output"
gcc -I${QUEX_PATH} -c Simple.c -Wall -Werror 2>&1

# cleansening
rm Simple*
cd $tmp

