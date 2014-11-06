from quex.blackboard import E_IncidenceIDs, \
                            E_PreContextIDs, \
                            E_IncidenceIDs_SubsetAcceptanceIDs

class StateOperation(object): 
    """A StateOperation tells about a state how it should behave in a state
       machine that represents one single isolated pattern. This is in 
       contrast to a state machine that consists of a conglomerate of 
       patterns combined into a single machine.

       Such a state of an isolated pattern needs has the following
       actions related to attributes:

       -- acceptance_f:

          (if True) When the state is hit, then it 'accepts'. This means that a
          pattern  has matched. 
    
       -- pre_context_id:

          (if True) it says that acceptance is only valid, if the given 
          pre-context is fulfilled.

       Pre contexts are checked by a backward analysis before the actual forward
       analysis. In the frame of this backward analysis matched pre-contexts raise
       a flag as soon as a pre-context is fulfilled. Those flags are checked if the 
       'pre_context_id' is not NONE.

       Post contexts are appended to the pattern. For example 'hello/world' is
       a pattern that matches 'hello' if it is followed by 'world'. This is
       implemented by a single concatenated state machine that matches
       'helloworld'. When acceptance is reached, though, it goes back to where
       'hello' ended its match. Consequently, there are states were the input
       position has to be stored, and others where the input position has to be
       restored. Of course, the restoring of input positions makes only sense
       in acceptance states. The storing of input positions, then makes only 
       sense in non-acceptance states. Otherwise, storing and restoring would 
       happen in the same state and therefore be superfluous.

       -- store_input_position_store_f:

          When the state is hit, the input position has to be stored. 
          Such a state can never be an acceptance state. 
          
       -- input_position_restore_f:

          When the state is hit the input position has to be restored. 
          Such a state **must** be an acceptance state.

       Some post contexts cannot be addressed by simple storing and restoring
       of input positions. They require a backward search. Such cases are 
       indicated by the following flag. In this case, the pattern's object
       contains a flag that tells 'backward input position search' required.
      _________________________________________________________________________

      NOTE: Again, objects of this type describe the behavior of a state 
            in a single isolated state machine, designed to match one single
            pattern. 

      The exact behavior of a state in a 'melted' state machine is derived from 
      lists of these objects by track analysis.
    """    
    __slots__ = ("__pattern_id", "state_index", 
                 "__acceptance_f", 
                 "__pre_context_id", 
                 "__input_position_store_f",
                 "__input_position_restore_f")

    def __init__(self, AcceptanceID, StateIndex, AcceptanceF, 
                 StoreInputPositionF=False, 
                 PreContextID=E_PreContextIDs.NONE,
                 RestoreInputPositionF=False):
        assert type(StateIndex)  == long
        assert type(AcceptanceF) == bool
        assert type(StoreInputPositionF) == bool
        assert type(RestoreInputPositionF) == bool
        assert AcceptanceID in E_IncidenceIDs_SubsetAcceptanceIDs or (isinstance(AcceptanceID, long)    and AcceptanceID >= 0) 
        assert PreContextID in E_PreContextIDs or (isinstance(PreContextID, long) and PreContextID >= 0), PreContextID

        if AcceptanceF: assert not StoreInputPositionF 
        else:           assert PreContextID == E_PreContextIDs.NONE
               
        # NOT: AcceptanceID != E_IncidenceIDs.MATCH_FAILURE => AcceptanceF == False
        #      State core info objects are also used for non-acceptance states of patterns
        self.__pattern_id = AcceptanceID
        self.state_index  = StateIndex

        self.__acceptance_f             = AcceptanceF 
        self.__input_position_store_f   = StoreInputPositionF
        self.__input_position_restore_f = RestoreInputPositionF
        self.__pre_context_id           = PreContextID  

    def clone(self, StateIndex=None, ReplDbPreContext=None, ReplDbAcceptance=None):
        if StateIndex is not None: state_index = StateIndex
        else:                      state_index = self.state_index

        # Perform optional replacements
        def produce(DB, Value, TheEnum):
            if Value  not in TheEnum and DB is not None: return DB[Value]
            else:                                        return Value

        return StateOperation(produce(ReplDbAcceptance, self.__pattern_id, E_IncidenceIDs_SubsetAcceptanceIDs), 
                             state_index, 
                             self.__acceptance_f,
                             self.__input_position_store_f,
                             produce(ReplDbPreContext, self.__pre_context_id, E_PreContextIDs),
                             self.__input_position_restore_f)

    def merge(self, Other):
        # It **DOES** make any sense to merge to state cores from different
        # state machines. This should NOT be an 'assert'. In the final state machine
        # more than one state machine is combined in parallel and then they belong 
        # to the same state machine
        # if self.__pattern_id != Other.__pattern_id: return

        if Other.__acceptance_f:                 
            self.__acceptance_f = True
            self.__input_position_store_f = False

        if Other.__pre_context_id != E_PreContextIDs.NONE:    
            self.__pre_context_id  = Other.__pre_context_id 

        if self.__acceptance_f:
            # 'restore' makes only sense on acceptance states
            if Other.__input_position_restore_f: self.__input_position_restore_f = True
        else:
            # 'store' makes only sense on non-acceptance states
            if Other.__input_position_store_f:   self.__input_position_store_f = True

        # It does not make sense to store and restore the input position at the same place
        if self.__input_position_store_f and self.__input_position_restore_f:
            self.__input_position_store_f = False
            self.__input_position_restore_f = False

        # NOTE: 'store' + 'restore' = no storage at all.
        #if Other.__input_position_store_f:
        #    if self.__input_position_restore_f: self.__input_position_restore_f = False  # 'store' + 'restore'
        #    else:                               self.__input_position_store_f   = True
        #if Other.__input_position_restore_f: 
        #    if self.__input_position_store_f: self.__input_position_store_f   = False    # 'store' + 'restore'
        #    else:                             self.__input_position_restore_f = True
        #
        #if Other.__pre_context_id != E_PreContextIDs.NONE:    
        #    self.__pre_context_id  = Other.__pre_context_id 

    def acceptance_id(self):
        return self.__pattern_id

    def set_pattern_id(self, AcceptanceID):
        assert    AcceptanceID in E_IncidenceIDs_SubsetAcceptanceIDs \
               or (isinstance(AcceptanceID, long) and AcceptanceID >= 0) 
        self.__pattern_id = AcceptanceID

    def is_acceptance(self):
        return self.__acceptance_f

    def set_acceptance_f(self, Value):
        assert type(Value) == bool
        # 'PreContextID', 'RestorePosition' can only be active if acceptance is True.
        # (May be, de-activate pre-context first)
        if Value == False: 
            assert self.__pre_context_id == E_PreContextIDs.NONE
            assert not self.__input_position_store_f
        self.__acceptance_f = Value

    def input_position_store_f(self):
        if self.__input_position_store_f: assert self.__input_position_restore_f == False
        if self.__acceptance_f:           assert self.__input_position_store_f == False
        return self.__input_position_store_f    

    def input_position_restore_f(self):
        return self.__input_position_restore_f

    def set_input_position_restore_f(self, Value=True):
        assert type(Value) == bool
        # 'Restore Position' can only be active if acceptance is True.
        # (May be, activate acceptance first)
        if Value == True: assert self.__acceptance_f
        self.__input_position_restore_f = Value
        
    def set_input_position_store_f(self, Value=True):
        assert type(Value) == bool
        if Value == True: assert self.__acceptance_f == False
        self.__input_position_store_f = Value

    def set_pre_context_id(self, Value=True):
        assert Value in E_PreContextIDs or (type(Value) == long and Value >= 0)
        # PreContextID can only be active if acceptance is True.
        # (May be, activate acceptance first)
        if Value == True: assert self.__acceptance_f
        self.__pre_context_id = Value

    def pre_context_id(self):
        return self.__pre_context_id  

    def __cmp__(self, Other):
        assert False
            
    def __repr__(self):
        return self.get_string()

    def get_string(self):
        def annotate(Str, PatternId):
            if PatternId == E_IncidenceIDs.MATCH_FAILURE:
                return Str
            return "%s%s" % (Str, PatternId)

        attribute_list = []
        if self.__acceptance_f:        
            acceptance_id_txt = ""
            pre_txt           = ""
            restore_txt       = ""
            if self.__pattern_id != E_IncidenceIDs.MATCH_FAILURE:
                acceptance_id_txt = repr(self.__pattern_id).replace("L", "")
            if self.__pre_context_id != E_PreContextIDs.NONE:            
                if self.__pre_context_id == E_PreContextIDs.BEGIN_OF_LINE:
                    pre_txt = "pre=bol"
                else: 
                    pre_txt = "pre=%s" % repr(self.__pre_context_id).replace("L", "")
            if self.__input_position_restore_f: 
                restore_txt = annotate("R", self.__pattern_id)

            txt = [ x for x in (acceptance_id_txt, pre_txt, restore_txt) if x ]
            if txt: txt_str = "A(%s)" % reduce(lambda x, y: "%s,%s" % (x,y), txt)
            else:   txt_str = "A"

            attribute_list.append(txt_str)

        else:
            assert not self.__input_position_restore_f

        if self.__input_position_store_f:   
            attribute_list.append(annotate("S", self.__pattern_id))

        # Attributes happen to be sorted alpabetically, to make the output more stable
        # Thus, "attribute_list.sort()" --> not necessary (yet)

        if attribute_list: return reduce(lambda x,y: "%s,%s" % (x,y), attribute_list)
        else:              return ""

