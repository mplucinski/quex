import quex.engine.state_machine.index              as     index
from   quex.engine.generator.state.transition.core  import assert_adjacency
from   quex.engine.analyzer.state_entry             import Entry
from   quex.engine.analyzer.state_entry_action      import SetTemplateStateKey, TransitionID, DoorID
from   quex.engine.interval_handling                import Interval
from   quex.engine.analyzer.core                    import AnalyzerState, get_input_action
from   quex.blackboard                              import E_StateIndices

from   itertools   import chain, imap
from   collections import defaultdict
import sys
from   copy import deepcopy

class TemplateState_Entry(Entry):
    def __init__(self, StateIndex, StateIndexToStateKeyDB, *EntryList):
        Entry.__init__(self, StateIndex, [])
        for entry in EntryList:
            self.update(entry, StateIndexToStateKeyDB)

        Entry.door_tree_configure(self, StateIndex)

        self.__door_id_replacement_db = self.__get_door_replacement_db(EntryList)

    @property
    def door_id_replacement_db(self):
        return self.__door_id_replacement_db

    def __get_door_replacement_db(self, EntryList):
        """Get the replacements of any involved door in the entry list
           and translate it into a door of this entry.
        """
        result = {}
        for entry in EntryList:
            for transition_id, door_id in entry.door_db.iteritems():
                result[door_id] = self.door_db[transition_id]
        return result

    def update(self, TheEntry, StateIndexToStateKeyDB):
        """Include 'TheState.entry.action_db' into this state. That means,
           that any mapping:
           
                transition (StateIndex, FromStateIndex) --> CommandList 

           is absorbed in 'self.__action_db'. Additionally, any command list
           must contain the 'SetTemplateStateKey' command that sets the state key for
           TheState. At each (external) entry into the Template state the
           'state_key' must be set, so that the template state can operate
           accordingly.  
        """
        for transition_id, action in TheEntry.action_db.iteritems():
            clone     = action.clone()
            if transition_id.state_index == transition_id.from_state_index: 
                # Recursion of a state will be a recursion of the template state.
                #   => The state_key does not have to be set (again) at entry.
                #   => With the "door_tree_configure()" comes an elegant consequence:
                # 
                # ALL RECURSIVE TARGETS INSIDE THE TEMPLATE WILL ENTER THROUGH THE
                # SAME DOOR, AS LONG AS THEY DO THE SAME THING. 
                # 
                # RECURSION WILL BE A SPECIAL CASE OF 'SAME DOOR' TARGET WHICH HAS 
                # NOT TO BE DEALT WITH SEPARATELY.
                pass
            else:
                # Not recursive => add control command 'SetTemplateStateKey'
                #
                # Determine 'state_key' (an integer value) for state that is
                # entered.  Since TheState may already be a template state, use
                # 'transition_id.state_index' to handle already absorbed states
                # correctly.
                state_key = StateIndexToStateKeyDB[transition_id.state_index]
                for command in clone.command_list.misc:
                    if not isinstance(command, SetTemplateStateKey): continue
                    # Adapt the existing 'SetTemplateStateKey' command
                    command.set_value(state_key)
                    break
                else:
                    # Create new 'SetTemplateStateKey' for current state
                    clone.command_list.misc.add(SetTemplateStateKey(state_key))

            self.action_db[transition_id] = clone

class TemplateState(AnalyzerState):
    """A TemplateState is a state that is implemented to represent multiple
       states.  Tt implements the general scheme and keeps track of the
       particularities. The TemplateState is constructed by 

       The template states are combined successively by the combination of 
       two states where each one of them may also be a TemplateState. The
       combination happens by means of the functions:
       
          self.__update_entry(...)  Which takes over the mappings from 
                                    transition_id to command list. Also, 
                                    it adds the 'SetTemplateStateKey' for each
                                    entry.

          combine_maps(...) which combines the transition maps of the 
                            two states into a single transition map that
                            may contain TargetScheme-s. 
                               
          combine_drop_out_scheme(...) which combines DropOut and Entry schemes
                                       of the two states.

       Notably, the derived class TemplateStateCandidate takes an important
       role in the construction of the TemplateState.
    """
    def __init__(self, StateA, StateB, TheAnalyzer):
        # The 'index' remains None, as long as the TemplateState is not an 
        # accepted element of a state machine. This makes sense, in particular
        # for TemplateStateCandidates (derived from TemplateState). 
        AnalyzerState.set_index(self, index.get())

        self.__analyzer             = TheAnalyzer
        self.__state_index_list     = get_state_list(StateA) + get_state_list(StateB)
        state_index_to_state_key_db = dict((state_index, i) for i, state_index in enumerate(self.__state_index_list))

        # Combined DropOut and Entry schemes are generated by the same function
        self.__entry    = TemplateState_Entry(self.index, state_index_to_state_key_db, StateA.entry, StateB.entry)
                                          
        self.__drop_out = combine_drop_out_scheme(get_state_list(StateA), StateA.drop_out, 
                                                  get_state_list(StateB), StateB.drop_out)

        # Adapt the door ids of the transition maps and bring them all into a form of 
        #   (interval --> TargetScheme)
        tm_a = self.__get_adapted_transition_map(StateA)
        tm_b = self.__get_adapted_transition_map(StateB)

        self.__transition_map,    \
        self.__target_scheme_list = combine_maps(StateA, tm_a, StateB, tm_b)

        # Compatible with AnalyzerState
        # (A template state can never mimik an init state)
        self.__engine_type = StateA.engine_type
        self.input         = get_input_action(StateA.engine_type, InitStateF=False)

    @property
    def engine_type(self):         return self.__engine_type
    @property
    def init_state_f(self):        return False
    @property
    def transition_map(self):      return self.__transition_map
    @property
    def target_scheme_list(self):  return self.__target_scheme_list
    @property
    def state_index_list(self):    return self.__state_index_list
    @property
    def implemented_state_index_list(self):    return self.__state_index_list
    @property
    def entry(self):               return self.__entry
    @property
    def uniform_drop_outs_f(self): 
        return len(self.__drop_out) == 1
    @property
    def drop_out(self):            return self.__drop_out

    def state_set_iterable(self, StateIndexList, TheAnalyzer):
        return imap(lambda i: 
                    (i,                                # state_index
                     self.state_index_list.index(i),   # 'state_key' of state (in array)
                     TheAnalyzer.state_db[i]),         # state object
                    StateIndexList)

    def __get_local_door_id(self, StateIndex, FromStateIndex):
        """If the target state is implemented in this template, then return 
           a locally implemented door. Otherwise, we return a 'standard door'
           of the original states. Later they may be replaced with the 
           doors of their mega states, if they are implemented elsewhere.
        """
        door_id = self.entry.get_door_id(StateIndex, FromStateIndex)
        if door_id is not None:
            # We implement the 'StateIndex' so return a local door from the template
            return door_id
        # Return the 'standard door' of state 'StateIndex' from outside the template
        return self.__analyzer.state_db[StateIndex].entry.get_door_id(StateIndex, FromStateIndex)

    def __get_adapted_transition_map(self, State):
        def adapt(Target):
            """Transitions to states are transformed into transitions to TargetSchemes.
               That is intervals are associated with 'doors' instead of target states.
            """
            if Target == E_StateIndices.DROP_OUT: 
                return TargetScheme(E_StateIndices.DROP_OUT)
            else:
                return self.__get_local_door_id(State.index, Target)

        def adapt_TargetScheme(Target):
            """A transition_map can refer to local door ids, as they are implemented
               by this template, or standard door_ids of 'normal original states'.
               Thus, transitions of an existing template, must de-translated door ids
               that relate to itself, and associate transitions to states which are
               implemented here with local door ids.
            """
            def __adapt(door_id):
                transition_id = TState.entry.transition_db[DoorId]
                new_door_id   = self.__get_local_door_id(transition_id.state_index, transition_id.from_state_index)
                door_id.state_index      = new_door_id.state_index
                door_id.from_state_index = new_door_id.from_state_index

            if Target.drop_out_f:    
                return Target
            clone = deepcopy(Target)
            if clone.door_id is not None:  
                __adapt(clone.door_id)
            else:
                for door_id in clone.scheme:
                    __adapt(door_id)
            return clone

        if isinstance(State, AnalyzerState):
            return [(interval, adapt(target))              for interval, target in State.transition_map ]
        else:
            return [(interval, adapt_TargetScheme(target)) for interval, target in State.transition_map ]

    def replace_door_ids_in_transition_map(self, ReplacementDB):
        """ReplacementDB:    DoorID --> Replacement DoorID

           The Existence of MegaStates has the consequence that transitions
           have to be adapted. Let 'X' be a state that has been absorbed by 
           a MegaState 'M'. Then a transition from another state 'Y' to 'X' is 
           originally associated with DoorID 'Dyx'. Since 'X' is now part
           of a MegaState, the transition 'from Y to X' has been associated
           with the DoorID 'Dyxm' which is the MegaState's entry that represents
           'from Y to X'. Any transition 'Dyx' must now be replaced by 'Dyxm'.
        """
        for interval, target in self.__transition_map:
            if target.drop_out_f: continue
            target.door_id_replacement(ReplacementDB)

def combine_drop_out_scheme(StateIndexListA, A, StateIndexListB, B):
    """A 'scheme' is a dictionary that maps:
             
         (1)       map: object --> state_index_list 

       where for each state referred in state_index_list it holds

         (2)            state.object == object

       For example, if four states 1, 4, 7, and 9 have the same drop_out 
       behavior DropOut_X, then this is stated by an entry in the dictionary as

         (3)       { ...     DropOut_X: [1, 4, 7, 9],      ... }

       For this to work, the objects must support a proper interaction 
       with the 'dict'-objects. Namely, they must support:

         (4)    __hash__          --> get the right 'bucket'.
                __eq__ or __cmp__ --> compare elements of 'bucket'.

       The dictionaries are implemented as 'defaultdict(list)' so that 
       the state index list can simply be 'extended' from scratch.

       NOTE: This type of 'scheme', as mentioned in (1) and (2) is suited 
             for DropOut and EntryObjects. It is fundamentally different 
             from a TargetScheme T of transition maps, where T[state_key] 
             maps to the target state of state_index_list[state_key].
    """
    # A and B can be 'objects' or dictionaries that map 'object: -> state_index_list'
    # where the 'state_index_list' is the set of states that have the 'object'.
    A_iterable = get_iterable(A, StateIndexListA)
    B_iterable = get_iterable(B, StateIndexListB)
    # '*_iterable' represent lists of pairs '(object, state_index_list)' 

    result = defaultdict(list)
    for element, state_index_list in chain(A_iterable, B_iterable):
        assert hasattr(element, "__hash__")
        assert hasattr(element, "__eq__")
        result[element].extend(state_index_list)

    return result

def combine_maps(StateA, AdaptedTM_A, StateB, AdaptedTM_B):
    """RETURNS:

          -- Transition map = combined transition map of StateA and StateB.

          -- List of target schemes that have been identified.

       NOTE: 

       If the entries of both states are uniform, then a transition to itself
       of both states can be implemented as a recursion of the template state
       without knowing the particular states.

       EXPLANATION:
    
       This function combines two transition maps. A transition map is a list
       of tuples:

            [
              ...
              (interval, target)
              ...
            ]

       Each tuple tells about a character range [interval.begin, interval.end)
       where the state triggers to the given target. In a normal AnalyzerState
       the target is the index of the target state. In a TemplateState, though,
       multiple states are combined. A TemplateState operates on behalf of a
       state which is identified by its 'state_key'. 
       
       If two states (even TemplateStates) are combined the trigger maps
       are observed, e.g.

            Trigger Map A                    Trigger Map B
                                                                          
            [                                [
              ([0,  10),   DropOut)            ([0,  10),   State_4)
              ([10, 15),   State_0)            ([10, 15),   State_1)
              ([15, 20),   DropOut)            ([15, 20),   State_0)
              ([20, 21),   State_1)            ([20, 21),   DropOut)
              ([21, 255),  DropOut)            ([21, 255),  State_0)
            ]                                ]                           


       For some intervals, the target is the same. But for some it is different.
       In a TemplateState, the intervals are associated with TargetScheme 
       objects. A TargetScheme object tells the target state dependent
       on the 'state_key'. The above example may result in a transition map
       as below:

            Trigger Map A                   
                                                                          
            [     # intervals:   target schemes:                           
                  ( [0,  10),    { A: DropOut,   B: State_4, },
                  ( [10, 15),    { A: State_0,   B: State_1, },
                  ( [15, 20),    { A: DropOut,   B: State_0, },
                  ( [20, 21),    { A: State_1,   B: DropOut, },
                  ( [21, 255),   { A: DropOut,   B: State_0, },
            ]                                                           

       Note, that the 'scheme' for interval [12, 20) and [21, 255) are identical.
       We try to profit from it by storing only it only once. A template scheme
       is associated with an 'index' for reference.

       TemplateStates may be combined with AnalyzerStates and other TemplateStates.
       Thus, TargetSchemes must be combined with trigger targets
       and other TargetSchemes.

       NOTE:

       The resulting target map results from the combination of both transition
       maps, which may introduce new borders, e.g.
    
                     |----------------|           (where A triggers to X)
                          |---------------|       (where B triggers to Y)

       becomes
                     |----|-----------|---|
                        1       2       3

       where:  Domain:     A triggers to:     B triggers to:
                 1              X               Nothing
                 2              X                  Y
                 3           Nothing               Y

    -----------------------------------------------------------------------------
    Transition maps of TemplateState-s function based on 'state_keys'. Those state
    keys are used as indices into TemplateTargetSchemes. The 'state_key' of a given
    state relates to the 'state_index' by

        (1)    self.state_index_list[state_key] == state_index

    where 'state_index' is the number by which the state is identified inside
    its state machine. Correspondingly, for a given TemplateTargetScheme T 

        (2)                   T[state_key]

    gives the target of the template if it operates for 'state_index' determined
    from 'state_key' by relation (1). The state index list approach facilitates the
    computation of target schemes. For this reason no dictionary
    {state_index->target} is used.
    """
    def __help(TM):
        assert_adjacency(TM, TotalRangeF=True)
        return TM, len(TM)

    TransitionMapA, LenA = __help(AdaptedTM_A)
    TransitionMapB, LenB = __help(AdaptedTM_B)

    i  = 0 # iterator over TransitionMapA
    k  = 0 # iterator over TransitionMapB

    # Intervals in trigger map are always adjacent, so the '.begin' member is
    # not required.
    scheme_db = TargetSchemeDB(StateA, StateB)
    result    = []
    prev_end  = - sys.maxint
    while not (i == LenA - 1 and k == LenB - 1):
        i_trigger = TransitionMapA[i]
        i_end     = i_trigger[0].end
        i_target  = i_trigger[1]

        k_trigger = TransitionMapB[k]
        k_end     = k_trigger[0].end
        k_target  = k_trigger[1]

        end       = min(i_end, k_end)
        target    = scheme_db.get_target(i_target, k_target)
        assert isinstance(target, TargetScheme)

        result.append((Interval(prev_end, end), target))
        prev_end  = end

        if   i_end == k_end: i += 1; k += 1;
        elif i_end <  k_end: i += 1;
        else:                k += 1;

    # Treat the last trigger interval
    target = scheme_db.get_target(TransitionMapA[-1][1], TransitionMapB[-1][1])

    result.append((Interval(prev_end, sys.maxint), target))

    return result, scheme_db.get_scheme_list()

class TargetScheme(object):
    """A target scheme contains the information about what the target
       state is inside an interval for a given template key. For example,
       a given interval X triggers to target scheme T, i.e. there is an
       element in the transition map:

                ...
                [ X, T ]
                ...

       then 'T.scheme[key]' tells the 'door id' of the door that is entered
       for the case the operates with the given 'key'. A key in turn, stands 
       for a particular state.

       There might be multiple intervals following the same target scheme,
       so the function 'TargetSchemeDB.get()' takes care of making 
       those schemes unique.

           .scheme = Target state index scheme as explained above.

           .index  = Unique index of the target scheme. This value is 
                     determined by 'TargetSchemeDB.get()'. It helps
                     later to define the scheme only once, even it appears
                     twice or more.
    """
    __slots__ = ('__index', '__scheme', '__drop_out_f', '__door_id', '__scheme')

    def __init__(self, Target, UniqueIndex=None):
        if UniqueIndex is not None: 
            assert isinstance(Target, tuple)
        else:
            assert    isinstance(Target, DoorID) \
                   or Target == E_StateIndices.DROP_OUT 

        self.__index       = UniqueIndex

        self.__drop_out_f  = False
        self.__door_id     = None
        self.__scheme      = None

        if   Target == E_StateIndices.DROP_OUT:  self.__drop_out_f  = True;   assert UniqueIndex is None
        elif isinstance(Target, DoorID):         self.__door_id     = Target; assert UniqueIndex is None
        elif isinstance(Target, tuple):          self.__scheme      = Target; assert UniqueIndex is not None

    @property
    def scheme(self):      return self.__scheme

    @property
    def door_id(self):     return self.__door_id

    def door_id_replacement(self, ReplacementDB):
        def replace_if_required(DoorId):
            replacement = ReplacementDB.get(DoorId)
            if replacement is not None: return replacement
            return DoorId

        if self.__door_id is not None:
            new_door_id = ReplacementDB.get(self.__door_id)
            if new_door_id is not None:
                self.__door_id = new_door_id
        else:
            self.__scheme = tuple(replace_if_required(door_id) for door_id in self.__scheme)

    @property
    def drop_out_f(self):  return self.__drop_out_f

    @property
    def index(self):       return self.__index

    def __repr__(self):
        if   self.drop_out_f:          return "TargetScheme:DropOut"
        elif self.door_id is not None: return "TargetScheme:(%s)" % repr(self.__door_id)
        elif self.scheme  is not None: return "TargetScheme:(%s)" % repr(self.__scheme)
        else:                          return "TargetScheme:<ERROR>"

    def __hash__(self):
        return self.__index

    def __eq__(self, Other):
        if isinstance(Other, TargetScheme) == False: return False
        ## if self.__index != Other.__index: return False
        return self.__scheme == Other.__scheme

class TargetSchemeDB(dict):
    """A TargetSchemeDB keeps track of existing target state combinations.
       If a scheme appears more than once, it does not get a new index. By means
       of the index it is possible to avoid multiple definitions of the same 
       scheme, later.
    """
    def __init__(self, StateA, StateB):
        dict.__init__(self)
        self.__state_a_state_index_list_length = len(get_state_list(StateA))
        self.__state_b_state_index_list_length = len(get_state_list(StateB))

    def get_TargetScheme(self, SchemeA, SchemeB):
        """Checks whether the combination is already present. If so, the reference
           to the existing target scheme is returned. If not a new scheme is created
           and entered into the database.

           The Targets must be a tuple, such as 

              (1, E_StateIndices.DROP_OUT, 4, ...)

           which tells that if the template operates with

              -- state_key = 0 (first element) there must be a transition to state 1, 
              -- state_key = 1 (second element), then there must be a drop-out,
              -- state_key = 2 (third element), then transit to state 4,
              -- ...
        """
        assert isinstance(SchemeA, tuple)
        assert isinstance(SchemeB, tuple)

        scheme = SchemeA + SchemeB

        for target in scheme:
            assert isinstance(target, DoorID) or target == E_StateIndices.DROP_OUT 

        result = dict.get(self, scheme)
        if result is None: 
            new_index    = len(self)
            result       = TargetScheme(scheme, new_index)
            self[scheme] = result

        return result

    def get_scheme_list(self):
        result = self.values()
        for element in result:
            assert element.scheme is not None
        return self.values()

    def get_target(self, TA, TB):
        print "##:", TA.__class__.__name__, TA
        print "##:", TB.__class__.__name__, TB
        assert isinstance(TA, TargetScheme) 
        assert isinstance(TB, TargetScheme) 

        if TA.drop_out_f:
            if TB.drop_out_f:
                return TA
            TA_scheme = (E_StateIndices.DROP_OUT,) * self.__state_a_state_index_list_length

        elif TA.door_id is not None:
            if TB.door_id is not None and TA.scheme == TB.scheme:
                return TA
            TA_scheme = (TA.door_id,) * self.__state_a_state_index_list_length

        else:
            TA_scheme = TA.scheme

        if TB.drop_out_f:
            # TA was not drop-out, otherwise we would have returned earlier
            TB_scheme = (E_StateIndices.DROP_OUT,) * self.__state_b_state_index_list_length

        elif TB.door_id is not None:
            # TA was not the same door, otherwise we would have returned earlier
            TB_scheme = (TB.door_id,) * self.__state_b_state_index_list_length

        else:
            TB_scheme = TB.scheme

        return self.get_TargetScheme(TA_scheme, TB_scheme)

def get_state_list(X): 
    if isinstance(X, TemplateState): return X.state_index_list 
    else:                            return [ X.index ]

def get_iterable(X, StateIndexList): 
    if isinstance(X, defaultdict): return X.iteritems()
    else:                          return [(X, StateIndexList)]

