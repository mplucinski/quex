lexer: simple.qx main.c
	quex -i  simple.qx -o Simple --post-categorizer --language C --debug-exception
	gcc -I$(QUEX_PATH) main.c Simple.c -o lexer -ggdb -Wall -Werror

clean: 
	rm -f Simple*
	rm -f lexer
