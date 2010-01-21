import quex.core_engine.generator.languages.core                   as languages
import quex.core_engine.generator.state_machine_coder              as state_machine_coder
import quex.core_engine.generator.input_position_backward_detector as backward_detector
from   quex.core_engine.generator.state_machine_decorator          import StateMachineDecorator
from   quex.input.setup import setup as Setup
from   quex.frs_py.string_handling import blue_print
#
from quex.core_engine.generator.base import GeneratorBase

class Generator(GeneratorBase):

    def __init__(self, PatternActionPair_List, 
                 StateMachineName, AnalyserStateClassName, Language, 
                 OnFailureAction, EndOfStreamAction, 
                 ModeNameList, 
                 PrintStateMachineF, StandAloneAnalyserF):

        self.state_machine_name         = StateMachineName
        self.analyzer_state_class_name  = AnalyserStateClassName
        self.programming_language       = Language
        self.language_db                = Setup.language_db
        self.end_of_stream_action       = EndOfStreamAction
        self.on_failure_action          = OnFailureAction
        self.mode_name_list             = ModeNameList
        self.print_state_machine_f      = PrintStateMachineF
        self.stand_alone_analyzer_f     = StandAloneAnalyserF

        GeneratorBase.__init__(self, PatternActionPair_List, StateMachineName)

    def __get_core_state_machine(self):
        LanguageDB = self.language_db 

        assert self.sm.get_orphaned_state_index_list() == []

        #  -- comment all state machine transitions 
        txt = "    " + LanguageDB["$comment"]("state machine") + "\n"
        if self.print_state_machine_f: 
            txt += LanguageDB["$ml-comment"](self.sm.get_string(NormalizeF=False)) + "\n"

        decorated_state_machine = StateMachineDecorator(self.sm, 
                                                        self.state_machine_name, 
                                                        self.post_contexted_sm_id_list, 
                                                        BackwardLexingF=False, 
                                                        BackwardInputPositionDetectionF=False)

        msg = state_machine_coder.do(decorated_state_machine)
        txt += msg

        
        #  -- terminal states: execution of pattern actions  
        txt += LanguageDB["$terminal-code"](decorated_state_machine,
                                            self.action_db, 
                                            self.on_failure_action, 
                                            self.end_of_stream_action, 
                                            self.begin_of_line_condition_f, 
                                            self.pre_context_sm_id_list,
                                            self.language_db) 

        return txt

    def __get_combined_pre_context_state_machine(self):
        LanguageDB = self.language_db

        assert self.pre_context_sm.get_orphaned_state_index_list() == []

        txt = "    " + LanguageDB["$comment"]("state machine for pre-condition test:") + "\n"
        if self.print_state_machine_f: 
            txt += LanguageDB["$ml-comment"](self.pre_context_sm.get_string(NormalizeF=False)) + "\n"

        decorated_state_machine = StateMachineDecorator(self.pre_context_sm, 
                                                        self.state_machine_name, 
                                                        PostContextSM_ID_List=[],
                                                        BackwardLexingF=True, 
                                                        BackwardInputPositionDetectionF=False)

        msg = state_machine_coder.do(decorated_state_machine)

        txt += msg

        txt += LanguageDB["$label-def"]("$terminal-general-bw", True) + "\n"
        # -- set the input stream back to the real current position.
        #    during backward lexing the analyzer went backwards, so it needs to be reset.
        txt += "    QUEX_NAME(Buffer_seek_lexeme_start)(&me->buffer);\n"

        return txt

    def do(self):
        LanguageDB = self.language_db

        #  -- state machines for backward input position detection (pseudo ambiguous post conditions)
        papc_input_postion_backward_detector_functions = ""
        for sm in self.papc_backward_detector_state_machine_list:
            assert sm.get_orphaned_state_index_list() == []
            papc_input_postion_backward_detector_functions +=  \
                  backward_detector.do(sm, LanguageDB, self.print_state_machine_f)

        function_body = ""
        # -- write the combined pre-condition state machine
        if self.pre_context_sm_list != []:
            function_body += self.__get_combined_pre_context_state_machine()
            
        # -- write the state machine of the 'core' patterns (i.e. no pre-conditions)
        function_body += self.__get_core_state_machine()

        # -- pack the whole thing into a function 
        analyzer_function = LanguageDB["$analyzer-func"](self.state_machine_name, 
                                                         self.analyzer_state_class_name, 
                                                         self.stand_alone_analyzer_f,
                                                         function_body, 
                                                         self.post_contexted_sm_id_list, 
                                                         self.pre_context_sm_id_list,
                                                         self.mode_name_list, 
                                                         InitialStateIndex=self.sm.init_state_index,
                                                         LanguageDB=LanguageDB) 

        option_str = ""
        if self.begin_of_line_condition_f: 
            option_str = LanguageDB["$compile-option"]("__QUEX_CORE_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION")

        #  -- paste the papc functions (if there are some) in front of the analyzer functions
        header_str = LanguageDB["$header-definitions"](LanguageDB)
        txt =   option_str                                     \
              + header_str                                     \
              + papc_input_postion_backward_detector_functions \
              + analyzer_function

        return languages.replace_keywords(txt, LanguageDB, NoIndentF=True)

def do(PatternActionPair_List, OnFailureAction, 
       EndOfStreamAction, Language="C++", StateMachineName="",
       PrintStateMachineF=False,
       AnalyserStateClassName="analyzer_state",
       StandAloneAnalyserF=False,
       QuexEngineHeaderDefinitionFile="",
       ModeNameList=[]):
    """Contains a list of pattern-action pairs, i.e. its elements contain
       pairs of state machines and associated actions to be take,
       when a pattern matches. 

       NOTE: From this level of abstraction downwards, a pattern is 
             represented as a state machine. No longer the term pattern
             is used. The pattern to which particular states belong are
             kept track of by using an 'origin' list that contains 
             state machine ids (== pattern ids) and the original 
             state index.
             
             ** A Pattern is Identified by the State Machine ID**
       
       NOTE: It is crucial that the pattern priviledges have been entered
             into 'state_machine_id_ranking_db' in state_machine.index
             if they are to be priorized. Further, priviledged state machines
             must have been created **earlier** then lesser priviledged
             state machines.
    """
    return Generator(PatternActionPair_List, 
                     StateMachineName, AnalyserStateClassName, Language, 
                     OnFailureAction, EndOfStreamAction, ModeNameList, 
                     PrintStateMachineF, StandAloneAnalyserF).do()
    
def frame_this(Code):
    return Setup.language_db["$frame"](Code, Setup)

def init_unused_labels():
    ## print "##init,", languages.label_db_marker_get_unused_label_list()
    languages.label_db_marker_init()

def delete_unused_labels(Code):
    """Delete unused labels, so that compilers won't complain.

       This function is performance critical, so we do a high speed replacement,
       where we write into the text itself. The original label is overwritten
       with the replaced label text.
       
       The body of this function contains the 'good old' but slow method
       in case that the new method has doubts about being able to perform well.
    """
    ## print "##delete,", languages.label_db_marker_get_unused_label_list()
    LanguageDB = Setup.language_db
    label_list = languages.label_db_marker_get_unused_label_list()

    # If the fast function was successful we are done
    result = delete_unused_labels_FAST(Code, label_list)
    if result != "": return result

    replacement_list_db = {}
    for label in label_list:
        original    = LanguageDB["$label-pure"](label)
        replacement = LanguageDB["$comment"](original)
        first_letter = original[0]
        if replacement_list_db.has_key(first_letter) == False:
            replacement_list_db[first_letter] = [ [original, replacement] ]
        else:
            replacement_list_db[first_letter].append([original, replacement])

    code = Code
    for first_letter, replacement_list in replacement_list_db.items():
        code = blue_print(code, replacement_list, first_letter)

    return code
        

import array
def delete_unused_labels_FAST(Code, LabelList):
    LanguageDB = Setup.language_db

    code = array.array("c", Code)
    if code.itemsize != 1: return ""

    comment_overhead = len(LanguageDB["$comment"](""))

    for label in LabelList:
        original = LanguageDB["$label-pure"](label)
        length = len(original)
        if length < 4: return ""
        idx = Code.find(original)
        while idx != -1:
            code[idx]              = "/"
            code[idx + 1]          = "*"
            code[idx + length - 1] = "*"
            code[idx + length]     = "/"
            idx = Code.find(original, idx + length)

    return code.tostring()
        
