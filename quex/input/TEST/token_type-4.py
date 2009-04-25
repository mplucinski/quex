#! /usr/bin/env python
import sys
import os

sys.path.append(os.environ["QUEX_PATH"])

from quex.input.token_type import *
from StringIO import StringIO


if "--hwut-info" in sys.argv:
    print "token_type: Constructor, Copy, Destructor;"
    print "CHOICES: Constructor, Constructor-1, Constructor-2, Destructor, Copy;"
    sys.exit(0)

def test(Tag, Txt):
    descr = TokenTypeDescriptor()
    sh = StringIO(Tag + Txt)
    sh.name = "a string"
    print "-----------------------------"
    print "IN:"
    print "    [" + (Tag + Txt).replace("\n", "\n    ") + "]"
    print 
    print "OUT:"
    print 
    parse_section(sh, descr, [])
    try:
        pass
    except Exception, inst:
        print "Exception Caught: " + inst.__class__.__name__ 
        pass
    print descr


if   "Constructor" in sys.argv:
    test("constructor", "{ The world is a { nice } place. }")

if   "Constructor-1" in sys.argv:
    test("constructor", "{  ")

if   "Constructor-2" in sys.argv:
    test("constructor", "{  The world is a /* } */ nice place }")

if   "Destructor" in sys.argv:
    test("destructor", "{ The world is a { nice } place. }")

if   "Copy" in sys.argv:
    test("copy", "{ The world is a { nice } place. }")




