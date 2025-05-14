from reportlab.lib.units import mm, cm
import geometry.base as base
import math
from typing import Optional
# import geomdl

def mm_to_pt(val):
    return val * mm


def cm_to_pt(val):
    return val * cm


def pt_to_cm(val):
    return val/cm


class Measurements:
    def __init__(self):
        self.meas = {}

    def add_chest(self, value):
        self.meas.update({"OH": float(value)})

    def add_waist(self, value):
        self.meas.update({"OP": float(value)})

    def add_back_length(self, value):
        self.meas.update({"DZ": float(value)})

    def add_back_width(self, value):
        self.meas.update({"Szad": float(value)})

    def get_all_measurements(self, scale: float = 1, unit: str = "cm"):
        """
        Returns all measurements scaled to the specified unit.

        Args:
            scale (float): Multiplier to scale all measurements.
            unit (str): Unit to convert to ("cm", "pt", "mm", or "in").

        Returns:
            dict: Scaled measurements in the desired unit.
        """
        unit_map = {
            "cm": 1,
            "mm": 10,
            "in": 2.54,  # 1 inch = 2.54 cm
            "pt": cm  # ReportLab point (1 pt = 1/72 inch = 0.3528 mm)
        }

        if unit not in unit_map:
            raise ValueError(f"Unsupported unit '{unit}'. Choose from: {list(unit_map.keys())}")

        conversion_factor = unit_map[unit]

        # Optional: return a new dictionary instead of modifying in place
        scaled_meas = {key: val * scale * conversion_factor for key, val in self.meas.items()}

        return scaled_meas


    def __str__(self):
        text = "Measured parameters:\n"
        for key in self.meas.keys():
            text_line = f"parameter {key}: value {self.meas[key]}"
            text = text + text_line + "\n"

        return text


class BackSkeleton:
    def __init__(self, x_pos, y_pos, measurements: Measurements, scale: float = 1):
        self.m = measurements.get_all_measurements(scale, "pt")
        self.x_pos = cm_to_pt(x_pos)
        self.y_pos = cm_to_pt(y_pos)


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

        # Return as a flat list: [x1, y1, x2, y2]
        # return [x_start, y_waist, x_end, y_waist]
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
        # y_top = armhole_line[3]  # end y of armhole line
        # y_bottom = waist_line[3]  # end y of waist line
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
        # y_top = neck_line[3]  # end y of neck line
        # y_bottom = armhole_line[3]  # end y of armhole line
        y_top = neck_line.get_end_point()[1]  # end y of neck line
        y_bottom = armhole_line.get_end_point()[1]  # end y of armhole line

        print("back line")
        print(f"x: {x}, y_top: {y_top}, y_bottom: {y_bottom}")

        # return [x, y_bottom, x, y_top]
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
        offset3cm = cm_to_pt(3)
        offset2cm = cm_to_pt(2)
        offset1cm = cm_to_pt(1)
        offset1p5cm = cm_to_pt(1.5)
        sk = self.get_skeleton_lines()
        neck = sk["neck"].get_start_point()
        back = sk["back"].get_start_point()
        chest = sk["chest"].get_start_point()
        waist = sk["waist"].get_start_point()
        side = sk["side"].get_start_point()
        armhole = sk["armhole"].get_start_point()

        print(f"sk: {sk}")

        shoulder = self.get_shoulder_line()
        side_curve = self.get_side_curve()

        points = []

        # points.append((back[0], neck[1]))
        # points.append((neck[0] + self.m["OH"] / 12, neck[1] - offset3cm))
        points.append(shoulder.get_end_point())
        points.append(shoulder.get_start_point())
        points.append((neck[0] + self.m["OH"] / 12, neck[1]))
        points.append((neck[0], neck[1]))
        points.append((chest[0], chest[1]))
        points.append((waist[0] + offset2cm, waist[1]))
        # points.append((waist[0] + offset2cm + self.m["OP"] / 4 - offset1cm, waist[1] + offset1cm))
        #
        # back_side = base.Line((waist[0] + offset2cm + self.m["OP"] / 4 - offset1cm, waist[1] + offset1cm),
        #                       (side[0], chest[1]))
        # points.append((back_side.get_x_point(armhole[1]), armhole[1]))
        points.append(side_curve.get_start_point())
        points.append((side_curve.get_x_point(armhole[1]), armhole[1]))


        print(f"points: {points}")

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

        # contour = self.get_contour()
        # points = []
        #
        # # starting points of final structure
        # points.append(self.get_armhole_edges()[0])
        # points.append(self.get_shoulder_line().get_start_point())
        #
        # # different types of neckline
        # if collar:
        #     # v-shape neckline for collar
        #     points.append(self.get_shoulder_line().get_start_point())
        #     back = base.Line(self.get_neck_line().get_start_point(), self.get_chest_line().get_start_point())
        #     points.append(back.get_point_distance(cm_to_pt(self.collar_depth)))
        # else:
        #     # smooth line for usage without collar
        #     neck_line_slope = self.get_shoulder_line().normal_line()
        #     neckhole_points = [self.get_shoulder_line().get_start_point(),
        #                        # (contour[3][0] + neck_width * (5.0 / 6), contour[2][1]),
        #                        (neck_line_slope.get_x_point(contour[3][1]), contour[3][1]),
        #                        contour[3]]
        #     # print(f"neckhole points: {neckhole_points}")
        #     if bezier_contour:
        #         for p in neckhole_points:
        #             points.append(p)
        #     else:
        #         neckhole = base.Bezier(neckhole_points)
        #         for p in neckhole.sample():
        #             points.append(p)
        #
        # # add points defined in basic contour -> back center and waist
        # points.append(contour[4])
        # points.append(contour[5])
        # points.append(contour[6])
        # points.append(contour[7])
        #
        #
        # # create armhole control points for bezier curve
        # armhole_shoulder_slope = self.get_shoulder_line().normal_line(self.get_armhole_edges()[0][0])
        # armhole_side_slope = self.get_side_curve().normal_line(self.get_armhole_edges()[1][0])
        # armhole_points = [self.get_armhole_edges()[1],
        #                   armhole_side_slope.get_point_distance(-cm_to_pt(10)),
        #                   armhole_shoulder_slope.get_point_distance(-cm_to_pt(13)),
        #                   self.get_armhole_edges()[0]]
        #
        # # switch draw smooth curve or curve input points
        # if bezier_contour:
        #     for p in armhole_points:
        #         points.append(p)
        # else:
        #     armhole = base.Bezier(armhole_points)
        #     for p in armhole.sample():
        #         points.append(p)
        #
        # return points

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

    def generate_collar(self):
        # ????????????????????????????????
        collar = CollarPattern(self.x_pos, self.y_pos, self.m)
        collar.set_collar_depth(self.collar_depth)
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
        # points = []
        #
        # center_point = self.get_neck_line().get_start_point()
        # points.append(self.get_shoulder_line().get_start_point())
        # back = base.Line(center_point, self.get_chest_line().get_start_point())
        #
        # if self.collar_depth:
        #     points.append(back.get_point_distance(cm_to_pt(self.collar_depth)))
        # else:
        #     if collar_depth:
        #         self.set_collar_depth(collar_depth)
        #         points.append(back.get_point_distance(cm_to_pt(self.collar_depth)))
        #     else:
        #         raise ValueError("Collar depth is not defined. Enter the value")
        #
        #
        # horiz_neck = base.Line(self.get_neck_line().get_point_distance(cm_to_pt(0.5)),
        #                        (center_point[0] + cm_to_pt(-0.5), center_point[1] + cm_to_pt(-5)))
        # points.append(horiz_neck.get_start_point())
        # points.append(horiz_neck.get_end_point())
        #
        # self.upper_edge = horiz_neck.normal_line(horiz_neck.get_end_point()[0])
        # self.lower_edge = self.upper_edge.parallel_line_point(self.get_shoulder_line().get_start_point())
        #
        # collar_front_point = self.lower_edge.get_point_distance(cm_to_pt(13))
        # normal_lower = self.lower_edge.normal_line(collar_front_point[0])
        # up_front_point = normal_lower.intersection(self.upper_edge)
        #
        # collar_height = normal_lower.line_length(up_front_point[0])
        # print(collar_height)
        #
        # upper_edge_length = self.upper_edge.line_length(up_front_point[0])
        #
        # front_slope = 3
        # point_to_slope_front = self.upper_edge.get_point_distance(upper_edge_length - cm_to_pt(front_slope))
        # print(f"upper_edge length: {self.upper_edge.line_length(up_front_point[0])}")
        #
        # # points.append(point_to_slope_front)
        #
        # front_curve_points = [self.upper_edge.get_point_distance(upper_edge_length - cm_to_pt(2*front_slope)),
        #                       point_to_slope_front,
        #                       collar_front_point]
        #
        #
        # # switch draw smooth curve or curve input points
        # if bezier_contour:
        #     for p in front_curve_points:
        #         points.append(p)
        # else:
        #     front_curve = base.Bezier(front_curve_points)
        #     for p in front_curve.sample():
        #         points.append(p)
        #
        # points.append(collar_front_point)
        # points.append(self.lower_edge.get_start_point())
        #
        # return points

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

    def set_collar_config(self, collar_depth: int = 13, back_height: Optional[float] = None, slope: Optional[float] = None):
        self.collar_depth = collar_depth

        if back_height:
            self.back_height = back_height

        if slope:
            self.slope = slope

    def get_collar_height(self):
        return pt_to_cm(self.collar_height)