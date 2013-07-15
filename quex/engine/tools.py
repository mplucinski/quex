from   itertools       import izip, islice
import sys
import os

def r_enumerate(x):
    """Reverse enumeration."""
    return izip(reversed(xrange(len(x))), reversed(x))

def print_callstack(BaseNameF=False):
    try:
        i = 2
        name_list = []
        while 1 + 1 == 2:
            x = sys._getframe(i).f_code
            name_list.append([x.co_filename, x.co_firstlineno, x.co_name])
            i += 1
    except:
        pass

    L = len(name_list)
    for i, x in r_enumerate(name_list):
        if BaseNameF: name = os.path.basename(x[0])
        else:         name = x[0]
        print "%s%s:%s:%s(...)" % (" " * ((L-i)*4), name, x[1], x[2]) 

def pair_combinations(iterable):
    other = tuple(iterable)
    for i, x in enumerate(other):
        for y in islice(other, i+1, None):
            yield x, y

def uniformity_check_and_set(X, NewX):
    if X == -1:      # Not yet set.
        return NewX  # => Set first time.
    elif X is None:  # Know to be not uniform.
        return X     # => No change.
    elif X != NewX:  # Uniform until now, but not with 'NewX'.
        return None  # => Not uniform.
    else:            # Uniform with 'NewX'.
        return X     # => Nothing to be done.

class TypedSet(set):
    def __init__(self, Cls):
        self.__element_class = Cls

    def add(self, X):
        assert isinstance(X, self.__element_class)
        set.add(self, X)

    def update(self, Iterable):
        for x in Iterable:
            assert isinstance(x, self.__element_class)
        set.update(self, Iterable)

