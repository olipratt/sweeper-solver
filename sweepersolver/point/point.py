"""
A point class with associated methods.
"""
from math import sqrt


class Point:
    """ Represents an immutable 2d point. """

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "Point(%r, %r)" % (self.x, self.y)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    @property
    def x(self):
        """ Get the x coordinated of the point. """
        return self._x

    @property
    def y(self):
        """ Get the y coordinated of the point. """
        return self._y

    def chebyshev_distance(self, other_point):
        """ 'Chessboard' distance between two points. """
        return max(abs(self.x - other_point.x), abs(self.y - other_point.y))

    def euclidean_distance(self, other_point):
        """ 'Normal' distance between two points. """
        return sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)


if __name__ == "__main__":
    import unittest

    class TestChebyshevDistance(unittest.TestCase):
        """ Test the distance calculation methods of a Point. """

        def test_zero_distance(self):
            self.assertEqual(Point(2, 1).chebyshev_distance(Point(2, 1)), 0)

        def test_one_distance(self):
            self.assertEqual(Point(2, 1).chebyshev_distance(Point(2, 2)), 1)

        def test_negative_distance(self):
            self.assertEqual(Point(2, 3).chebyshev_distance(Point(-2, -3)), 6)

    class TestEuclideanDistance(unittest.TestCase):
        """ Test the distance calculation methods of a Point. """

        def test_zero_distance(self):
            self.assertEqual(Point(2, 1).euclidean_distance(Point(2, 1)), 0)

        def test_one_distance(self):
            self.assertEqual(Point(2, 1).euclidean_distance(Point(2, 2)), 1)

        def test_negative_distance(self):
            self.assertEqual(Point(1, 1).euclidean_distance(Point(-2, -3)), 5)

    class TestEquality(unittest.TestCase):
        """ Test the equality and inequality of Points. """

        def test_same_coords(self):
            self.assertEqual(Point(2, 1), Point(2, 1))

        def test_same_instance(self):
            point = Point(2, 1)
            self.assertEqual(point, point)

        def test_x_inequality(self):
            self.assertNotEqual(Point(1, 1), Point(0, 1))

        def test_y_inequality(self):
            self.assertNotEqual(Point(1, 1), Point(1, 0))

    unittest.main()
