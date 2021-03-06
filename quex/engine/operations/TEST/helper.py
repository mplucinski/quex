from   quex.engine.operations.content_terminal_router         import *
from   quex.engine.operations.operation_list         import *
from   quex.engine.operations.operation_list         import _cost_db
from   quex.engine.analyzer.door_id_address_label import DoorID
import quex.engine.operations.shared_tail  as command_list_shared_tail
import quex.engine.analyzer.engine_supply_factory as     engine
from   quex.output.core.dictionary       import db

from   quex.blackboard import E_Op, \
                              E_R, \
                              E_Compression, \
                              setup as Setup, \
                              Lng

from   itertools   import permutations
from   collections import defaultdict
from   copy        import deepcopy
from   random      import shuffle


Setup.language_db = db[Setup.language]

example_db = {
    E_Op.StoreInputPosition: [ 
        Op.StoreInputPosition(4711, 7777, 0),
        Op.StoreInputPosition(4711, 7777, 1000) 
    ],
    E_Op.PreContextOK:                     [ Op.PreContextOK(4711) ],
    E_Op.TemplateStateKeySet:              [ Op.TemplateStateKeySet(66) ],
    E_Op.PathIteratorSet:                  [ Op.PathIteratorSet(11, 22, 1000) ],
    E_Op.PrepareAfterReload:               [ Op.PrepareAfterReload(DoorID(33, 44), DoorID(55, 66)) ],
    E_Op.InputPIncrement:                  [ Op.InputPIncrement() ],
    E_Op.InputPDecrement:                  [ Op.InputPDecrement() ],
    E_Op.InputPDereference:                [ Op.InputPDereference() ],
    E_Op.LexemeResetTerminatingZero:       [ Op.LexemeResetTerminatingZero() ],
    E_Op.ColumnCountReferencePSet:         [ Op.ColumnCountReferencePSet(E_R.CharacterBeginP, 1000) ],
    E_Op.ColumnCountReferencePDeltaAdd:    [ Op.ColumnCountReferencePDeltaAdd(E_R.CharacterBeginP, 5555, False) ],
    E_Op.ColumnCountAdd:                   [ Op.ColumnCountAdd(1) ],
    E_Op.ColumnCountGridAdd: [ 
        Op.ColumnCountGridAdd(1),
        Op.ColumnCountGridAdd(2),
        Op.ColumnCountGridAdd(3),
        Op.ColumnCountGridAdd(4),
        Op.ColumnCountGridAdd(5),
    ],
    E_Op.LineCountAdd: [ Op.LineCountAdd(1) ],
    ## The column number is set to 1 at the newline.
    ## So, no the delta add 'column += (p - reference_p) * c' is not necessary.
    E_Op.GotoDoorId:                        [ Op.GotoDoorId(DoorID(33,44)) ],
    E_Op.GotoDoorIdIfInputPNotEqualPointer: [ Op.GotoDoorIdIfInputPNotEqualPointer(DoorID(33,44), E_R.CharacterBeginP) ],
    E_Op.Assign:                            [ Op.Assign(E_R.InputP, E_R.LexemeStartP) ],
    E_Op.AssignConstant: [ 
        Op.AssignConstant(E_R.InputP, 0), 
        Op.AssignConstant(E_R.ReferenceP, 1), 
        Op.AssignConstant(E_R.Column, 2), 
    ],
    E_Op.IfPreContextSetPositionAndGoto: [
        Op.IfPreContextSetPositionAndGoto(24, RouterContentElement(66, 1)),
    ],
    E_Op.IndentationHandlerCall: [ 
        Op.IndentationHandlerCall(True, "SLEEPY"),
        Op.IndentationHandlerCall(False, "EXITED"),
    ],
    E_Op.QuexAssertNoPassage: [
        Op.QuexAssertNoPassage(),
    ],
    E_Op.QuexDebug: [
        Op.QuexDebug("Hello Bug!"),
    ],
    E_Op.RouterOnStateKey: [
        Op.RouterOnStateKey(E_Compression.PATH, 0x4711L, 
                         [(1L, 100L), (2L, 200L), (3L, 300L)], 
                         lambda x: DoorID(x,1)),
    ],
}

accepter = Op.Accepter()
accepter.content.add(55L, 66L)
example_db[E_Op.Accepter] = [ accepter ]

router = Op.RouterByLastAcceptance()
router.content.add(66, 1)
example_db[E_Op.RouterByLastAcceptance] = [ router ]

def generator():
    """Iterable over all commands from the example_db.
    """
    index = 0
    for example_list in example_db.itervalues():
        for example in example_list:
            index += 1
            yield index, example

def generator_n(N, Begin=0):
    index = -1
    while 1 + 1 == 2:
        for i, cmd in generator():
            index += 1
            if   index < Begin:      continue
            elif index == N + Begin: return
            yield cmd

def random_command_list(N, Seed):
    return [ cmd for cmd in generator_n(N, Seed) ]

def get_two_lists(FirstSize):
    selectable = generator()

    first_list = []
    for i, cmd in selectable:
        if i == FirstSize: break
        first_list.append(cmd)

    second_list = [ cmd ]
    for i, cmd in selectable:
        second_list.append(cmd)

    return first_list, second_list

def rw_generator(N):
    """Iterable over all commands from the example_db.
    """
    for write_n in xrange(N):
        base = ["R"] + [" "] * (N - write_n - 1) + ["W"] * write_n
        for setting in set(permutations(base, N)):
            yield setting 

def rw_get(Flag):
    if   Flag == "R": return Op.Assign(E_R.InputP,       E_R.LexemeStartP)
    elif Flag == "W": return Op.Assign(E_R.LexemeStartP, E_R.InputP)
    else:             return Op.Assign(E_R.Column,       E_R.CharacterBeginP)

def string_cl(Name, Cl):
    if len(Cl) == 0:
        return "    %s: <empty>" % Name
    txt = "    %s: [0] %s\n" % (Name, Cl[0])
    for i, cmd in enumerate(Cl[1:]):
        txt += "       [%i] %s\n" % (i+1, cmd)
    return txt

def print_cl(Name, Cl):
    print string_cl(Name, Cl)

class MiniAnalyzer:
    def __init__(self):
        self.engine_type = engine.FORWARD

Lng.register_analyzer(MiniAnalyzer())
