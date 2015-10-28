"""
An integer that may not be exactly known, so is represented by a set of bounds.
"""
import functools


@functools.total_ordering
class BoundedInt:

    def __init__(self, init_min, init_max):
        self._min = int(init_min)
        self._max = int(init_max)

    def __eq__(self, other):
        if isinstance(other, int):
            return (self.exact is not None) and self.exact == other
        elif isinstance(other, self.__class__):
            return ((self.exact is not None) and
                    (other.exact is not None) and
                    (self.exact == other.exact))
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, int):
            return (self.exact is not None) and self.exact < other
        elif isinstance(other, self.__class__):
            return ((self.exact is not None) and
                    (other.exact is not None) and
                    (self.exact < other.exact))
        else:
            return NotImplemented

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.min, self.max)

    def __str__(self):
        return "[%d-%d]" % (self.min, self.max)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, new_min):
        new_min = int(new_min)
        assert self._min < new_min, "Can't decrease lower bound"
        self._min = int(new_min)

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, new_max):
        new_max = int(new_max)
        assert self._max < new_max, "Can't increase upper bound"
        self._max = new_max

    @property
    def exact(self):
        return self.min if self.min == self.max else None
