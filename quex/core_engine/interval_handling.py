#! /usr/bin/env python
# PURPOSE: Provides classes for handling of sets of numbers:
#
#     Interval: A continous set of numbers in a range from a
#              minimum to a maximum border.
# 
#     NumberSet: A non-continous set of numbers consisting of
#                described as a set of intervals.
#
# DATE: May 26, 2006
#
# (C) 2006 Frank-Rene Schaefer
#
# ABSOLUTELY NO WARRANTY
################################################################################

from copy import copy, deepcopy
from quex.frs_py.string_handling import blue_print

import quex.core_engine.generator.languages.core as languages
import quex.core_engine.utf8                     as utf8
import sys

class Interval:
    """Representing an interval with a minimum and a maximum border. Implements
    basic operations on intervals: union, intersection, and difference.
    """
    def __init__(self, Begin=None, End=None):
        """NOTE: Begin = End signifies **empty** interval.

        Begin == None and End == None   => Empty Interval

        Begin == int and End == None    => Interval of size '1' (one number = Begin)
        
        Begin and End != None           => Interval starting from 'Begin' and the last
                                           element is 'End-1'

        """

        # .begin = smallest integer that belogns to interval.
        # .end   = first integer > 'Begin' that does **not belong** to interval
        if Begin == None and End == None:
            # empty interval
            self.begin = 0
            self.end   = 0
        else:
            if Begin == None:
                raise "Begin can only be 'None', if End is also 'None'!"
            self.begin = Begin            
            if End == None:  
                if self.begin != sys.maxint: self.end = self.begin + 1
                else:                        self.end = self.begin
            else:    
                self.end = End
            
    def is_empty(self):
        return self.begin == self.end

    def is_all(self):
        return self.begin == -sys.maxint and self.end == sys.maxint   
        print "##res:", result
 
    def contains(self, Number):
        """True  => if Number in NumberSet
           False => else
        """
        if Number >= self.begin and Number < self.end: return True
        else:                                          return False
        
    def check_overlap(self, Other):
        """Does interval overlap the Other?"""
        if self.begin  < Other.end and self.end > Other.begin: return True
        if Other.begin < self.end  and Other.end > self.begin: return True
        else:                                                  return False

    def check_touch(self, Other):
        """Does interval touch the Other?"""
        if self.begin  < Other.end and self.end > Other.begin:   return True
        if Other.begin < self.end  and Other.end > self.begin:   return True
        if self.begin == Other.begin or self.end == Other.begin: return True
        else:                                                    return False
    
    def union(self, Other):
        if self.check_overlap(Other):
            # overlap: return one single interval
            #          (the one that encloses both intervals)
            return [ Interval(min(self.begin, Other.begin),
                              max(self.end, Other.end)) ]
        else:
            # no overlap: two disjunct intervals
            result = []
            if not self.is_empty(): result.append(copy(self))
            if not Other.is_empty(): result.append(copy(Other))
            return result

    def intersection(self, Other):
        if self.check_overlap(Other):
            # overlap: return one single interval
            #          (the one that both have in common)
            return Interval(max(self.begin, Other.begin),
                            min(self.end, Other.end)) 
        else:
            # no overlap: empty interval (begin=end)
            return Interval()  # empty interval

    def difference(self, Other):
        """Difference self - Other."""
        if self.begin >= Other.begin:
            if self.end <= Other.end:
                # overlap: Other covers self
                # --------------[xxxxxxxxxxxxx]-------------------
                # ---------[yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy]-----
                #
                #          nothing remains - empty interval
                return []
            else:
                if self.begin >= Other.end:
                    # no intersection
                    return [ copy(self) ]
                else:
                    # overlap: Other covers lower part
                    # --------------[xxxxxxxxxxxxxxxxxxxx]------------
                    # ---------[yyyyyyyyyyyyyyyyyyyy]-----------------
                    return [ Interval(Other.end, self.end) ]
        else:            
            if self.end >= Other.end:
                # overlap: self covers Other
                # ---------[xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx]-----
                # --------------[yyyyyyyyyyyyy]-------------------
                #
                # result = two disjunct intervals
                result = []
                lower_part = Interval(self.begin, Other.begin)
                if not lower_part.is_empty(): result.append(lower_part)
                upper_part = Interval(Other.end, self.end)
                if not upper_part.is_empty(): result.append(upper_part)
                return result
            else:
                if self.end <= Other.begin:
                    # no intersection
                    return [ copy(self) ]
                else:
                    # overlap: Other upper part
                    # ---------[xxxxxxxxxxxxx]------------------------
                    # --------------[yyyyyyyyyyyyy]-------------------
                    #                
                    return [ Interval(self.begin, Other.begin) ]

    def inverse(self):
        if self.begin == self.end:
            # empty interval => whole range
            return [ Interval(-sys.maxint, sys.maxint) ]
        else:
            result = []
            if self.begin != -sys.maxint: result.append(Interval(-sys.maxint,self.begin))
            if self.end   != sys.maxint:  result.append(Interval(self.end, sys.maxint))
            return result

    def size(self):
        return self.end - self.begin

    def __repr__(self):
        return self.get_string(Option="")

    def __utf8_char(self, Code):
        if   Code == - sys.maxint:   return "-oo"
        elif Code == sys.maxint:     return "oo"            
        elif Code == ord(' '):       return "' '"
        elif Code == ord('\n'):      return "'\\n'"
        elif Code == ord('\t'):      return "'\\t'"
        elif Code == ord('\r'):      return "'\\r'"
        elif Code < ord('0'):        return "\\" + repr(Code) 
        else:
            char_str = utf8.map_unicode_to_utf8(Code)
            return "'" + char_str + "'"
        # elif Code < ord('0') or Code > ord('z'): return "\\" + repr(Code)
        # else:                                    return "'" + chr(Code) + "'"

    def get_string(self, Option="", Delimiter=", "):
        if Option == "hex":    __repr = lambda x: "%05X" % x
        elif Option == "utf8": __repr = lambda x: self.__utf8_char(x)
        else:                  __repr = repr
        
        if self.begin == self.end:       return "[]"
        elif self.end - self.begin == 1: return "[" + __repr(self.begin) + "]" 
        else:                            return "[" + __repr(self.begin) + Delimiter + __repr(self.end-1) + "]"

    def get_utf8_string(self):
        #_____________________________________________________________________________
        assert self.begin <= self.end
        
        if self.begin == self.end: 
            return "''"
        elif self.end - self.begin == 1: 
            return self.__utf8_char(self.begin) 
        else:                          
            if   self.end == -sys.maxint: end_char = "-oo"
            elif self.end == sys.maxint:  end_char = "oo"
            else:                         end_char = self.__utf8_char(self.end-1)
            return "[" + self.__utf8_char(self.begin) + ", " + end_char + "]"

    def gnuplot_string(self, y_coordinate):
        if self.begin == self.end: return ""
        txt = ""
        txt += "%i %f\n" % (self.begin, y_coordinate)
        txt += "%i %f\n" % (self.end-1, y_coordinate)
        txt += "%i %f\n" % (self.end-1, float(y_coordinate) + 0.8)
        txt += "%i %f\n" % (self.begin, float(y_coordinate) + 0.8)
        txt += "%i %f\n" % (self.begin, y_coordinate)
        return txt

            
class NumberSet:
    """Represents an arbitrary set of numbers. The set is described
       in terms of intervals, i.e. objects of class 'Interval'. This
       class also provides basic operations such as union, intersection,
       and difference.
    """
    
    def __init__(self, Arg = None):
        """Arg = list     ==> list of initial intervals
           Arg = Interval ==> initial interval
           Arg = integer  ==> interval consisting of one number
           """
        arg_type = Arg.__class__.__name__
        assert arg_type in  ["Interval", "NumberSet", "int", "list"] or Arg == None

        self.__intervals = []
        
        if  arg_type == "list":
            # use 'add_interval' to ensure consistency
            for interval in Arg:
                assert interval.__class__.__name__ == "Interval"
                self.add_interval(deepcopy(interval))

        elif arg_type == "Interval":
            self.add_interval(deepcopy(Arg))

        elif arg_type == "NumberSet":
            self.__intervals = deepcopy(Arg.__intervals)

        elif arg_type == "int":
            self.add_interval(Interval(Arg))

    def quick_append_interval(self, Other, SortF=True):
        """This function assumes that there are no intersections with other intervals.
           Use this function with caution. It is much faster than the 'union' function
           or the function 'add_interval'.
        """
        assert Other.__class__.__name__ == "Interval"

        self.__intervals.append(Other)

    def add_interval(self, NewInterval):
        """Adds an interval and ensures that no overlap with existing
        intervals occurs. Note: the 'touch' test is faster here, because
        only one interval is checked against. Do not use __touchers()!"""
        if NewInterval.is_empty(): return
        
        # (1) determine if begin overlaps with the new interval
        if self.__intervals == [] or NewInterval.begin > self.__intervals[-1].end:
            self.__intervals.append(NewInterval)
            return

        X = NewInterval
        i = -1
        for y in self.__intervals:
            i += 1
            # possible cases:
            #  (1) [=== X ===]         [=== y ===]             
            #  
            #  (2) [=== X ============][=== y ===]
            #  
            #  (3) [=== X ==================]
            #                          [=== y ===]
            #  
            #  (4) [=== X =======================]
            #                          [=== y ===]
            #  
            #  (5) [=== X =============================================]
            #                          [=== y ===]
            #  
            #  (6)                     [=== X =========================]
            #                          [=== y ===]
            #  
            #  (7)                     [=== y ===][=== X ==============]
            #  
            #  (8)                     [=== y ===]           [=== X ===]
            #  
            if X.begin > y.end: 
                continue                              # filter (8)
            elif X.end < y.begin: 
                self.__intervals.insert(i, X) 
                return                                # filter (1)
            else:
                touch_begin = min(X.begin, y.begin) 
                break

        toucher_list    = [ ]
        insertion_index = i
        for y in self.__intervals[i:]:
            if X.end < y.begin: touch_end = X.end; break
            toucher_list.append(i)
            if X.end <= y.end: touch_end = y.end; break
            i += 1
        else:
            touch_end = X.end

        # (2) combine all intervals that intersect with the new one
        combination = Interval(touch_begin, touch_end)

        # (3) build new list of intervals
        #     (all overlaps are deleted, i.e. not added because they are
        #      replaced by the union with the NewInterval)
        # NOTE: The indices need to be adapted, since if for example
        #       interval '3' was an overlapper, and so '5' then if
        #       '3' is deleted, '5' comes at position '5'.
        offset = -1
        for i in toucher_list:
            offset += 1
            del self.__intervals[i - offset]

        self.__intervals.insert(insertion_index, combination)


    def cut_interval(self, CutInterval):
        """Cuts an interval from the intervals of the set.
        Note: the 'overlap' test is faster here, because
        only one interval is checked against. Do not use __overlapers()!"""
        
        # (1) deterbegine overlaps with the cutting interval
        overlapper_list = [] 
        for interval in self.__intervals:
            if interval.check_overlap(CutInterval):
                overlapper_list.append(interval)

        # (2) substract NewInterval from all intervals that overlap
        combination = CutInterval
        for overlapper in overlapper_list:
            difference_interval = overlapper.substract(CutInterval)
            combination.append(difference_interval)

        # (3) build new list of intervals
        #     (all overlaps are deleted, i.e. not added because they are
        #      replaced by the union with the CutInterval)
        new_interval_list = combination
        for interval in self.__intervals:
            if interval not in overlapper_list:
                new_interval_list.append(interval)

        self.__intervals = new_interval_list

    def contains(self, Number):
        """True  => if Number in NumberSet
           False => else
        """
        for interval in self.__intervals:
            if interval.contains(Number): return True
        return False

    def is_empty(self):
        if self.__intervals == []: return True
        for interval in self.__intervals:
            if interval.is_empty() == False: return False
        return True
        
    def is_all(self):
        """Returns True if this NumberSet covers all numbers, False if not.
           
           Note: All intervals should have been added using the function 'add_interval'
                 Thus no overlapping intervals shall exists. If the set covers all numbers,
                 then there can only be one interval that 'is_all()'
        """
        if len(self.__intervals) != 1: return False
        return self.__intervals[0].is_all()
            
    def interval_number(self):
        """This value gives some information about the 'complexity' of the number set."""
        return len(self.__intervals)

    def get_intervals(self):
        return deepcopy(self.__intervals)

    def unite_with(self, Other):
        Other_type = Other.__class__
        assert Other_type == Interval or Other_type == NumberSet, \
               "Error, argument of type %s" % Other.__class__.__name__

        if Other_type == Interval: Other = NumberSet(Other)

        # simply add all intervals to one single set
        for interval in Other.__intervals:
            self.add_interval(interval)

    def union(self, Other):
        Other_type = Other.__class__
        assert Other_type == Interval or Other_type == NumberSet, \
               "Error, argument of type %s" % Other.__class__.__name__

        shadow_of_self = deepcopy(self)

        if Other_type == Interval: Other = NumberSet(Other)

        # simply add all intervals to one single set
        for interval in Other.__intervals + shadow_of_self.__intervals:
            shadow_of_self.add_interval(interval)

        return shadow_of_self            

    def intersection(self, Other):
        assert Other.__class__.__name__ == "Interval" or Other.__class__.__name__ == "NumberSet"

        if Other.__class__.__name__ == "Interval": Other = NumberSet(Other)

        # intersect with each interval
        result = NumberSet()

        # TODO: Intervals are always sorted, thus intervals that are not to be 
        #       considered can be identified quickly. The fact that they are 
        #       sorted, though, needs to be verified! Only then touch this issue.
        for x in Other.__intervals:
            for y in self.__intervals:
                # PASTE: Interval::intersection() for performance reasons.
                if x.check_overlap(y):
                    result.add_interval(Interval(max(x.begin, y.begin),
                                                 min(x.end,   y.end)))

        return result

    def difference(self, Other):
        assert Other.__class__.__name__ == "Interval" or Other.__class__.__name__ == "NumberSet"

        if Other.__class__.__name__ == "Interval": Other = NumberSet(Other)

        assert self.__overlappers() == []
        
        # note: there should be no overlaps according to 'add_interval'
        remainder = deepcopy(self)
        for interval in Other.__intervals:
            new_remainder = NumberSet()
            for my_interval in remainder.__intervals:
                subtraction = my_interval.difference(interval)
                for sub_interval in subtraction:
                    new_remainder.add_interval(sub_interval)
            remainder = new_remainder
        return remainder

    def inverse(self):
        """Intersection of inverses of all intervals."""
        inverse_intervals = []

        result = NumberSet(Interval(-sys.maxint, sys.maxint))
        i = -1        
        for interval in self.__intervals:
            inv_interval = interval.inverse()
            result = result.intersection(NumberSet(inv_interval))

        return result
        
    def clean(self, SortF=True):
        """Sorts all intervals, so according to their begin. Lowest comes first.
           Combines adjacent and intersecting intervals to one.
        """

        # (1) Sort intervals
        if SortF:
            self.__intervals.sort(lambda a, b: -cmp(b.begin, a.begin))        

        # (2) Combine adjacent intervals
        L = len(self.__intervals)
        if L < 2: return

        new_intervals = []
        i = 0 
        current = self.__intervals[0]
        while i < L - 1:
            i += 1
            next = self.__intervals[i]

            if current.end < next.begin: 
                # (1) no intersection?
                new_intervals.append(current)
                current = next
            else:
                # (2) intersection:  [xxxxxxxxxxxxxxx]
                #                              [yyyyyyyyyyyyyyyyy]
                #          becomes   [xxxxxxxxxxxxxxxxxxxxxxxxxxx]
                #
                # => do not append interval i + 1, do not consider i + 1
                if current.end > next.end:
                    # no adaptions necessary, simply ignore next interval
                    pass
                else:
                    # adapt upper border of current interval to the end of the next
                    current.end = next.end

        new_intervals.append(current)


        self.__intervals = new_intervals

    def __overlappers(self):
        tmp = {} # use this to get unique values of indices
        #        # tmp.values() == indices of intervals that overlap
        for i in range(len(self.__intervals)):
            for k in range(i):
                if self.__intervals[i].check_overlap(self.__intervals[k]):
                    tmp[i] = 1
                    tmp[k] = 1
        return map(lambda idx: self.__intervals[idx], tmp.values())

    def __touchers(self):
        tmp = {} # use this to get unique values of indices
        #        # tmp.values() == indices of intervals that touch
        for i in range(len(self.__intervals)):
            for k in range(i):
                if self.__intervals[i].check_touch(self.__intervals[k]):
                    tmp[i] = 1
                    tmp[k] = 1
        return map(lambda idx: self.__intervals[idx], tmp.values())

    def __repr__(self):
        return repr(self.__intervals)

    def get_utf8_string(self):
        msg = ""
        for interval in self.__intervals:
            msg += interval.get_utf8_string() + ", "
        if msg != "": msg = msg[:-2]
        return msg

    def gnuplot_string(self, y_coordinate):
        txt = ""
        for interval in self.__intervals:
            txt += interval.gnuplot_string(y_coordinate)
            txt += "\n"
        return txt

    def condition_code(self,
                       Language     = "C",
                       FunctionName = "example"):

        LanguageDB = languages.db[Language]
        txt  = LanguageDB["$function_def"].replace("$$function_name$$", FunctionName)
        txt += self.__condition_code(LanguageDB)
        txt += LanguageDB["$function_end"]

        return txt

    def __condition_code(self, LanguageDB,
                         LowestInterval_Idx = -1, UppestInterval_Idx = -1, 
                         NoIndentF = False):
        
        """Writes code that does a mapping according to 'binary search' by
        means of if-else-blocks.
        """
        if LowestInterval_Idx == -1 and UppestInterval_Idx == -1:
            LowestInterval_Idx = 0
            UppestInterval_Idx = len(self.__intervals) - 1
            
        if NoIndentF:
            txt = ""
        else:
            txt = "    "

        MiddleInterval_Idx = (UppestInterval_Idx + LowestInterval_Idx) / 2
        
        # quick check:
        assert UppestInterval_Idx >= LowestInterval_Idx, \
               "NumberSet::conditions_code(): strange interval indices:" + \
               "lowest interval index = " + repr(LowestInterval_Idx) + \
               "uppest interval index = " + repr(UppestInterval_Idx)
        
        middle = self.__intervals[MiddleInterval_Idx]
        
        if LowestInterval_Idx == UppestInterval_Idx \
           and middle.begin == middle.end - 1:
            # middle == one element
            txt += "$if input $== %s $then\n" % repr(middle.begin)
            txt += "    $return_true\n"
            txt += "$end\n"
            txt += "$return_false\n"
            
        else:
            # middle interval > one element
            txt += "$if input $>= %s $then\n" % repr(middle.end)

            if MiddleInterval_Idx == UppestInterval_Idx:
                # upper interval = none
                txt += "    $return_false\n"
                txt += "$end\n"
            else:
                # upper intervals = some
                txt += self.__condition_code(LanguageDB,
                                             MiddleInterval_Idx + 1, UppestInterval_Idx)
                txt += "$end\n"

            txt += "$if input $>= %s $then\n" % repr(middle.begin)
            txt += "    $return_true\n"
            txt += "$end\n" 

            if MiddleInterval_Idx == LowestInterval_Idx:
                # lower intervals = none
                txt += "$return_false\n"
            else:
                # lower intervals = some
                txt += self.__condition_code(LanguageDB,
                                             LowestInterval_Idx, MiddleInterval_Idx - 1,
                                             NoIndentF = True)
            
        # return program text for given language
        return languages.replace_keywords(txt, LanguageDB, NoIndentF)

