# PURPOSE: Providing a database for code generation in different programming languages.
#          A central object 'db' contains for each keyword, such as '$if' '$else' a correspondent
#          keyword or sequence that corresponds to it in the given language. Some code
#          elements are slighly more complicated. Therefore the db returns for some keywords
#          a function that generates the correspondent code fragment.
# 
# NOTE: The language of reference is C++. At the current state the python code generation 
#       is only suited for unit test of state transitions, no state machine code generation.
#       Basics for other languages are in place (VisualBasic, Perl, ...) but no action has been
#       taken to seriously implement them.
#
# AUTHOR: Frank-Rene Schaefer
# ABSOLUTELY NO WARRANTY
#########################################################################################################
from copy import deepcopy, copy
import quex.core_engine.generator.languages.cpp    as cpp
import quex.core_engine.generator.languages.python as python
from quex.frs_py.string_handling import blue_print

def __nice(SM_ID): 
    return repr(SM_ID).replace("L", "")
    
db = {}

__label_db = \
{
    "$terminal":              lambda TerminalIdx: "TERMINAL_%s"        % __nice(TerminalIdx),
    "$terminal-direct":       lambda TerminalIdx: "TERMINAL_%s_DIRECT" % __nice(TerminalIdx),
    "$terminal-general-bw":   lambda NoThing:     "TERMINAL_GENERAL_BACKWARD",
    "$terminal-EOF":          lambda NoThing:     "TERMINAL_END_OF_STREAM",
    "$terminal-FAILURE":      lambda NoThing:     "TERMINAL_FAILURE",
    "$entry":                 lambda StateIdx:    "STATE_%s"          % __nice(StateIdx),
    "$drop-out":              lambda StateIdx:    "STATE_%s_DROP_OUT" % __nice(StateIdx),
    "$drop-out-direct":       lambda StateIdx:    "STATE_%s_DROP_OUT_DIRECT" % __nice(StateIdx),
    "$input":                 lambda StateIdx:    "STATE_%s_INPUT"    % __nice(StateIdx),
    "$re-start":              lambda NoThing:     "__REENTRY_PREPARATION",
    "$start":                 lambda NoThing:     "__REENTRY",
}

## 
__label_printed_list_unique = {}
__label_used_list_unique    = {}

def label_db_marker_init():
    global __label_printed_list_unique
    global __label_used_list_unique

    __label_printed_list_unique.clear()
    ## __label_printed_list_unique["__TERMINAL_ROUTER"] = True
    __label_used_list_unique.clear()

def label_db_get(Type, Index, GotoTargetF=False):
    global __label_printed_list_unique
    global __label_used_list_unique
    global __label_db
    
    label = __label_db[Type](Index)

    if Type in ["$re-start", "$start"]: return label

    # Keep track of any label. Labels which are not used as goto targets
    # may be deleted later on.
    if GotoTargetF: __label_used_list_unique[label]    = True
    else:           __label_printed_list_unique[label] = True

    return label

def label_db_marker_get_unused_label_list():
    global __label_used_list_unique
    global __label_printed_list_unique
    global __label_db
    
    result = []

    # print "##0", __label_used_list_unique.keys()
    # print "##1", __label_printed_list_unique.keys()
    for label in __label_printed_list_unique:
        if label not in __label_used_list_unique:
            result.append(label)
    return result


#________________________________________________________________________________
# C++
#    
def __close_namespace(NameList):
    txt = ""
    for name in NameList:
        txt += "} /* Closing Namespace '%s' */\n" % name
    return txt

def __open_namespace(NameList):
    txt = ""
    i = -1
    for name in NameList:
        i += 1
        txt += "    " * i + "namespace %s {\n" % name
    return txt

def __string_if_true(Value, Condition):
    if Condition: return Value
    else:         return ""

db["C++"] = {
    "$language":      "C++",
    "$comment-delimiters": [["/*", "*/", ""], ["//", "\n", ""], ["\"", "\"", "\\\""]],
    "$namespace-open":     __open_namespace,
    "$namespace-close":    __close_namespace,
    "$namespace-ref":      lambda NameList:
                           reduce(lambda x, y: x + "::" + y, [""] + NameList) + "::",
    "$class-member-def":   lambda TypeStr, MaxTypeNameL, VariableName, MaxVariableL:
                           "    %s%s %s;" % (TypeStr, " " * (MaxTypeNameL - len(TypeStr)), VariableName),
    "$MODUL$":        cpp,
    "$require-terminating-zero-preparation": cpp.__require_terminating_zero_preparation,
    "$function_def":  "bool\n$$function_name$$(const int input)\n{\n", # still needed ?? fschaef 07y3m20d
    "$function_end":  "}\n",                                           # still needed ??
    "$if":            "if(",
    "$then":          ") {\n",
    "$elseif":        "} else if(",
    "$endif":         "}\n",
    "$endif-else":    "} else {\n",
    "$end-else":      "}\n",
    "$else":          "else {",                                                     
    "$and":           "&&",
    "$or":            "||",
    "$loop-start-endless":    "while( 1 + 1 == 2 ) {\n",
    "$loop-end":              "}\n",
    "$continue":              "continue;\n",
    "$break":                 "break;\n",
    "$not BLC":               "(input != QUEX_SETTING_BUFFER_LIMIT_CODE) ",
    "$EOF":                   "QUEX_NAME(Buffer_is_end_of_file)(&me->buffer)",
    "$BOF":                   "QUEX_NAME(Buffer_is_begin_of_file)(&me->buffer)",
    "$if pre-context":        lambda id: "if( pre_context_%s_fulfilled_f ) {\n" % repr(id).replace("L", ""),
    "$elseif pre-context":    lambda id: "else if( pre_context_%s_fulfilled_f ) {\n" % repr(id).replace("L", ""),
    "$if begin-of-line":      "if( me->buffer._character_before_lexeme_start == '\\n' ) {\n",
    "$elseif begin-of-line":  "else if( me->begin_of_line_f ) {\n",
    "$if <":              lambda value: "if( input < "  + value + ") {\n",
    "$if in-set":         cpp.__get_if_in_character_set,
    "$if in-interval":    cpp.__get_if_in_interval,
    "$if ==":             lambda value: "if( input == " + value + ") {\n",
    "$if !=":             lambda value: "if( input != " + value + ") {\n",
    #
    "$if >=":             lambda value: "if( input >= " + value + ") {\n",
    "$<":                 lambda left, right: left + " < " + right,
    "$==":                lambda left, right: left + " == " + right,
    "$!=":                lambda left, right: left + " != " + right,
    #
    "$comment":           lambda txt: "/* " + txt + " */",
    "$ml-comment":        lambda txt: "    /* " + txt.replace("/*", "SLASH_STAR").replace("*/", "STAR_SLASH").replace("\n", "\n     * ") + "\n     */",
    "$/*":     "//",
    "$*/":     "\n",
    "$*/\n":   "\n",    # make sure, that we do not introduce an extra '\n' in case that end of comment
    #                   # is followed directly by newline.
    "$local-variable-defs": cpp.__local_variable_definitions, 
    "$input":               "input",
    "$mark-lexeme-start":   "QUEX_NAME(Buffer_mark_lexeme_start)(&me->buffer);",
    "$input/increment":     "QUEX_NAME(Buffer_input_p_increment)(&me->buffer);",
    "$input/add":           lambda Offset:      "QUEX_NAME(Buffer_input_p_add_offset)(&me->buffer, %i);" % Offset,
    "$input/decrement":     "QUEX_NAME(Buffer_input_p_decrement)(&me->buffer);",
    "$input/get":           "input = QUEX_NAME(Buffer_input_get)(&me->buffer);",
    "$input/get-offset":    lambda Offset:      "input = QUEX_NAME(Buffer_input_get_offset)(&me->buffer, %i);" % Offset,
    "$input/tell_position": lambda PositionStr: "%s = QUEX_NAME(Buffer_tell_memory_adr)(&me->buffer);\n" % PositionStr,
    "$input/seek_position": lambda PositionStr: "QUEX_NAME(Buffer_seek_memory_adr)(&me->buffer, %s);\n" % PositionStr,
    "$return":              "return;",
    "$return_true":         "return true;",
    "$return_false":        "return false;",
    "$goto":                 lambda Type, Argument=None:  "goto %s;" % label_db_get(Type, Argument, GotoTargetF=True),
    "$goto-template":        lambda TemplateStateIdx, StateKey: 
                             "template_state_key = %i; " % StateKey + \
                             "goto %s;\n" % label_db_get("$entry", TemplateStateIdx, GotoTargetF=True),
    "$goto-template-target": lambda TemplateIdx, TargetStateIdx: 
                             "QUEX_TEMPLATE_GOTO(%i, %i);" % (TemplateIdx, TargetStateIdx),
    "$label-pure":           lambda Label:                "%s:" % Label,
    "$label-def":           lambda Type, Argument=None:  
                                "%s:\n"                             % label_db_get(Type, Argument) + \
                                __string_if_true("    ", Type == "$drop-out-direct") + \
                                "    QUEX_DEBUG_PRINT(&me->buffer, \"LABEL: %s\");\n" % label_db_get(Type, Argument),
    "$analyzer-func":        cpp.__analyzer_function,
    "$terminal-code":        cpp.__terminal_states,      
    "$compile-option":       lambda option: "#define %s\n" % option,
    "$assignment":           lambda variable, value:
                             "QUEX_DEBUG_PRINT2(&me->buffer, \"%s = %%s\", \"%s\");\n" % (variable, value) + \
                             "%s = %s;\n" % (variable, value),
    "$set-last_acceptance":  lambda value:
                             "QUEX_DEBUG_PRINT2(&me->buffer, \"ACCEPTANCE: %%s\", \"%s\");\n" % value + \
                             "QUEX_SET_last_acceptance(%s);\n" % value,
    "$goto-last_acceptance": "QUEX_GOTO_last_acceptance();\n",
    #
    "$header-definitions":   cpp.__header_definitions,
    "$frame":                cpp.__frame_of_all,
    "$goto-mode":            lambda Mode: "QUEX_NAME(enter_mode)(&self, &" + Mode + ");",
    "$gosub-mode":           lambda Mode: "QUEX_NAME(push_mode)(&self, &" + Mode + ");",
    "$goup-mode":            lambda Mode: "QUEX_NAME(pop_mode)(&self);",                  # Must be function, w/o arg
    "$code_base":               "/quex/code_base/",
    "$token-default-file":      "/token/CppDefault.qx",
    "$token_template_file":     "/token/CppTemplate.txt",
    "$analyzer_template_file":  "/analyzer/CppTemplate.txt",
    "$file_extension":          ".cpp",
    }

#________________________________________________________________________________
# C
#    
db["C"] = copy(db["C++"])
db["C"]["$token-default-file"]     = "/token/CDefault.qx"
db["C"]["$token_template_file"]    = "/token/CTemplate.txt"
db["C"]["$token_template_i_file"]  = "/token/CTemplateI.txt"
db["C"]["$analyzer_template_file"] = "/analyzer/CTemplate.txt"
db["C"]["$file_extension"]         = ".c"

#________________________________________________________________________________
# Perl
#    
db["Perl"] = copy(db["C"])
db["Perl"]["$function_def"] = "sub $$function_name$$ {\n    input = shift\n"

#________________________________________________________________________________
# Python
#    
db["Python"] = {
    "$function_def":  "def $$function_name$$(input):\n",
    "$function_end":  "\n",                                                  
    "$if":     "if ",
    "$then":   ":",
    "$if EOF": "if True:\n",
    "$not BLC": "True",
    "$if <":   lambda value: "if input < "  + value + ":\n",
    "$if in-set":       python.__get_if_in_character_set,
    "$if in-interval":  python.__get_if_in_interval,
    "$if ==":  lambda value: "if input == " + value + ":\n",
    "$if !=":  lambda value: "if input != " + value + ":\n",
    "$if >=":  lambda value: "if input >= " + value + ":\n",
    "$<":      lambda left, right: left + " < " + right,
    "$==":     lambda left, right: left + " == " + right,
    "$!=":     lambda left, right: left + " != " + right,
    "$>=":     ">=",
    "$endif":      "",                                                    
    "$else":       "else:",                                              
    "$endif-else": "else:\n",
    "$end-else":   "",
    "$and":    "and",
    "$comment": lambda txt: "# " + txt + "\n",
    "$/*":     "#",
    "$*/":     "\n",  
    "$*/\n":   "\n",    # make sure, that we do not introduce an extra '\n' in case that end of comment
    #                   # is followed directly by newline.
    "$input":         "input",
    "$input/get":     "# TODO: getting input into parser",
    "$input/increment":     "# TODO: getting input into parser",
    "$return_true":   "return True",
    "$return_false":  "return False",
    "$label-definition":  python.__label_definition,
    "$goto-terminate":    python.__goto_terminal_state, 
    "$acceptance-info-fw":   lambda x, y: "",
    "$acceptance-info-bw":   lambda x, y: "",
    "$acceptance-info-bwfc": lambda x, y: "",
    "$label":             "",   
    "$include":           lambda include_file: "#include <%s>" % include_file,
    "$debug-info-input":  "",
    "$header-definitions": "",
    "$goto-last_acceptance": "# QUEX_GOTO_last_acceptance();\n",
    "$drop-out": "# drop out\n",
    #
    "$goto":                lambda Type, Argument=None:  "return %s;" % Argument,
    "$label-def":           lambda Type, Argument=None:  
                                "#%s:\n"                                % label_db[Type](Argument) + \
                                "#    QUEX_DEBUG_LABEL_PASS(\"%s\");\n" % label_db[Type](Argument),
    "$drop-out-forward":  lambda StateIndex: 
                          "# QUEX_SET_drop_out_state_index(%i);\n" % int(StateIndex) + \
                          "# goto __FORWARD_DROP_OUT_HANDLING;\n",
    "$drop-out-backward": lambda StateIndex:              
                          "# QUEX_SET_drop_out_state_index(%i);\n" % int(StateIndex) + \
                          "# goto __BACKWARD_DROP_OUT_HANDLING;\n",
}

#________________________________________________________________________________
# Visual Basic 6
#    
db["VisualBasic6"] = {
    "$if":     "If",
    "$then":   "Then",
    "$endif":  "End If",
    "$>=":     ">=",
    "$==":     lambda left, right: left + " == " + right,
    "$!=":     lambda left, right: left + " <> " + right,
    "$input":  "input",
    "$return_true":  "$the_function = True: Exit Function",
    "$return_false": "$the_function = True: Exit Function",
    }



def replace_keywords(program_txt, LanguageDB, NoIndentF):
    """Replaces pseudo-code keywords with keywords of the given language."""

    txt = blue_print(program_txt, LanguageDB.items())

    if NoIndentF == False:
        # delete the last newline, to prevent additional indentation
        if txt[-1] == "\n": txt = txt[:-1]
        # indent by four spaces
        # (if this happens in recursively called functions nested indented blocks
        #  are correctly indented, see NumberSet::get_condition_code() for example)     
        txt = txt.replace("\n", "\n    ") + "\n"
    
    return txt          
