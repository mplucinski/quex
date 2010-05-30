#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])
import quex.core_engine.state_machine.compression.templates as templates
from   quex.core_engine.state_machine.core                  import StateMachine, State
import quex.core_engine.generator.template_coder            as coder
import quex.core_engine.generator.languages.cpp             as cpp
from   quex.core_engine.generator.state_machine_decorator   import StateMachineDecorator
from   quex.input.setup import setup as Setup

if "--hwut-info" in sys.argv:
    print "Basic Template Compression Test;"
    print "CHOICES: 1, 2;"
    sys.exit(0)

# Buffer limit code is required in order to choose between
# 'direct drop out' and 'drop out' in state transition map.
Setup.buffer_limit_code = 0

# A state machine decorator is required for the code generation.
# Create a default one
sm = StateMachine()

sm.states = {
        1L:   State(),
        2L:   State(),
        3L:   State(),
        100L: State(),
        200L: State(),
        202L: State(),
        300L: State(),
        400L: State(),
        500L: State(),
        }
# print sm.states.keys()
for state_index in sm.states.keys():
    sm.add_transition(state_index, 1L, 202L)

DSM = StateMachineDecorator(sm, "Test", [], False, False)
# print DSM.sm().states.keys()


if "1" in sys.argv:
    combination = templates.TemplateCombination([100L], [200L, 202L])
    combination.append(-sys.maxint, 10, None)
    combination.append(8,   9,          [1L, None, 2L])
    combination.append(9,  10,          [1L, 3L,   2L])
    combination.append(10, 11,          100L)
    combination.append(11, 12,          -2)
    combination.append(12, 13,          None)
    combination.append(14, sys.maxint,  [2L, 3L,   1L])

else:
    combination = templates.TemplateCombination([100L], [200L, 202L, 300L, 400L, 500L])
    combination.append(-sys.maxint, 10, [1L, None, 1L, 2L,   2L, 2L])
    combination.append(10,  sys.maxint, [2L, 3L,   1L, None, 2L, 2L])

x = coder._do([combination], DSM)

print "--(Transition Targets)--------------------------------------------------"
print
print cpp.__local_variable_definitions(x[0])
print
print "--(Template Code)-------------------------------------------------------"
print
print "".join(x[1])
print
print "--(State Router)--------------------------------------------------------"
print
print "".join(x[2])
print

sys.exit(0)
