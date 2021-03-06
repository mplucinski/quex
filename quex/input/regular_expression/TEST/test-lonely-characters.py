#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine as core
from   quex.blackboard import setup as Setup
Setup.set_all_character_set_UNIT_TEST(-sys.maxint, sys.maxint)
Setup.buffer_limit_code = 0
Setup.path_limit_code   = 0
 
if "--hwut-info" in sys.argv:
    print "Basics: Lonestanding characters"
    sys.exit(0)
    
def test(TestString):
    # state_machine_index.clear()
    print "expression    = \"" + TestString + "\""
    print "state machine\n", core.do(TestString, {})

test('you(a|b)you')
test('[fb]oo-a')
test('a*(b|cd+)e+')
test('a*.b*')     # '.' == anything by newline
test('\\"\\n')
test('\\"\\[\\]\\-\\*\\+\\$\\^\\)\\(')

print "## NOTE: The 'c' has to be ignored, because it comes after the lonestanding space"
test('(a|b) c')
print "## NOTE: The 'c' has to be ignored, because it comes after the lonestanding space"
test('(a|b)\nc')
print "## NOTE: The '=> TKN_IF' has to be ignored, because it comes after the lonestanding space"
test('if         => TKN_IF')
test('\\n')
