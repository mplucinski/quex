# (C) 2010 Frank-Rene Schaefer
"""
   Template Compression _______________________________________________________

   The idea behind 'template compression' is to combine the transition maps of
   multiple similar states into a single transition map. The difference in the
   transition maps are dealt with by an adaption table. For example the three
   states

         .---- 'a' --> 2        .---- 'a' --> 2        .---- 'a' --> 2
         |                      |                      |
       ( A )-- 'e' --> 0      ( B )-- 'e' --> 1      ( C )-- 'e' --> 2
         |                      |                      |
         `---- 'x' --> 5        `---- 'x' --> 5        `---- 'y' --> 5

   can be combined into a single template state

                         .----- 'a' --> 2 
                         |               
                      ( T1 )--- 'e' --> Target0 
                         |\               
                         \  `-- 'x' --> Target1
                          \
                           `--- 'y' --> Target2

   where the targets Target0, Target1, and Target2 are adapted. If the template
   has to mimik state A then Target0 needs to be 1, Target1 is 5, and Target2
   is 'drop-out'. The adaptions can be stored in a table:

                                A     B     C
                       Target0  0     1     2
                       Target1  5     5     drop
                       Target2  drop  drop  5

   Practically, this means that a 'goto state' is transformed into a 'set state
   key' plus a 'goto template'. The state key tells which column of the table
   is to be used in the transition map. Thus, a state that is implemented in a
   template is identified by 'template index' and 'state key', i.e.

            templated state <--> (template index, state key)

   The combination of multiple states reduces memory consumption. The
   efficiency increases with the similarity of the transition maps involved.
   The less differences there are in the trigger intervals, the less additional
   intervals need to be added. The less differences there are in target states,
   the less information needs to be stored in adaption tables.

   Result ______________________________________________________________________


   The result of analyzis of template state compression is:
    
              A list of 'TemplateCombination' objects. 

   A TemplateCombination carries:
   
     -- a trigger map, i.e. a list of intervals together with target state
        lists to which they trigger. If there is only one associated target
        state, this means that all involved states trigger to the same target
        state.

     -- a list of involved states. A state at position 'i' in the list has
        the state key 'i'. It is the key into the adaption table mentioned
        above.

   Algorithm __________________________________________________________________

   Not necessarily all states can be combined efficiently with each other. The
   following algorithm finds successively best combinations and stops when no
   further useful combinations can be found. The algorithm works as follows:

      (1) Determine for each possible pair of transition maps a value that
          represents the expected 'gain' if they were combined.

      (2.a) If there is no possitive gain possible, break up.

      (2.b) Else, for the best pair, create a TemplateCombination that
            incorporates both transition maps. Include the TemplateCombination
            as transition map in the following considerations.

            Goto (1)

   Measurement of the 'Gain Value' ____________________________________________

   The 'gain' shall **represent** the amount of memory that can be spared if
   two trigger maps are combined. The number does not necessarily relate
   directly to a physical byte consumption. Moreover, it is only required, that
   if a combination of (A, B) spares more than a combination of (C, D) then
   the gain value of (A, B) must be greater than the gain value for (C, D).

   The measurement of 'gain' is done in two steps:

       (1) get_metric(A, B): computes the number of borders of a
           transition map that would combine the two trigger
           maps A and B. Also, it combines the number of target
           set combinations, i.e. the number of X0, X1, X3 ...
           in the example above.

       (2) get_delta_cost(...): computes a scalar value that indicates
           the 'gain' in terms of program space, if the two trigger
           maps are combined. This function is controlled by the
           coefficient 'CX' that indicates the ratio between the
           'normal cost' of transition and the cost of routing, i.e.
           entering the right target state according to the adapted
           trigger map.

   both functions work with normal state trigger maps and objects of class
   TemplateCombination.

   Class TemplateCombination __________________________________________________

   Combined trigger maps are stored in objects of type 'TemplateCombination'.
   As normal trigger maps they are built of a list of tuples:

              (I0, TL0), (I1, TL1), .... (In, TLn)

   where the intervals I0 to In are adjacent intervals starting with 

              I0.begin == - sys.maxint

   and ending with 

              In.end   == sys.maxint

   In 'normal trigger maps' the target state indices TL0 to TLn are scalar
   values. In a 'TemplateCombination' object, the 'target' can be a scalar
   value or a list. Accordingly, this means that TLk is

        a scalar, if Ik maps to the same target state for all involved 
                  states.

                  If TLk == TARGET_RECURSIVE, then all involved states
                  trigger recursively.

        a list, if Ik maps to different target states for each involved
                state. Then, Tlk[i] is the target state to which the 
                state with key 'i' triggers.  

   The state key has been mentioned above. It designates the column in the
   adaption table that is required for each state involved.

"""
import sys
from copy import copy
from quex.core_engine.interval_handling import Interval
import quex.core_engine.state_machine.index as index
import quex.core_engine.state_machine.core  as state_machine

def do(sm, CostCoefficient):
    """
       sm:              StateMachine object containing all states

                        NOTE: The init state is **never** part of a template 
                              combination.

       CostCoefficient: Coefficient that indicates how 'costy' it is differentiate
                        between target states when it is different in states that
                        are combined into a template. Meaningful range: 0 to 3.

       RETURNS: List of template combinations.
    """
    trigger_map_db = TriggerMapDB(sm)

    # Build templated combinations by finding best pairs, until there is no meaningful way to
    # build any clusters. TemplateCombinations of states also take part in the race.
    while 1 + 1 == 2:
        i, k = trigger_map_db.get_best_matching_pair()
        if i == None: break

        # Add new element: The combined pair
        new_sm_index = index.get_state_machine_id()
        trigger_map_db[new_sm_index] = get_combined_trigger_map(trigger_map_db[i], 
                                                                involved_state_list(trigger_map_db[i], i),
                                                                trigger_map_db[k], 
                                                                involved_state_list(trigger_map_db[k], k))
        # Delete the two states that have now been combined.
        trigger_map_db.delete_pair(i, k) 

    result = []
    for state_index, combination in trigger_map_db.items():
        if isinstance(combination, TemplateCombination): result.append(combination)

    return result

TARGET_RECURSIVE = -2L # 'Normal' targets are greater than zero
class TemplateCombination:
    def __init__(self, InvolvedStateList0,  InvolvedStateList1):
        self.__trigger_map         = []
        self.__involved_state_list = InvolvedStateList0 + InvolvedStateList1

    def involved_state_list(self):
        return self.__involved_state_list

    def append(self, Begin, End, TargetStateIdxList):
        """TargetStateIdxList can be
        
            A list of (long) integers: List of targets where

                list[i] == target index of involved state number 'i'

            A scalar value:

                i)  > 0, then all involved states trigger to this same
                         target index.
                ii) == TARGET_RECURSIVE, then all involved states are 
                                         recursive.
        """
        self.__trigger_map.append([Interval(Begin, End), TargetStateIdxList])

    def __getitem__(self, Index):
        return self.__trigger_map[Index]

    def __len__(self):
        return len(self.__trigger_map)

    def __repr__(self):
        txt = []
        for trigger in self.__trigger_map:
            txt.append("[%i, %i) --> %s\n" % \
                       (trigger[0].begin, trigger[0].end, trigger[1]))
        return "".join(txt)

    def get_trigger_map(self):
        return self.__trigger_map

def get_delta_cost(SizeA, SizeB, N, CombinedBorderN, TargetCombinationN, CX=1):
    """SizeA, SizeB       = number of borders in target map A and B
       N                  = total number of combined states.
       CombinedBorderN    = number of borders in the combined map.
       TargetCombinationN = number of different target state combinations.

       CX = the calculation coefficient as explained below:
    
    
       BEFORE: 
                Cost0 = (SizeA + SizeB) * CI

                where CI is the average 'identification cost', i.e. the
                cost for branching through the 'if/else' statements of 
                the transition map, plus the cost for a goto.

       AFTER:
                Cost1 =   SameTargetN * CI
                        + TargetCombinationN * N * CR

                where SameTargetN = CombinedBorderN - TargetCombinationN
                                    the number of intervals that trigger to
                                    the same target in both maps.
                      CR is the cost for routing, i.e. jumping to
                         the correct target state depending on template.
                      N the number of involved states must be multiplied because
                        for each state there must be a 'switch case'.

       THUS:    
                Delta = Cost0 - Cost1

                      = (SizeA + SizeB - (CombinedBorderN - TargetCombinationN)) * CI
                         - TargetCombinationN * N * CR

                Delta shall be a 'measure', so there is no loss of 
                information if we devide by a constant, e.g. CI. Thus

                .-------------------------------------------------------------------.
                | Delta =   (SizeA + SizeB - CombinedBorderN + TargetCombinationN)  |
                |         - CX * TargetCombinationN * N                             |
                '-------------------------------------------------------------------'

                Where CX = CR/CI. A big CX means that target state routing is
                expensive, a low CX means, that it is cheap. The constants CI
                and CR where used to express an estimated proportional
                relationship without having a concrete 'physical'
                interpretation.  Now, CI and CR can be replaced by a single
                heuristic value CX.

    """
    return (SizeA + SizeB - CombinedBorderN + TargetCombinationN) - CX * TargetCombinationN * N

class TriggerMapDB:
    def __init__(self, SM, CostCoefficient=1.0):
        assert isinstance(SM, state_machine.StateMachine)

        # (1) Get the trigger maps of all states of the state machine
        self.__db = {}
        for index, state in SM.states.items():
            trigger_map = state.transitions().get_trigger_map()
            # Dead ends, cannot be part of the code generation
            if trigger_map == []: continue
            self.__db[index] = trigger_map

        self.__delta_cost_cache = {}
        self.__cost_coefficient = CostCoefficient

        self.__states           = SM.states
        self.__init_state_index = SM.init_state_index

    def get_best_matching_pair(self):
        """Determines the two trigger maps that are closest to each
           other. The consideration includes the trigger maps of
           combined trigger maps. Thus this function supports the
           clustering of the best trigger maps into combined trigger
           maps.

           If no pair can be found with a gain > 0, then this function
           returns 'None, None'.
        """
        best_a = None 
        best_b = None

        index_list = self.__db.keys()
        L          = len(index_list)
        max_gain   = 0                 # No negative cost allowed
        for i in range(L):
            StateIndexA = index_list[i]
            if StateIndexA == self.__init_state_index: continue

            for k in range(i + 1, L):
                StateIndexB = index_list[k]
                if StateIndexB == self.__init_state_index: continue

                delta_cost = self.__get_delta_cost(StateIndexA, StateIndexB)

                if delta_cost <= max_gain:  continue
                max_gain = delta_cost
                best_a = StateIndexA; best_b = StateIndexB;

        return best_a, best_b

    def __get_delta_cost(self, StateIndexA, StateIndexB):
        delta_cost = self.__delta_cost_cache_get(StateIndexA, StateIndexB)
        if delta_cost != None: return delta_cost

        TriggerMapA = self.__db[StateIndexA]
        SizeA       = len(TriggerMapA)
        TriggerMapB = self.__db[StateIndexB]
        # Get border_n    = number of borders of combined map
        #     eq_target_n = number of equivalent targets, i.e. number of 
        #                   target combinations that need to be routed.
        InvolvedStateListA = involved_state_list(TriggerMapA, StateIndexA)
        InvolvedStateListB = involved_state_list(TriggerMapB, StateIndexB)
        border_n, eq_target_n = get_metric(TriggerMapA, InvolvedStateListA, 
                                           TriggerMapB, InvolvedStateListB)
        combined_state_n      = len(InvolvedStateListA) + len(InvolvedStateListB)

        delta_cost = get_delta_cost(SizeA, len(TriggerMapB), combined_state_n, 
                                    border_n, len(eq_target_n), 
                                    CX=self.__cost_coefficient)

        self.__delta_cost_cache_set(StateIndexA, StateIndexB, delta_cost)

        return delta_cost

    def __delta_cost_cache_get(self, I, K):
        # Return 'None' if element '(I, K)' is not in cache
        return self.__delta_cost_cache.get(I, {}).get(K)

    def __delta_cost_cache_set(self, I, K, Value):
        # Set dictionary[I][K] = Value
        self.__delta_cost_cache.setdefault(I, {})[K] = Value

    def delete_pair(self, I, K):
        del self.__db[I]
        del self.__db[K]

    def __len__(self):
        return len(self.__db)

    def __getitem__(self, Key):
        assert type(Key) == long
        return self.__db[Key]

    def __setitem__(self, Key, Value):
        assert type(Key) == long
        assert Value.__class__ == TemplateCombination
        self.__db[Key] = Value

    def items(self):
        return self.__db.items()

def involved_state_number(TM):
    if TM.__class__ == TemplateCombination:
        return TM.involved_state_number()
    else:
        return 1

def involved_state_list(TM, DefaultIfTriggerMapIsNotACombination):
    if TM.__class__ == TemplateCombination:
        return TM.involved_state_list()
    else:
        return [ DefaultIfTriggerMapIsNotACombination ]

def is_recursive(TM, Target, InvolvedStateList):
    """Determine whether the target state indicates that the 
       state triggers to itself.
    """
    if TM.__class__ != TemplateCombination:
        # In a 'normal trigger map' the target needs to be equal to the
        # state that it contains.
        assert len(InvolvedStateList) == 1
        return Target == InvolvedStateList[0]
    else:
        # In a trigger map combination, the recursive target is 
        # identifier by the value 'TARGET_RECURSIVE'.
        return Target == TARGET_RECURSIVE

def get_metric(TriggerMap0, InvolvedStateList0, TriggerMap1, InvolvedStateList1):
    """Assume that interval list 0 and 1 are sorted.
       
       RETURNS: -- Number of new borders if both maps are combined.
                -- Number of transitions that trigger to the same 
                   target state on the same interval in both maps.

       The result of this function is later used to feed 'delta_cost' that
       estimates the 'gain' of combining the two maps. 

       If both trigger maps trigger to itself, then this counted as a 
       'same target' since there is no change needed and the template
       triggers to itself.
    """
    Li = len(TriggerMap0)
    Lk = len(TriggerMap1)
    # Count the number of additional intervals if list 0 is combined with list 1
    # Each intersection requires the setup of new intervals, e.g.
    #
    #          |----------------|
    #               |---------------|
    #
    # Requires to setup three intervals in order to cover all cases propperly: 
    #
    #          |----|-----------|---|
    #

    assert TriggerMap0[0][0].begin == -sys.maxint
    assert TriggerMap1[0][0].begin == -sys.maxint
    assert TriggerMap0[-1][0].end  == sys.maxint
    assert TriggerMap1[-1][0].end  == sys.maxint

    equivalent_target_list = []
    def __check_targets(T0, T1):
        # Both trigger to the same target --> no adaption required
        if T0 == T1: return

        # Both trigger to itself --> no adaption required.
        recursion_n = 0
        if is_recursive(TriggerMap0, T0, InvolvedStateList0):
            T0 = InvolvedStateList0
            if len(T0) == 1: T0 = T0[0]
            recursion_n += 1
        if is_recursive(TriggerMap1, T1, InvolvedStateList1): 
            T1 = InvolvedStateList1
            if len(T1) == 1: T1 = T1[0]
            recursion_n += 1
        if recursion_n == 2: return

        # The 'trigger map' may as well be a combination of trigger maps,
        # thus the 'target' may be a list of targets.
        if type(T0) != list: combination = [T0]
        else:                combination = copy(T0)
        if type(T1) == list: combination.extend(T1)
        else:                combination.append(T1)
        if combination not in equivalent_target_list:
            equivalent_target_list.append(combination)

    i = 0 # iterator over interval list 0
    k = 0 # iterator over interval list 1

    # Intervals in trigger map are always adjacent, so the '.end'
    # member is not required.
    border_count_n = 0
    while not (i == Li-1 and k == Lk-1):
        i_trigger = TriggerMap0[i]
        i_end     = i_trigger[0].end
        i_target  = i_trigger[1]

        k_trigger = TriggerMap1[k]
        k_end     = k_trigger[0].end
        k_target  = k_trigger[1]

        __check_targets(i_target, k_target)

        # Step to the next *lowest* border, i.e. increment the 
        # interval line index with the lowest '.end'. For example:
        # 
        #         0   1 2  3 4 5  6   7
        #     i   |     |      |  |   |
        #     k   |   |    | |        |
        #         :   : :  : : :  :   :   (6 intervals, 6 borders)
        #
        #                         i_end:     k_end:
        # Does:  (1) ++i, ++k -->    2            1
        #        (2) ++k      -->    2            3
        #        (3) ++i      -->    5            3
        #        (4) ++k      -->    5            4
        #        (5) ++k      -->    5            6
        #        (6) ++i      -->    6            7
        #        (6) ++i      -->    7            7
        if   i_end == k_end:  i += 1; k += 1;
        elif i_end < k_end:   i += 1;
        else:                 k += 1;

        border_count_n += 1

    # Treat the last trigger interval
    __check_targets(TriggerMap0[-1][1], TriggerMap1[-1][1])

    return border_count_n, \
           equivalent_target_list

def get_combined_trigger_map(TriggerMap0, InvolvedStateList0, TriggerMap1, InvolvedStateList1):
    Li = len(TriggerMap0)
    Lk = len(TriggerMap1)

    InvolvedStateN0 = len(InvolvedStateList0)
    InvolvedStateN1 = len(InvolvedStateList1)

    def __asserts(TM):
        """-- first border at - sys.maxint
           -- all intervals are adjacent (current begin == previous end)
           -- last border at  + sys.maxint
        """
        prev_end = -sys.maxint
        for x in TM:
            assert x[0].begin == prev_end
            prev_end = x[0].end
        assert TM[-1][0].end  == sys.maxint

    __asserts(TriggerMap0)
    __asserts(TriggerMap1)

    def __get_target(T0, T1):
        """In the 'TemplateCombination' trigger map, a transition to the same
           target for all involved states is coded as a scalar value.
           Other combined transitions are coded as list while 

                    list[i] = target index of involved state 'i'

           As soon as the single transition is over, the scalar value
           needs to be expanded, so that the above consensus holds.
        """
        recursion_n = 0
        if is_recursive(TriggerMap0, T0, InvolvedStateList0):
            T0 = InvolvedStateList0
            if len(T0) == 1: T0 = T0[0]
            recursion_n += 1
        if is_recursive(TriggerMap1, T1, InvolvedStateList1): 
            T1 = InvolvedStateList1
            if len(T1) == 1: T1 = T1[0]
            recursion_n += 1

        # If both transitions are recursive, then the template will
        # contain only a 'recursion flag'. Note, that if one state is
        # acceptance than, recursion actually needs to pass the 'set acceptance'
        # part at the state entry. It cannot be recursive.
        if recursion_n == 2 \
           and __no_acceptance(InvolvedStateList0) \
           and __no_acceptance(InvolvedStateList1): 
               return TARGET_RECURSIVE

        if type(T0) == list:
            if type(T1) == list: return T0 + T1
            else:                return T0 + [T1] * InvolvedStateN1
        else:
            if type(T1) == list: return [T0] * InvolvedStateN0 + T1
            elif T0 != T1:       return [T0] * InvolvedStateN0 + [T1] * InvolvedStateN1
            else:                return T0                      # Same Target => Scalar Value

    i = 0 # iterator over interval list 0
    k = 0 # iterator over interval list 1

    # Intervals in trigger map are always adjacent, so the '.end'
    # member is not required.
    result = TemplateCombination(InvolvedStateList0, InvolvedStateList1)
    prev_end = - sys.maxint
    while not (i == Li-1 and k == Lk-1):
        i_trigger = TriggerMap0[i]
        i_end     = i_trigger[0].end
        i_target  = i_trigger[1]

        k_trigger = TriggerMap1[k]
        k_end     = k_trigger[0].end
        k_target  = k_trigger[1]

        target    = __get_target(i_target, k_target)
        end = min(i_end, k_end)
        result.append(prev_end, min(i_end, k_end), target)
        prev_end = end

        if   i_end == k_end:  i += 1; k += 1;
        elif i_end < k_end:   i += 1;
        else:                 k += 1;

    # Treat the last trigger interval
    target = __get_target(TriggerMap0[-1][1], TriggerMap1[-1][1])
    result.append(prev_end, sys.maxint, target)

    return result
