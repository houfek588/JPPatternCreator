import math
from typing import Optional, Tuple, List
import matplotlib.pyplot as plt
# def substract_tuples(tuple1: tuple = (float, float), tuple2: tuple = (float, float)):
#     return (tuple1[0] - tuple2[0], tuple1[1] - tuple2[1])

class Line:
    def __init__(self, point1: Tuple[float, float], point2: Optional[Tuple[float, float]] = None,
                 vector: Optional[Tuple[float, float]] = None):
        """
        Initialize a line using two points or a point and a direction vector.
        The internal representation is in the general form: ax + by + c = 0.
        """
        self.point1 = point1
        self.point2 = point2
        self.vector = vector if vector else self._compute_vector(point1, point2)

        if self.vector is None:
            raise ValueError("Either a second point or a direction vector must be provided.")

        # Compute general form coefficients: ax + by + c = 0
        self.a = self.vector[1]
        self.b = -self.vector[0]
        self.c = point1[1] * self.vector[0] - point1[0] * self.vector[1]

    def __str__(self) -> str:
        return f"Equation of line: {self.a}*x + {self.b}*y + {self.c} = 0"

    def is_vertical(self) -> bool:
        return self.b == 0

    def is_horizontal(self) -> bool:
        return self.a == 0

    def get_vector(self) -> Tuple[float, float]:
        return self.vector

    def get_start_point(self) -> Tuple[float, float]:
        return self.point1

    def get_end_point(self, x: Optional[float] = None) -> Tuple[float, float]:
        if self.point2:
            return self.point2
        if x is None:
            raise ValueError("End point is not defined. Provide x value to compute it.")
        y = self.get_y_point(x)
        self.point2 = (x, y)
        return self.point2

    def get_edge_points(self):
        return (self.get_start_point(), self.get_end_point())

    def get_y_point(self, x: float) -> float:
        """
        Evaluate y for a given x using the line equation.
        Returns None if the line is vertical.
        """
        if self.is_vertical():
            raise ValueError("Cannot compute y for vertical line.")
        return (-self.a * x - self.c) / self.b

    def get_x_point(self, y: float) -> float:
        """
        Evaluate x for a given y using the line equation.
        Returns None if the line is horizontal.
        """
        if self.is_horizontal():
            raise ValueError("Cannot compute x for horizontal line.")
        return (-self.b * y - self.c) / self.a

    def get_point_distance(self, d: float) -> Tuple[float, float]:
        """
        Returns a point at distance `d` along the line direction, starting from point1.
        """
        if self.is_vertical():
            return (self.point1[0], self.point1[1] + d)

        slope = -self.a / self.b
        dx = d / math.sqrt(1 + slope ** 2)
        x_new = self.point1[0] + dx
        return (x_new, self.get_y_point(x_new))

    def line_length(self, x: Optional[float] = None) -> float:
        if self.point2:
            length = math.sqrt((self.point2[0] - self.point1[0]) ** 2 + (self.point2[1] - self.point1[1]) ** 2)
            return length
        if x is None:
            raise ValueError("End point is not defined. Provide x value to compute it.")

        y = self.get_y_point(x)
        self.point2 = (x, y)
        length = math.sqrt((self.point2[0] - self.point1[0]) ** 2 + (self.point2[1] - self.point1[1]) ** 2)
        return length

    def intersection(self, other: 'Line') -> Tuple[float, float]:
        """
        Computes the intersection point with another line.
        Raises error if lines are parallel or colinear.
        """
        if not isinstance(other, Line):
            raise TypeError("Argument must be of type Line.")

        denominator = self.a * other.b - other.a * self.b
        if abs(denominator) < 1e-9:
            raise ValueError("Lines are parallel or colinear; no unique intersection.")

        y = (other.a * self.c - self.a * other.c) / denominator
        x = self.get_x_point(y)
        return (x, y)

    def normal_line(self, x: Optional[float] = None) -> 'Line':
        """
        Returns the normal line (perpendicular) to this one,
        passing through the point at x on the current line (or point1 if x is None).
        """
        normal_vector = (-self.vector[1], self.vector[0])  # Rotate vector 90 degrees
        if x is not None:
            y = self.get_y_point(x)
            return Line((x, y), vector=normal_vector)
        return Line(self.point1, vector=normal_vector)

    def parallel_line(self, d: float) -> 'Line':
        """
        Returns a line parallel to the current line and offset by distance `d`.
        The offset is done perpendicular to the line direction.
        """
        normal = self.normal_line()
        new_point = normal.get_point_distance(d)
        return Line(new_point, vector=self.vector)

    def parallel_line_point(self, p: Tuple[float, float]) -> 'Line':
        return Line(p, vector=self.vector)

    @staticmethod
    def _compute_vector(p1: Tuple[float, float], p2: Optional[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """
        Compute direction vector from two points.
        """
        if p1 is None or p2 is None:
            return None
        return (p2[0] - p1[0], p2[1] - p1[1])


class Bezier:
    def __init__(self, control_points: List[Tuple[float, float]]):
        """
        Initialize a Bezier curve from a list of control points.

        Supports arbitrary degree, though quadratic (3 points) and cubic (4 points) are most common.
        """
        if len(control_points) < 2:
            raise ValueError("At least two control points are required.")
        self.control_points = control_points
        self.degree = len(control_points) - 1

    def __str__(self) -> str:
        return f"BezierCurve (degree {self.degree}) with control points: {self.control_points}"

    def get_point(self, t: float) -> Tuple[float, float]:
        """
        Evaluate the Bezier curve at a parameter t in [0, 1].
        Uses De Casteljau's algorithm.
        """
        if not 0 <= t <= 1:
            raise ValueError("Parameter t must be in [0, 1].")

        points = self.control_points.copy()
        while len(points) > 1:
            points = [
                (
                    (1 - t) * p0[0] + t * p1[0],
                    (1 - t) * p0[1] + t * p1[1]
                )
                for p0, p1 in zip(points[:-1], points[1:])
            ]
        return points[0]

    def get_derivative(self) -> 'BezierCurve':
        """
        Returns the derivative of the Bezier curve as another Bezier curve.
        Useful for getting tangent vectors.
        """
        n = self.degree
        derivative_points = [
            (
                n * (p1[0] - p0[0]),
                n * (p1[1] - p0[1])
            )
            for p0, p1 in zip(self.control_points[:-1], self.control_points[1:])
        ]
        return Bezier(derivative_points)

    def get_tangent(self, t: float) -> Tuple[float, float]:
        """
        Computes the tangent vector at a parameter t in [0, 1].
        """
        deriv_curve = self.get_derivative()
        return deriv_curve.get_point(t)

    def get_length(self, segments: int = 100) -> float:
        """
        Approximate the length of the Bezier curve by linear interpolation.
        """
        length = 0.0
        prev_point = self.get_point(0.0)
        for i in range(1, segments + 1):
            t = i / segments
            curr_point = self.get_point(t)
            length += math.dist(prev_point, curr_point)
            prev_point = curr_point
        return length

    def subdivide(self, t: float) -> Tuple['BezierCurve', 'BezierCurve']:
        """
        Subdivide the Bezier curve into two curves at parameter t using De Casteljau's algorithm.
        Returns (left_curve, right_curve)
        """
        if not 0 <= t <= 1:
            raise ValueError("Parameter t must be in [0, 1].")

        points = [self.control_points]
        while len(points[-1]) > 1:
            prev = points[-1]
            next_level = [
                (
                    (1 - t) * p0[0] + t * p1[0],
                    (1 - t) * p0[1] + t * p1[1]
                )
                for p0, p1 in zip(prev[:-1], prev[1:])
            ]
            points.append(next_level)

        left = [level[0] for level in points]
        right = [level[-1] for level in points[::-1]]

        return Bezier(left), Bezier(right)

    def sample(self, resolution: int = 100) -> List[Tuple[float, float]]:
        """
        Sample the curve at a number of evenly spaced points.
        """
        return [self.get_point(i / (resolution - 1)) for i in range(resolution)]


class CatmullRomSpline:
    def __init__(self, control_points: List[Tuple[float, float]], closed: bool = False, start_tangent: Optional[Tuple[float, float]] = None,
                 end_tangent: Optional[Tuple[float, float]] = None):
        """
        Create a Catmull-Rom spline that interpolates all control points.
        :param control_points: list of (x, y) points
        :param closed: whether the curve loops
        :param start_tangent: optional tangent vector at the start (dx, dy)
        :param end_tangent: optional tangent vector at the end (dx, dy)
        """
        if len(control_points) < 2:
            raise ValueError("At least 2 control points are required.")
        # self.points = control_points
        self.closed = closed
        self.original_points = control_points

        if closed:
            self.points = control_points + control_points[:2]  # wrap
        else:
            # Pad using tangent-based extrapolation if provided
            if start_tangent:
                first_virtual = (
                    control_points[0][0] - start_tangent[0],
                    control_points[0][1] - start_tangent[1]
                )
            else:
                first_virtual = control_points[0]

            if end_tangent:
                last_virtual = (
                    control_points[-1][0] + end_tangent[0],
                    control_points[-1][1] + end_tangent[1]
                )
            else:
                last_virtual = control_points[-1]

            self.points = [first_virtual] + control_points + [last_virtual]

    def __str__(self):
        # kind = "Closed" if self.closed else "Open"
        # return f"Catmull-Rom Spline ({kind}), {len(self.points)} points"
        kind = "Closed" if self.closed else "Open"
        return f"Catmull-Rom Spline ({kind}), {len(self.original_points)} points"

    def get_segment_points(self, i):
        """
        Returns 4 control points for segment i, adding duplicates or wrapping if needed.
        """
        n = len(self.points)
        def get(idx):
            if self.closed:
                return self.points[idx % n]
            else:
                # Clamp endpoints
                idx = min(max(idx, 0), n - 1)
                return self.points[idx]

        return get(i - 1), get(i), get(i + 1), get(i + 2)

    def get_point(self, t: float) -> Tuple[float, float]:
        """
        Evaluate point on the Catmull-Rom spline at global parameter t in [0, 1].
        """
        segment_count = len(self.points) - 3  # segments interpolate from P1 to P2
        t = max(0.0, min(1.0, t))  # clamp
        t_scaled = t * segment_count
        seg = min(int(t_scaled), segment_count - 1)
        local_t = t_scaled - seg

        p0 = self.points[seg]
        p1 = self.points[seg + 1]
        p2 = self.points[seg + 2]
        p3 = self.points[seg + 3]

        return self._catmull_rom(p0, p1, p2, p3, local_t)

    @staticmethod
    def _catmull_rom(p0, p1, p2, p3, t):
        """Compute Catmull-Rom interpolation for four points at parameter t ∈ [0, 1]."""
        t2 = t * t
        t3 = t2 * t
        x = 0.5 * (
            (2 * p1[0]) +
            (-p0[0] + p2[0]) * t +
            (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
            (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3
        )
        y = 0.5 * (
                (2 * p1[1]) +
                (-p0[1] + p2[1]) * t +
                (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
        )
        return (x, y)

    def sample(self, resolution: int = 100) -> List[Tuple[float, float]]:
        """
        Sample the curve at a number of evenly spaced points.
        """
        return [self.get_point(i / (resolution - 1)) for i in range(resolution)]

if __name__ == "__main__":
    c = (10, 10)
    l1 = Line((0, 0), (0, c[1]))     # svisla
    # l2 = Line((0, 0), c)                    # sikma
    # l21 = Line((c[0], 0), (0, c[1]) )  # sikma
    # l22 = Line((0, 0), c)  # sikma
    # l3 = Line((0, 0), (c[0], 0))       # vodorovna
    #

    # print(f"distance: {l1.get_point_distance(-3)}")
    #
    # intersection = l2.intersection(l21)
    # print(f"intersection: {intersection}")
    # print(f"\nl2 line: {str(l2)}")
    # print(f"start l2: {l2.get_start_point()}")
    # print(f"intersection point l2: {l2.get_y_point(5)}")
    # print(f"vector l2: {l2.get_vector()}")
    #
    # n = l2.normal_line(5)
    # print(f"\nnormal line: {str(n)}")
    # print(f"start n: {n.get_start_point()}")
    # print(f"vector n: {n.get_vector()}")
    # intersection2 = l2.intersection(n)
    # print(f"intersection2: {intersection2}")
    #
    # print(f"\nl21 line: {str(l21)}")
    # print(f"start l21: {l21.get_start_point()}")
    # print(f"intersection point l21: {l21.get_y_point(5)}")
    # print(f"vector l21: {l21.get_vector()}")
    #
    #
    #
    #
    # #
    # l4 = l2.parallel_line(-4)
    # print(f"start point parallel line: {l4.get_start_point()}")
    # print(f"0 point parallel line: {l4.get_y_point(0)}")
    #
    # # print(f"intersection: {l2.intersection(l22)}")
    #
    # l5 = l2.normal_line(1)
    # print(l5.get_end_point(-10))
    #
    # print("z1 line:")
    # z1 = Line((0,3), (2,7))
    # print(f"start point: {z1.get_start_point()}")
    # print(f"endf point: {z1.get_end_point()}")
    # print(f"y point on x={3}: {z1.get_y_point(3)}")
    # print(f"distance: {z1.get_point_distance(3)}")
    #
    # plt.plot((l2.get_start_point()[0], l2.get_end_point()[0]), (l2.get_start_point()[1], l2.get_end_point()[1]))
    # plt.plot((l4.get_start_point()[0], l4.get_end_point(10)[0]), (l4.get_start_point()[1], l4.get_end_point(10)[1]))
    # plt.show()

    # c = [(0, 0), (10, 10), (7, 15)]
    # c = [(0, 0), (10, 0), (10, 10), (0,10)]
    # # b1 = CatmullRomSpline([(0, 0), c])
    # b1 = CatmullRomSpline(c)
    # b2 = Bezier(c)
    # # b1 = CatmullRomSpline([(0,0), (c[0]/2,0), (c[0],c[1]/2), c])
    # print(b1)
    #
    # p = b1.get_point(1)
    # print(p)
    #
    # # p = []
    #
    #
    # plot = True
    # # print(po)
    #
    # # print(b1.get_point(1))
    #
    # if plot:
    #     n = 100
    #
    #     xb1 = []
    #     yb1 = []
    #     xb2 = []
    #     yb2 = []
    #     xc = []
    #     yc = []
    #     po = b1.sample(n)
    #     for i in po:
    #         xb1.append(i[0])
    #         yb1.append(i[1])
    #
    #     po = b2.sample(n)
    #     for i in po:
    #         xb2.append(i[0])
    #         yb2.append(i[1])
    #
    #     for k in c:
    #         xc.append(k[0])
    #         yc.append(k[1])
    #
    #     print(po)
    #
    #     plt.plot(xc, yc)
    #     plt.plot(xb1, yb1)
    #     plt.plot(xb2, yb2)
    #     plt.show()