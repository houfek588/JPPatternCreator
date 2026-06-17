from reportlab.lib.units import mm, cm
import geometry.base as base
import math
from geometry.measurements import Measurements
from data.manage import cm_to_pt, pt_to_cm, mm_to_pt
from typing import Optional
# import geomdl







class BackSkeleton:
    def __init__(self, x_pos, y_pos, measurements: Measurements, scale: float = 1):
        self.measurements = measurements
        self.measurements.validate()
        self.m = self.measurements.get_all_measurements(scale, "pt")
        self.x_pos = cm_to_pt(x_pos)
        self.y_pos = cm_to_pt(y_pos)


    # def _get_measurements(self):
    #     return self.measurements.get_all_measurements(self.scale, "pt")

    def get_center_line(self):
        origin = (0 + self.x_pos, 0 + self.y_pos)
        end = (0 + self.x_pos, self.m["DZ"] + self.y_pos)
        # return [origin, end]
        return base.Line(origin, end)
        # return [origin[0], origin[1], end[0], end[1]]

    def get_waist_line(self):
        """Returns a horizontal waist guideline defined by origin and end point coordinates."""

        # Calculate the vertical position of the waistline
        y_waist = self.m["DZ"] + self.y_pos

        # Calculate the start and end x-positions
        x_start = self.x_pos
        x_end = x_start + (1.2 * self.m["OH"] / 4)  # 1.2 * quarter of outer height

        # Return as a flat list: [(x1, y1), (x2, y2)]
        return base.Line((x_start, y_waist), (x_end, y_waist))

    def get_chest_line(self):
        """Returns a horizontal chest guideline as a flat list of coordinates: [x1, y1, x2, y2]."""

        # Convert 20 mm to points
        chest_offset = mm_to_pt(20)

        # Calculate vertical Y position of the chest line
        y_chest = (self.m["DZ"] / 2) + chest_offset + self.y_pos

        # Define horizontal start and end X positions
        x_start = self.x_pos
        x_end = x_start + (1.2 * self.m["OH"] / 4)  # Adjusted width

        # Return line as flat list
        # return [x_start, y_chest, x_end, y_chest]
        return base.Line((x_start, y_chest), (x_end, y_chest))

    def get_armhole_line(self):
        """Returns a horizontal armhole guideline as a flat list of coordinates: [x1, y1, x2, y2]."""

        # Calculate vertical Y position for the armhole line
        y_armhole = (self.m["DZ"] / 3) + (self.m["DZ"] / 8) + self.y_pos

        # Define horizontal start and end X positions
        x_start = self.x_pos
        x_end = x_start + (1.2 * self.m["OH"] / 4)  # Adjusted line width

        # Return line coordinates as a flat list
        # return [x_start, y_armhole, x_end, y_armhole]
        return base.Line((x_start, y_armhole), (x_end, y_armhole))

    def get_neck_line(self):
        """Returns a horizontal neckline guideline as a flat list of coordinates: [x1, y1, x2, y2]."""

        y_neck = self.y_pos
        x_start = self.x_pos
        x_end = x_start + (1.2 * self.m["OH"] / 4)  # Line width based on opening height (OH)

        # return [x_start, y_neck, x_end, y_neck]
        return base.Line((x_start, y_neck), (x_end, y_neck))

    def get_side_line(self):
        """
        Returns a vertical side seam line as a flat list of coordinates: [x1, y1, x2, y2].

        The line connects from the armhole level down to the waistline level,
        offset horizontally by OH/4 plus an additional 20mm.
        """

        # Get y-coordinates from previously defined horizontal lines
        armhole_line = self.get_armhole_line()
        waist_line = self.get_waist_line()


        # Convert 2 cm to points for consistent scaling
        offset = cm_to_pt(2)

        # Compute constant horizontal x-position for the vertical side line
        x = (self.m["OH"] / 4) + offset + self.x_pos

        # Use y-values from the corresponding line ends
        y_top = armhole_line.get_end_point()[1]  # end y of armhole line
        y_bottom = waist_line.get_end_point()[1]  # end y of waist line

        # return [x, y_top, x, y_bottom]
        return base.Line((x, y_top), (x, y_bottom))

    def get_back_line(self):
        """
        Returns a vertical line representing the back seam, from the armhole level to the neckline level.
        The x-position is placed at half the back width (Szad), adjusted by the horizontal position offset.
        The y-positions are based on existing armhole and neckline lines.
        """

        # Get y-coordinates from helper line methods
        armhole_line = self.get_armhole_line()
        neck_line = self.get_neck_line()

        # Calculate x-position for the back line (middle of back width)
        x = (self.m["Szad"] / 2) + self.x_pos

        # y-coordinates from previously defined lines
        y_top = neck_line.get_end_point()[1]  # end y of neck line
        y_bottom = armhole_line.get_end_point()[1]  # end y of armhole line

        # return [(x, y_bottom), (x, y_top)]
        return base.Line((x, y_bottom), (x, y_top))

    def get_skeleton_lines(self):
        """
        Returns a dictionary of key structural lines used in pattern drafting.
        Each line represents a major horizontal or vertical measurement on the body.

        Returns:
            dict: A dictionary with named keys corresponding to specific lines:
                - "neck": neckline baseline
                - "armhole": horizontal line at armhole depth
                - "chest": horizontal line at chest level
                - "waist": horizontal waistline
                - "center": vertical center front or back
                - "side": vertical side seam
                - "back": vertical back seam
        """

        # Get the main horizontal and vertical construction lines
        w_line = self.get_waist_line()
        ch_line = self.get_chest_line()
        a_line = self.get_armhole_line()
        n_line = self.get_neck_line()
        side_line = self.get_side_line()
        back_line = self.get_back_line()
        c_line = self.get_center_line()

        # Return them organized by name
        return {
            "neck": n_line,
            "armhole": a_line,
            "chest": ch_line,
            "waist": w_line,
            "center": c_line,
            "side": side_line,
            "back": back_line
        }


class BackContour(BackSkeleton):
    def __init__(self, x_pos, y_pos, measurements:Measurements, scale: float = 1):
        BackSkeleton.__init__(self, x_pos, y_pos, measurements, scale)

    def get_contour(self):
        """
            Returns a list of contour points based on the skeleton lines and defined geometric logic.
            These points typically represent key areas of a bodice pattern like neckline, shoulder, chest, waist, and armhole.
            """

        # Precomputed offsets for shaping (in points)
        offset_3cm = cm_to_pt(3)
        offset_2cm = cm_to_pt(2)
        offset_1cm = cm_to_pt(1)

        # Get critical skeleton points
        sk = self.get_skeleton_lines()
        neck = sk["neck"].get_start_point()
        back = sk["back"].get_start_point()
        chest = sk["chest"].get_start_point()
        waist = sk["waist"].get_start_point()
        side = sk["side"].get_start_point()
        armhole = sk["armhole"].get_start_point()

        # Useful curve objects
        shoulder_line = self.get_shoulder_line()
        side_curve = self.get_side_curve()

        # Begin assembling contour point list
        points = []

        # 1. Shoulder line
        points.append(shoulder_line.get_end_point())  # End of shoulder (near neck)
        points.append(shoulder_line.get_start_point())  # Start of shoulder (toward armhole)

        # 2. Neck shaping (slightly extended from base neck point)
        neck_extension_x = neck[0] + self.m["OH"] / 12
        points.append((neck_extension_x, neck[1]))  # Projected neckline curve point
        points.append(neck)  # Base of neck

        # 3. Chest and waist shaping
        points.append(chest)  # Chest point
        points.append((waist[0] + offset_2cm, waist[1]))  # Waist with horizontal shaping

        # 4. Side shaping using Bezier curve logic (curve start and interpolation for armhole height)
        points.append(side_curve.get_start_point())  # Side curve near waist
        armhole_x = side_curve.get_x_point(armhole[1])  # Interpolated X at armhole Y
        points.append((armhole_x, armhole[1]))  # Final point near armhole

        # print(f"points: {points}")

        return points

    def get_shoulder_line(self):
        offset3cm = cm_to_pt(3)
        neck = self.get_neck_line().get_start_point()
        back = self.get_back_line().get_start_point()

        shoulder_line = base.Line((neck[0] + self.m["OH"] / 12, neck[1] - offset3cm), (back[0], neck[1]))
        return shoulder_line

    def get_armhole_edges(self):
        points = self.get_contour()

        shoulder = self.get_shoulder_line()

        origin = shoulder.get_point_distance(cm_to_pt(3))
        end = points[-1]

        return (origin,end)

    def get_side_curve(self):
        offset2cm = cm_to_pt(2)
        offset1cm = cm_to_pt(1)
        sk = self.get_skeleton_lines()
        chest = sk["chest"].get_start_point()
        waist = sk["waist"].get_start_point()
        side = sk["side"].get_start_point()

        return base.Line((waist[0] + offset2cm + self.m["OP"] / 4 - offset1cm, waist[1] + offset1cm),
                  (side[0], chest[1]))


class BackPattern(BackContour):
    def __init__(self, x_pos, y_pos, measurements:Measurements, scale: float = 1):
        BackContour.__init__(self, x_pos, y_pos, measurements, scale)
        self.collar_depth = 12

    def get_pattern_points(self, collar: bool = False, bezier_contour: bool = False) -> list[tuple[float, float]]:
        """
            Generates a list of 2D points outlining the pattern shape, depending on collar and contour type.

            :param collar: If True, generates a V-shaped neckline for a collar; else a smooth curved neckline.
            :param bezier_contour: If True, use raw control points for neckhole and armhole instead of smooth curves.
            :return: List of 2D points outlining the pattern.
            """
        points = []
        points += self._get_upper_opening_points(collar, bezier_contour)
        points += self._get_back_and_waist_points()
        points += self._get_armhole_points(bezier_contour)
        return points

    def _get_upper_opening_points(self, collar: bool, bezier: bool) -> list[tuple[float, float]]:
        points = [
            self.get_armhole_edges()[0],
            self.get_shoulder_line().get_start_point()
        ]

        if collar:
            # V-shaped neckline for a collar
            shoulder_start = self.get_shoulder_line().get_start_point()
            back = base.Line(self.get_neck_line().get_start_point(), self.get_chest_line().get_start_point())
            v_neck_point = back.get_point_distance(cm_to_pt(self.collar_depth))

            points.append(shoulder_start)
            points.append(v_neck_point)
        else:
            # Smooth curved neckline without collar
            shoulder_start = self.get_shoulder_line().get_start_point()
            contour = self.get_contour()
            neck_line_slope = self.get_shoulder_line().normal_line()

            # Neckhole Bezier control points
            neckhole_points = [
                shoulder_start,
                (neck_line_slope.get_x_point(contour[3][1]), contour[3][1]),
                contour[3]
            ]

            if bezier:
                points += neckhole_points
            else:
                bezier_curve = base.Bezier(neckhole_points)
                points += bezier_curve.sample()

        return points

    def _get_back_and_waist_points(self) -> list[tuple[float, float]]:
        contour = self.get_contour()
        # points: back center (4), waist top/bottom (5,6), side seam base (7)
        return [contour[i] for i in range(4, 8)]

    def _get_armhole_points(self, bezier: bool) -> list[tuple[float, float]]:
        armhole_start, armhole_end = self.get_armhole_edges()
        shoulder_normal = self.get_shoulder_line().normal_line(armhole_start[0])
        side_normal = self.get_side_curve().normal_line(armhole_end[0])

        # Control points for the armhole curve
        control_points = [
            armhole_end,
            side_normal.get_point_distance(-cm_to_pt(10)),
            shoulder_normal.get_point_distance(-cm_to_pt(13)),
            armhole_start
        ]

        if bezier:
            return control_points
        else:
            bezier_curve = base.Bezier(control_points)
            return bezier_curve.sample()

    def generate_collar(self, collar_depth: int = 12, back_height: Optional[float] = None, slope: Optional[float] = None):
        self.collar_depth = collar_depth

        collar = CollarPattern(pt_to_cm(self.x_pos), pt_to_cm(self.y_pos), self.measurements)
        collar.set_collar_config(self.collar_depth, back_height, slope)
        return collar


class CollarPattern(BackContour):
    def __init__(self, x_pos, y_pos, measurements: Measurements, scale: float = 1):
        BackContour.__init__(self, x_pos, y_pos, measurements, scale)
        self.upper_edge = None
        self.lower_edge = None
        self.collar_height = None

        self.collar_depth = None
        self.back_height = 5
        self.slope = 3


    def get_pattern_points(self, collar_depth: Optional[int] = None, bezier_contour: bool = False) -> list[tuple[float, float]]:
        """
            Generates collar pattern points based on collar depth and contour smoothness.

            :param collar_depth: Optional override for the collar depth in cm.
            :param bezier_contour: If True, uses control points directly. If False, interpolates with a Bezier curve.
            :return: List of 2D points forming the collar pattern.
            """
        self._ensure_collar_depth(collar_depth)

        center_point = self.get_neck_line().get_start_point()
        chest_point = self.get_chest_line().get_start_point()
        shoulder_start = self.get_shoulder_line().get_start_point()

        points = [shoulder_start]

        # Step 1: Calculate base back line and collar tip
        back_line = base.Line(center_point, chest_point)
        collar_tip = back_line.get_point_distance(cm_to_pt(self.collar_depth))
        points.append(collar_tip)

        # Step 2: Build horizontal neck construction line
        horiz_neck = base.Line(
            self.get_neck_line().get_point_distance(cm_to_pt(0.5)),
            (center_point[0] - cm_to_pt(0.5), center_point[1] - cm_to_pt(self.back_height))
        )
        points += [horiz_neck.get_start_point(), horiz_neck.get_end_point()]

        # Step 3: Define upper/lower collar edge
        self.upper_edge = horiz_neck.normal_line(horiz_neck.get_end_point()[0])
        self.lower_edge = self.upper_edge.parallel_line_point(shoulder_start)

        # Step 4: Front and slope logic
        collar_front_point = self.lower_edge.get_point_distance(cm_to_pt(13))
        normal_lower = self.lower_edge.normal_line(collar_front_point[0])
        up_front_point = normal_lower.intersection(self.upper_edge)

        upper_edge_length = self.upper_edge.line_length(up_front_point[0])
        slope_length = cm_to_pt(self.slope)

        point_to_slope_front = self.upper_edge.get_point_distance(upper_edge_length - slope_length)
        curve_start = self.upper_edge.get_point_distance(upper_edge_length - 2 * slope_length)

        front_curve_points = [curve_start, point_to_slope_front, collar_front_point]

        # Step 5: Generate curve or raw control points
        if bezier_contour:
            points += front_curve_points
        else:
            front_curve = base.Bezier(front_curve_points)
            points += front_curve.sample()

        # Step 6: Final point and return
        points.append(collar_front_point)
        points.append(self.lower_edge.get_start_point())

        self.collar_height = normal_lower.line_length(up_front_point[0])
        return points


    def _ensure_collar_depth(self, collar_depth: Optional[int]):
        """
        Ensures collar depth is set either from internal state or provided argument.
        """
        if self.collar_depth:
            return
        if collar_depth:
            self.set_collar_config(collar_depth)
        else:
            raise ValueError("Collar depth is not defined. Enter the value.")

    def set_collar_config(self, collar_depth: int = 12, back_height: Optional[float] = None, slope: Optional[float] = None):
        self.collar_depth = collar_depth

        if back_height:
            self.back_height = back_height

        if slope:
            self.slope = slope

    def get_collar_height(self):
        return pt_to_cm(self.collar_height)