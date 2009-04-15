from   quex.frs_py.file_in          import *

def parse(fh):
    # NOTE: Catching of EOF happens in caller: parse_section(...), the caller

    option_list = parse_token_type_options(fh)
    #
    dummy, i = read_until_letter(fh, ["{"], Verbose=True)

    while 1 + 1 == 2:
        if __check(fh, "{"):
            # Combined token type members (members that can occur at the same time)
            combined_member_list = []
            while 1 + 1 == 2:
                member = parse_token_type_member_definition(fh)
                if member == None: break
                combined_member_list.append(member)
            # Closing '}' has been eaten by parse_token_type_member_definition(..)
            token_type_member_list.append(combined_member_list)
        else:
            member = parse_token_type_member_definition(fh)
            if member == None: break
            token_type_member_list.append([member])
            
def parse_token_type_options(fh):
    """ <head:  std::string        name>
        <head:  std::vector<int>   number_list>
        <column:   uint32_t>
        <line:     uint32_t>
        <token_id: uint8_t>
    """
    token_id_type        = CodeFragment()
    column_counter_type  = CodeFragment()
    line_counter_type    = CodeFragment()
    header_variable_list = []

    while 1 + 1 == 2:
        identifier = read_option_start(fh)
        if identifier == None: return

        fields = read_option_value(fh).split()
        if identifier == "head":
            if len(fields) != 2:
                error_msg("token_type: Header variable specification requires\n" + \
                          "two fields, namely a variable name and a type/class.\n" + \
                          "Example: <head: std::string  name>", fh)
            type = UserCodeFragment(fields[0], fh.name, get_current_line_info_number(fh))
            name = fields[1]
            header_variable_list.append([type, name])

        elif identifier == "token_id":
            token_id_type = __extract_type_code_str(fields, "token identifier", fh)

        elif identifier == "column":
            column_counter_type = __extract_type_code_str(fields, "column counter", fh)
    
        elif identifier == "line":
            line_counter_type = __extract_type_code_str(fields, "line counter",fh)
    
def __extract_type_code_str(fields, Description, fh):
    if    len(fields) != 1 \
       or fields[0].find("string") != -1 \
       or fields[0].find("vector") != -1 \
       or fields[0].find("map")    != -1:
        error_msg("token_id: The type of the %s type must be a scalar numeric type.\n" % Description \
                  "Example: <token_id: uint16_t>", fh)

    return UserCodeFragment(fields[0], fh.name, get_current_line_info_number(fh))

def parse_token_type_member_definition(fh):
    member_name     = ""
    type_name       = ""
    array_element_n = -1

    skip_whitespace(fh)
    if __check(fh, "}"): return
    
    # -- get the name of the pattern
    skip_whitespace(fh)
    member_name = read_identifier(fh)
    if member_name == "":
        error_msg("Missing identifier for token struct/class member.", fh)

    skip_whitespace(fh)
    verify_next_word(fh, ":")
    skip_whitespace(fh)

    if __check(fh, "}"): 
        error_msg("Missing type for token struct/class member '%s'." % member_name, fh)

    type_name = read_identifier(fh)
    if type_name == "":
        error_msg("Missing type name for token struct/class member.", fh)

    skip_whitespace(fh)
    if __check(fh, "[") == false:
        skip_whitespace(fh)
        if __check(fh, ";"): 
            error_msg("Missing ';' after token struct/class member '%s' definition." % \
                      member_name, fh)
    else:
        skip_whitespace(fh)
        number_str = read_integer(fh)
        if number_str == "":
            error_msg("Missing integer after '[' in '%s' definition." % member_name, fh)
        array_element_n = int(number_str)

        skip_whitespace(fh)

        if __check(fh, "]") == false:
            error_msg("Missing closing ']' in '%s' array definition." % member_name, fh)
        skip_whitespace(fh)

        if __check(fh, ";"): 
            error_msg("Missing ';' after token struct/class member '%s' definition." % \
                      member_name, fh)

    return TokenTypeMember(member_name, type_name, array_element_n)


