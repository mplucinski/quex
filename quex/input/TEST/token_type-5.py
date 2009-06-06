#! /usr/bin/env python
import sys
import os

sys.path.append(os.environ["QUEX_PATH"])
import quex.input.setup         
quex.input.setup.setup.token_type_disable_stringless_check_f = True

from quex.input.token_type import *
from StringIO import StringIO


if "--hwut-info" in sys.argv:
    print "token_type: Class Name and Namespace;"
    print "CHOICES: 0, 1, 2, 3, 4, 5, 6;"
    sys.exit(0)

def test(Txt):
    descr = TokenTypeDescriptorCore()
    txt = "{" + Txt + "}"
    sh = StringIO(txt)
    sh.name = "a string"
    print "-----------------------------"
    print "IN:"
    print "    [ " + txt.replace("\n", "\n    ") + "]"
    print 
    print "OUT:"
    print 
    try:
        descr = parse(sh)
    except Exception, inst:
        print "Exception Caught: " + inst.__class__.__name__ 
    print TokenTypeDescriptor(descr)


arg = sys.argv[1]
test({ 
    "0": "name",
    "1": "name;",
    "2": "name =;",
    "3": "name = ispringen;",
    "3": "name = ispringen::;",
    "4": "name = deutschland::ispringen;",
    "5": "name = deutschland::ispringen::;",
    "6": "name = europa::deutschland::ispringen;",
    }[arg])




