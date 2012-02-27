import quex.engine.analyzer.mega_state.template.core as     template_analyzer
import quex.engine.analyzer.mega_state.path.core     as     path_analyzer
from   quex.blackboard                               import E_StateIndices, E_Compression
from   quex.blackboard                               import setup as Setup

def do(TheAnalyzer):
    # Track what states are treated with different methods (see below)
    remainder  = set(TheAnalyzer.state_db.keys())
    # The init state shall never be part of a mega state
    remainder.discard(TheAnalyzer.init_state_index)

    mega_state_list = []
    remainder       = set(TheAnalyzer.state_db.keys())
    remainder.remove(TheAnalyzer.init_state_index)
    for ctype in Setup.compression_type_list:
        # -- Path-Compression
        if ctype in (E_Compression.PATH, E_Compression.PATH_UNIFORM):
            done_state_index_list, \
            new_mega_state_list    = path_analyzer.do(TheAnalyzer, ctype, 
                                                      remainder, mega_state_list)
    
        # -- Template-Compression
        elif ctype in (E_Compression.TEMPLATE, E_Compression.TEMPLATE_UNIFORM):
            done_state_index_list, \
            new_mega_state_list    = template_analyzer.do(TheAnalyzer, 
                                                          Setup.compression_template_min_gain, ctype, 
                                                          remainder, mega_state_list)
        else:
            assert False

        __transition_adaption(TheAnalyzer, new_mega_state_list, mega_state_list)

        remainder.difference_update(done_state_index_list)
        mega_state_list.extend(new_mega_state_list)

    TheAnalyzer.non_mega_state_index_set = remainder
    TheAnalyzer.mega_state_list          = mega_state_list

def __transition_adaption(TheAnalyzer, NewMegaStateList, OldMegaStateList):
    """Some AnalyzerState objects have been implemented in Mega States that 
       contain multiple states in once. Thus, the transitions to those AnalyzerState-s
       must be related to doors in the Mega State. This is what happens inside
       the present function.
    """
    # For the states that the new mega states implement, the doors need to 
    # be redirected from the original states to doors of the mega states.
    door_id_replacement_db = {}
    for mega_state in NewMegaStateList:
        door_id_replacement_db.update(mega_state.door_id_replacement_db)

    # All template states must set the databases about 'door-id' and 'transition-id'
    # in the states that they implement.
    for state in NewMegaStateList:
        state.replace_door_ids_in_transition_map(door_id_replacement_db)

    for state in OldMegaStateList:
        state.replace_door_ids_in_transition_map(door_id_replacement_db)

    # We must leave the databases in place, until the replacements are made
    for mega_state in NewMegaStateList:
        for state in (TheAnalyzer.state_db[i] for i in mega_state.implemented_state_index_list()):
            # Make sure, that the databases which are referenced for transition addresses
            # are updated, i.e. we use the ones of the template state.
            state.entry.set_door_db(mega_state.entry.door_db)
            state.entry.set_transition_db(mega_state.entry.transition_db)
            state.entry.set_door_tree_root(mega_state.entry.door_tree_root)
    return