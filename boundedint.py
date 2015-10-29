"""
An integer that may not be exactly known, so is represented by a set of bounds.
"""


class BoundedInt:

    def __init__(self, init_min, init_max):
        self._validate_initial_bounds(init_min, init_max)
        self._min = int(init_min)
        self._max = int(init_max)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.is_exact and self.exact == other
        elif isinstance(other, self.__class__):
            return (self.is_exact and
                    other.is_exact and
                    (self.exact == other.exact))
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, int):
            return self.max < other
        elif isinstance(other, self.__class__):
            return self.max < other.min
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, int):
            return self.max <= other
        elif isinstance(other, self.__class__):
            return self.max <= other.min
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, int):
            return self.min > other
        elif isinstance(other, self.__class__):
            return self.min > other.max
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, int):
            return self.min >= other
        elif isinstance(other, self.__class__):
            return self.min >= other.max
        else:
            return NotImplemented

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.min, self.max)

    def __str__(self):
        return "[%d-%d]" % (self.min, self.max)

    def _validate_initial_bounds(self, min_bound, max_bound):
        if not isinstance(min_bound, int) or not isinstance(max_bound, int):
            raise TypeError("Bounds are not integers")
        if max_bound < min_bound:
            raise ValueError("Min bound greater than max bound")

    def _validate_new_lower_bound(self, new_min):
        if not isinstance(new_min, int):
            raise TypeError("Bounds must be integers")
        if self.min > new_min:
            raise ValueError("Can't decrease lower bound")
        if new_min > self.max:
            raise ValueError("Can't increase lower bound above upper")

    def _validate_new_upper_bound(self, new_max):
        if not isinstance(new_max, int):
            raise TypeError("Bounds must be integers")
        if self.max < new_max:
            raise ValueError("Can't increase upper bound")
        if new_max < self.min:
            raise ValueError("Can't decrease upper bound below lower")

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, new_min):
        self._validate_new_lower_bound(new_min)
        self._min = new_min

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, new_max):
        self._validate_new_upper_bound(new_max)
        self._max = new_max

    @property
    def is_exact(self):
        return self.min == self.max

    @property
    def exact(self):
        return self.min if self.is_exact else None

    @exact.setter
    def exact(self, new_exact):
        self._validate_new_lower_bound(new_exact)
        self._validate_new_upper_bound(new_exact)
        self.min = new_exact
        self.max = new_exact


if __name__ == "__main__":
    import unittest

    class TestCreationErrors(unittest.TestCase):
        def test_wrong_type(self):
            self.assertRaises(TypeError, BoundedInt, 'a', 1)
            self.assertRaises(TypeError, BoundedInt, 0, 2.3)

        def test_min_above_max_bound(self):
            self.assertRaises(ValueError, BoundedInt, 2, 1)

    class TestEquality(unittest.TestCase):
        def test_same_bounds(self):
            self.assertEqual(BoundedInt(1, 1), BoundedInt(1, 1))

        def test_same_instance(self):
            bounded = BoundedInt(1, 1)
            self.assertEqual(bounded, bounded)

        def test_exact(self):
            self.assertEqual(BoundedInt(1, 1), 1)

    class TestInequality(unittest.TestCase):
        def test_same_bounds(self):
            self.assertNotEqual(BoundedInt(1, 2), BoundedInt(1, 2))

        def test_same_instance(self):
            bounded = BoundedInt(1, 2)
            self.assertNotEqual(bounded, bounded)

        def test_exact(self):
            self.assertNotEqual(BoundedInt(1, 1), 2)

    class TestSameTypeComparisons(unittest.TestCase):
        def test_lt(self):
            self.assertFalse(BoundedInt(1, 3) < BoundedInt(2, 4))
            self.assertFalse(BoundedInt(1, 3) < BoundedInt(3, 5))
            self.assertTrue(BoundedInt(1, 3) < BoundedInt(4, 6))

        def test_le(self):
            self.assertFalse(BoundedInt(1, 3) <= BoundedInt(2, 4))
            self.assertTrue(BoundedInt(1, 3) <= BoundedInt(3, 5))
            self.assertTrue(BoundedInt(1, 3) <= BoundedInt(4, 6))

        def test_gt(self):
            self.assertTrue(BoundedInt(1, 3) > BoundedInt(-2, 0))
            self.assertFalse(BoundedInt(1, 3) > BoundedInt(-1, 1))
            self.assertFalse(BoundedInt(1, 3) > BoundedInt(0, 2))

        def test_ge(self):
            self.assertTrue(BoundedInt(1, 3) >= BoundedInt(-2, 0))
            self.assertTrue(BoundedInt(1, 3) >= BoundedInt(-1, 1))
            self.assertFalse(BoundedInt(1, 3) >= BoundedInt(0, 2))

    class TestIntComparisons(unittest.TestCase):
        def test_lt(self):
            self.assertFalse(BoundedInt(1, 3) < 2)
            self.assertFalse(BoundedInt(1, 3) < 3)
            self.assertTrue(BoundedInt(1, 3) < 4)

        def test_le(self):
            self.assertFalse(BoundedInt(1, 3) <= 2)
            self.assertTrue(BoundedInt(1, 3) <= 3)
            self.assertTrue(BoundedInt(1, 3) <= 4)

        def test_gt(self):
            self.assertTrue(BoundedInt(1, 3) > 0)
            self.assertFalse(BoundedInt(1, 3) > 1)
            self.assertFalse(BoundedInt(1, 3) > 2)

        def test_ge(self):
            self.assertTrue(BoundedInt(1, 3) >= 0)
            self.assertTrue(BoundedInt(1, 3) >= 1)
            self.assertFalse(BoundedInt(1, 3) >= 2)

    class TestSetterErrors(unittest.TestCase):
        def setUp(self):
            self.boundedint = BoundedInt(1, 9)

        def test_wrong_type(self):
            self.assertRaises(TypeError, setattr, self.boundedint, "min", 'a')
            self.assertRaises(TypeError, setattr, self.boundedint, "max", 2.3)

        def test_changing_bounds_wrong_way(self):
            self.assertRaises(ValueError, setattr, self.boundedint, "min", 0)
            self.assertRaises(ValueError, setattr, self.boundedint, "max", 10)

        def test_min_above_max_bound(self):
            self.assertRaises(ValueError, setattr, self.boundedint, "min", 10)
            self.assertRaises(ValueError, setattr, self.boundedint, "max", 0)

    class TestExact(unittest.TestCase):
        def setUp(self):
            self.bounded = BoundedInt(1, 9)

        def test_wrong_type(self):
            self.assertRaises(TypeError, setattr, self.bounded, "exact", 'a')

        def test_setting_outside_bounds(self):
            self.assertRaises(ValueError, setattr, self.bounded, "exact", 0)
            self.assertRaises(ValueError, setattr, self.bounded, "exact", 10)

        def test_is_exact(self):
            self.assertFalse(self.bounded.is_exact)
            self.assertIsNone(self.bounded.exact)
            self.bounded.exact = 5
            self.assertTrue(self.bounded.is_exact)
            self.assertEqual(self.bounded.exact, 5)

    unittest.main()
