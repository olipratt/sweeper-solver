"""
An integer that may not be exactly known, so is represented by a set of bounds.
"""


class BoundedInt:
    # Todo: Add docstings to all properties, magic methods, etc.

    def __init__(self, init_min, init_max):
        if not isinstance(init_min, int) or not isinstance(init_max, int):
            raise TypeError("Bounds are not integers")
        if init_max < init_min:
            raise ValueError("Min bound greater than max bound")

        self._min = int(init_min)
        self._max = int(init_max)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.is_exact and self.exact == other
        elif isinstance(other, self.__class__):
            return (self.min == other.min) and (self.max == other.max)
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

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def is_exact(self):
        return self.min == self.max

    @property
    def exact(self):
        return self.min if self.is_exact else None

    def intersection(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Can only take intersection with same type")

        if (self.min > other.max) or (self.max < other.min):
            # Ranges don't overlap at all.
            return None

        # Ranges must overlap somewhat - build that overlapping range.
        new_min = max(self.min, other.min)
        new_max = min(self.max, other.max)

        return BoundedInt(new_min, new_max)


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

        def test_same_bounds_2(self):
            self.assertEqual(BoundedInt(1, 2), BoundedInt(1, 2))

        def test_same_instance_exact(self):
            bounded = BoundedInt(1, 1)
            self.assertEqual(bounded, bounded)

        def test_same_instance_range(self):
            bounded = BoundedInt(1, 2)
            self.assertEqual(bounded, bounded)

        def test_exact(self):
            self.assertEqual(BoundedInt(1, 1), 1)

    class TestInequality(unittest.TestCase):
        def test_exact(self):
            self.assertNotEqual(BoundedInt(1, 1), 2)

        def test_different_bounds(self):
            self.assertNotEqual(BoundedInt(1, 3), BoundedInt(1, 2))

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

    class TestExact(unittest.TestCase):
        def test_is_exact_when_not(self):
            self.assertFalse(BoundedInt(1, 9).is_exact)
            self.assertIsNone(BoundedInt(1, 9).exact)

        def test_is_exact_when_is(self):
            self.assertTrue(BoundedInt(5, 5).is_exact)
            self.assertEqual(BoundedInt(5, 5).exact, 5)

    class TestIntersection(unittest.TestCase):
        def setUp(self):
            self.bounded = BoundedInt(1, 9)

        def test_wrong_type(self):
            self.assertRaises(TypeError, self.bounded.intersection, 'a')

        def test_self_intersection(self):
            self.assertEqual(self.bounded.intersection(self.bounded),
                             self.bounded)

        def test_no_intersection(self):
            self.assertIsNone(self.bounded.intersection(BoundedInt(10, 11)))

        def test_boundary_intersection(self):
            self.assertEqual(self.bounded.intersection(BoundedInt(9, 11)),
                             9)
            self.assertEqual(self.bounded.intersection(BoundedInt(0, 1)),
                             1)

        def test_overlap_intersection(self):
            self.assertEqual(self.bounded.intersection(BoundedInt(5, 11)),
                             BoundedInt(5, 9))
            self.assertEqual(self.bounded.intersection(BoundedInt(-3, 2)),
                             BoundedInt(1, 2))

        def test_contained_intersection(self):
            self.assertEqual(self.bounded.intersection(BoundedInt(5, 7)),
                             BoundedInt(5, 7))
            self.assertEqual(BoundedInt(-5, 15).intersection(self.bounded),
                             self.bounded)

    unittest.main()
