"""TODO:

    NOTE: Acceptance Pruning of 'Pre-Contexts', 'Non-Ambigous Post Context'
          and 'Backward Input Position Detectors' happens with the original
          state machines: Module 'state_machine/acceptance_pruning.py'

    (*) Post-pone acceptance storage and position storage as much as 
        possible. This decreases the probability that a transition
        sequence ever hits such places.

    (2) If the state is the terminal of a post-context pattern
        without further transitions, then the input position
        is set to the end of the core pattern. Thus, it does
        not need to be incremented.

    (11) If all successor acceptance states depend on 
         a certain pre-context flag being raised, then
         the first state on that path can drop-out 
         on the condition that the pre-context is not met.

    (12) When a terminal is reached where the paths took 
         care of the pre-context checks, then there is no
         need to check it again in the terminal.

    (16) If no successor acceptance state 'cares' about the lexeme and
         a 'dont-care' acceptance state has been passed, then then reload
         can set the lexeme_start_p to the current input position and 
         reload the buffer from start.

    (17) All non-acceptance states that immediately follow a 'skipper
         state' must cause 'skip-failure' on drop-out.

"""

from   quex.blackboard import E_EngineTypes
from   itertools       import imap

def do(analyzer):
    if analyzer.engine_type != E_EngineTypes.FORWARD:
        return analyzer

    # If a state has no successor state, or only transitions to itself,
    # => No accepter check is necessary, done in drop-out
    for state_index, state in analyzer.state_db.iteritems():
        tm = state.transition_map
        if   len(tm) == 0: 
            state.entry.accepter.clear()
        elif (len(tm) == 1 and tm[0][1] == state_index):
            state.entry.accepter.clear()

    for entry in imap(lambda x: x.entry, analyzer.state_db.itervalues()):
        entry.finish()

    return analyzer


