#define QUEX_CHARACTER_TYPE uint32_t
#include<iostream>
#include<fstream>

#include<quex/code_base/buffer/BufferFiller>
#include<quex/code_base/buffer/plain/BufferFiller_Plain>
#include<quex/code_base/buffer/plain/BufferFiller_Plain.i>
#include<cstring>

using namespace std;
using namespace quex;

int
main(int argc, char** argv) 
{
    if( argc <= 1 ) {
        cout << "command line argument required. try '--hwut-info'.\n";
        return 0;
    }
    else if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        cout << "sphericalcow: 1935701 - 0.24.7 buffer handling size mismatch\n";
        cout << "CHOICES: FILE, fstream";
        return 0;
    }

    uint8_t              buffer[512];
    size_t               loaded_character_n = 0;  

    if( strcmp(argv[1], "FILE") == 0 ) { 
        FILE* fh = 0x0;

        fh = fopen("misc/bug-1935701-text.dat", "r");
        if( fh == 0x0 ) {
            cout << "error file 'misc/bug-1935701-text.dat' not found.\n";
            return 0;
        }

        QuexBufferFiller_Plain<FILE>    is;
        QuexBufferFiller_Plain_construct<FILE>(&is, fh);
        loaded_character_n = __BufferFiller_Plain_read_characters<FILE>((QuexBufferFiller*)&is, 
                                                                        (QUEX_CHARACTER_TYPE*)buffer, 
                                                                        (const size_t)128);
        fclose(fh);
        cout << "4 byte mode: loaded characters = " << loaded_character_n << "\n";

    } else {
        fstream fh;

        fh.open("misc/bug-1935701-text.dat");
        if( fh.bad() ) {
            cout << "error file 'misc/bug-1935701-text.dat' not found.\n";
            return 0;
        }
        
        QuexBufferFiller_Plain<istream>    is;
        QuexBufferFiller_Plain_construct<istream>(&is, &fh);
        loaded_character_n = __BufferFiller_Plain_read_characters<istream>((QuexBufferFiller*)&is, 
                                                                           (QUEX_CHARACTER_TYPE*)buffer, 
                                                                           (const size_t)128);
        
        fh.close();
        cout << "4 byte mode: loaded characters = " << loaded_character_n << "\n";
    }

 
}
