from reportlab.lib.units import mm, cm
import geometry.base as base
from data.manage import cm_to_pt, pt_to_cm
from geometry.measurements import LowerMeasurements
from data.manage import TextLine
import math
from typing import Optional, Dict, List
from dataclasses import dataclass
# import geomdl
import json


@dataclass
class LineFactory:
    x_pos: float
    y_pos: float
    measurements: Dict[str, float]

    def center_line(self):
        origin = (self.x_pos, self.y_pos)
        end = (self.x_pos, self.y_pos + self.measurements["BDK"])
        return base.Line(origin, end)

    def horizontal_line_at(self, y_offset: float, width: float):
        y_level = self.y_pos + self.measurements["BDK"] - y_offset
        x_start, x_end = self._middle_line_x(width)
        return base.Line((x_start, y_level), (x_end, y_level))

    def _middle_line_x(self, width: float):
        return self.x_pos - width / 2, self.x_pos + width / 2


class HosenBaseSkeleton:
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, scale: float = 1, divide_line_offset: float = 0):
        self.raw_measurements = measurements
        # self.measurements = self.raw_measurements.get_all_measurements(scale, "pt")
        self.measurements = self.raw_measurements.get_all_measurements(scale, "cm")
        self.divide_line_offset = divide_line_offset



        # self.x_pos = cm_to_pt(x_pos)
        # self.y_pos = cm_to_pt(y_pos)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.factory = LineFactory(self.x_pos, self.y_pos, self.measurements)

        # print(f"self.measurements: {self.measurements}")
        # print(f"self.x_pos: {self.x_pos}")
        # print(f"self.y_pos: {self.y_pos}")

    def get_center_line(self):
        return self.factory.center_line()

    def get_hip_line(self):
        y_offset = self.measurements["KD"]
        width = self.measurements["OS"] / 4.0 + 6
        return self.factory.horizontal_line_at(y_offset, width)

    def get_knee_line(self):
        y_offset = (self.measurements["KD"] / 2.0) + 6
        width = self.measurements["O_nk"]
        return self.factory.horizontal_line_at(y_offset, width)

    def get_calf_line(self):
        y_offset = (self.measurements["KD"] / 3.0) + 4
        width = self.measurements["O_l"]
        return self.factory.horizontal_line_at(y_offset, width)

    def get_ankle_line(self):
        y_offset = 11
        width = self.measurements["O_kot"] + 5
        return self.factory.horizontal_line_at(y_offset, width)

    def get_ground_line(self):
        y_offset = 0
        width = self.measurements["O_kot"] + 7
        return self.factory.horizontal_line_at(y_offset, width)

    def corner_divide_line(self):
        hip_height = self.get_hip_line().get_start_point()[1] - self.get_center_line().get_start_point()[1]
        y_offset = self.measurements["BDK"] - hip_height*0.5 + self.divide_line_offset
        width = self.measurements["OS"]
        return self.factory.horizontal_line_at(y_offset, width)

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
        c_line = self.get_center_line()
        h_line = self.get_hip_line()
        k_line = self.get_knee_line()
        ca_line = self.get_calf_line()
        a_line = self.get_ankle_line()
        g_line = self.get_ground_line()
        d_line = self.corner_divide_line()

        # Return them organized by name
        return {
            "hip": h_line,
            "center": c_line,
            "knee": k_line,
            "calf": ca_line,
            "ankle": a_line,
            "ground": g_line,
            "divide": d_line
        }


class HosenFrontContour():
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, scale: float = 1, divide_line_offset: float = 0,
                 left_wide_offset: float = 1):
        self.base = HosenBaseSkeleton(x_pos, y_pos, measurements, scale, divide_line_offset)
        self.left_wide_offset = left_wide_offset

    def get_front_line(self):
        hip_x, hip_y = self.base.get_hip_line().get_end_point()
        x_level = hip_x - self.base.measurements["OS"]/20
        y_start = hip_y

        waist = self.base.get_center_line().get_start_point()
        y_end = waist[1]

        return base.Line((x_level, y_start), (x_level, y_end))

    def get_front_waist_line(self):
        front_point_x, front_point_y = self.get_front_line().get_end_point()
        y_level = front_point_y

        line_wide = (self.base.measurements["OP"]/4.0) + 4
        x_start = front_point_x
        x_end = x_start - line_wide

        return base.Line((x_start, y_level), (x_end, y_level))

    def get_back_waist_line(self):
        waist_point = self.get_front_waist_line().get_end_point()

        help_line_wide = (self.base.measurements["OP"]/4.0)
        y_end = waist_point[1] - 5
        x_end = waist_point[0] - help_line_wide

        help = base.Line(waist_point, (x_end, y_end))

        line_wide = (self.base.measurements["OP"] / 4.0) + 5
        end = help.get_point_distance(-line_wide)

        return base.Line(waist_point, end)

    def get_front_side_right(self, mode: int = 1):
        knee = self.base.get_knee_line()
        line_wide = knee.line_length() / 2
        x_start, x_end = self.base.factory._middle_line_x(line_wide)

        if mode == 1:
            return base.Line(self.base.get_hip_line().get_start_point(), (x_start, knee.get_start_point()[1]))
        else:
            return base.Line(self.base.get_hip_line().get_end_point(), (x_end, knee.get_end_point()[1]))

    def get_front_side_left(self):
        return base.Line(self.base.get_hip_line().get_end_point(), self.base.get_knee_line().get_end_point())

    def get_right_wide(self):
        right_front = self.get_front_side_right(1)
        normal = right_front.normal_line()
        dist = self.base.measurements["OS"]/8 + self.left_wide_offset
        # end_point = normal.get_point_distance(-self.base.measurements["O_st"]/4)
        end_point = normal.get_point_distance(-dist)

        return base.Line(right_front.get_start_point(), end_point)

    def upper_crotch(self):
        waist = self.get_back_waist_line()
        normal = waist.normal_line(waist.get_end_point()[0])

        div_x, div_y = self.base.corner_divide_line().get_end_point()
        end = normal.get_x_point(div_y)

        return base.Line(waist.get_end_point(), (end, div_y))

    def get_skeleton_lines(self):
        """
        Returns a dictionary of key structural lines used in pattern drafting.
        Each line represents a major horizontal or vertical measurement on the body.

        """

        # Get the main horizontal and vertical construction lines
        w_line = self.get_front_waist_line()
        wb_line = self.get_back_waist_line()
        fr_line = self.get_front_line()
        fsr_line = self.get_front_side_right(1)
        fsl_line = self.get_front_side_right(2)
        rw_line = self.get_right_wide()
        up_cr = self.upper_crotch()


        # Return them organized by name
        return {
            "waist": w_line,
            "waist_b": wb_line,
            "front": fr_line,
            "side_right": fsr_line,
            "side_left": fsl_line,
            "side_wide": rw_line,
            "upper_crotch": up_cr,
        }


class HosenCrotchSkeleton():
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, scale: float = 1, divide_line_offset: float = 0,
                 right_wide_offset: float = 0):
        self.base = HosenBaseSkeleton(x_pos, y_pos, measurements, scale, divide_line_offset)
        self.right_wide_offset = right_wide_offset

    def corner_slope(self):
        hip = self.base.get_hip_line().get_end_point()
        const = -5
        x_end = hip[0] - const
        y_end = hip[1] - const

        return base.Line(hip, (x_end, y_end))

    def crotch_back(self):
        slope = self.corner_slope()
        wide = self.base.measurements["OS"]/20 + 4
        p = slope.get_point_distance(wide)
        normal = slope.normal_line(p[0])

        div_x, div_y = self.base.corner_divide_line().get_end_point()
        end = normal.get_x_point(div_y)

        return base.Line(normal.get_start_point(), (end, div_y))

    def slope_wide(self):
        help_line = self.corner_slope()
        help1 = base.Line(self.crotch_back().get_start_point(), vector=help_line.get_vector())
        dist = self.base.measurements["OS"]/8 + self.right_wide_offset
        end = help1.get_point_distance(dist)

        return base.Line(help_line.get_end_point(), end)

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
        cor_sl = self.corner_slope()
        cr = self.crotch_back()
        sl_w = self.slope_wide()

        # Return them organized by name
        return {
            "cor_slope": cor_sl,
            "crotch": cr,
            "slope_wide": sl_w,
        }

class HosenPatternParameter:
    def __init__(self, waist_offset: float = 5, instep_width: float = 12, foot_finger_curve: float = 2,
                 upper_corner_tangent: float = 15, divide_line_offset: float = 0, left_wide_offset: float = 0,
                 right_wide_offset: float = 0):
        self.waist_offset = waist_offset
        self.instep_width = instep_width
        self.foot_finger_curve = foot_finger_curve
        self.upper_corner_tangent = upper_corner_tangent
        self.divide_line_offset = divide_line_offset
        self.left_wide_offset = left_wide_offset
        self.right_wide_offset = right_wide_offset

class HosenSkeleton:
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, param: HosenPatternParameter, scale: float = 1):
        self.base = HosenBaseSkeleton(x_pos, y_pos, measurements, scale, param.divide_line_offset)
        self.front = HosenFrontContour(x_pos, y_pos, measurements, scale, param.divide_line_offset, param.left_wide_offset)
        self.crotch = HosenCrotchSkeleton(x_pos, y_pos, measurements, scale, param.divide_line_offset, param.right_wide_offset)

    def get_skeleton_lines(self):
        base = self.base.get_skeleton_lines()
        front = self.front.get_skeleton_lines()
        crotch = self.crotch.get_skeleton_lines()

        # Return them organized by name
        return {**base, **front, **crotch}

    def check_thigh(self):
        lines = self.get_skeleton_lines()
        line_lenght = 0
        line_lenght += lines["side_wide"].line_length()
        line_lenght += lines["hip"].line_length()

        slope = base.Line(lines["hip"].get_end_point(), lines["slope_wide"].get_end_point())
        line_lenght += slope.line_length()

        print(f"side_wide lenght: {lines['side_wide'].line_length()}")
        print(f"hip lenght: {lines['hip'].line_length()}")
        print(f"slope lenght: {slope.line_length()}")

        print(f"line_lenght: {line_lenght}")
        print(f"thigh: {self.base.measurements['O_st']}")
        print(f"hip/2: {self.base.measurements['OS']/2}")

        thigh_text = f"thigh {round(self.base.measurements['O_st'],2)} ; line lenght: {round(line_lenght,2)}"

        return [thigh_text]





class HosenPattern(HosenSkeleton):
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, param: HosenPatternParameter, scale: float = 1):
        HosenSkeleton.__init__(self, x_pos, y_pos, measurements, param, scale)
        self.param = param
        self.lines = self.get_skeleton_lines()

    def get_pattern_points(self) -> list[tuple[float, float]]:
        """
            Generates a list of 2D points forming the full outline of the garment pattern
            using a combination of Bezier curves and Catmull-Rom splines.
            """
        points = []

        # === 1. Waistline Curve (Upper Edge) ===
        waist_offset = self.param.waist_offset
        waist_start = self.lines["waist"].get_start_point()
        waist_control = self.lines["waist"].get_end_point()
        waist_end = self.lines["waist_b"].get_end_point()

        waist_start_offset = (waist_start[0], waist_start[1] + waist_offset)
        waist_control_offset = (waist_control[0], waist_control[1] + waist_offset)
        waist_end_offset = self.lines["upper_crotch"].get_point_distance(-waist_offset)

        waist_curve = base.Bezier([waist_start_offset, waist_control_offset, waist_end_offset])
        points += waist_curve.sample()
        points.append(self.lines["upper_crotch"].get_end_point())

        # === 2. Left Side Curve (Upper to Ground) ===
        upper_crotch_end = self.lines["upper_crotch"].get_end_point()
        side_wide_end = self.lines["side_wide"].get_end_point()

        start_tangent = self.lines["upper_crotch"].normal_line(upper_crotch_end[0])
        end_tangent = base.Line(side_wide_end, self.lines["knee"].get_start_point())

        left_upper_curve = base.Bezier([
            upper_crotch_end,
            start_tangent.get_point_distance(10),
            end_tangent.get_point_distance(-5),
            side_wide_end
        ])
        points += left_upper_curve.sample()

        left_lower_curve = base.CatmullRomSpline([
            side_wide_end,
            self.lines["knee"].get_start_point(),
            self.lines["calf"].get_start_point(),
            self.lines["ankle"].get_start_point(),
            self.lines["ground"].get_start_point()
        ])
        points += left_lower_curve.sample()

        # === 3. Foot Section (Bottom Curve) ===
        left_tangent = base.Line(points[-1], points[-2])
        left_ground = left_tangent.normal_line(left_tangent.get_start_point()[0])

        y_offset = self.lines['center'].get_end_point()[1] - self.lines['ankle'].get_start_point()[1]
        width = self.param.instep_width
        foot_line = self.base.factory.horizontal_line_at(y_offset, width)

        left_foot = left_tangent.parallel_line_point(foot_line.get_start_point())
        left_intersection = left_ground.intersection(left_foot)
        points.append(left_intersection)
        points.append(foot_line.get_start_point())

        # Define smooth foot curve
        bottom_offset = self.param.foot_finger_curve
        contour1 = base.Line(left_intersection, vector=(-1, 1))
        contour1_point = contour1.get_point_distance(-10)

        contour2 = contour1.normal_line(contour1_point[0])
        contour_middle = (self.base.x_pos, contour2.get_y_point(self.base.x_pos))
        contour_slope1 = (left_foot.get_x_point(contour_middle[1] - bottom_offset), contour_middle[1] - bottom_offset)

        contour3 = contour1.parallel_line_point(contour_middle)

        # === 4. Right Side Curve (Ground to Hip) ===
        right_lower_curve = base.CatmullRomSpline([
            self.lines["ground"].get_end_point(),
            self.lines["ankle"].get_end_point(),
            self.lines["calf"].get_end_point(),
            self.lines["knee"].get_end_point(),
            self.lines["slope_wide"].get_end_point()
        ])
        right_curve_pts = right_lower_curve.sample()

        right_tangent = base.Line(right_curve_pts[0], right_curve_pts[1])
        right_ground = right_tangent.normal_line(right_tangent.get_start_point()[0])

        right_foot = right_tangent.parallel_line_point(foot_line.get_end_point())
        right_intersection = right_ground.intersection(right_foot)
        contour_slope2 = (right_foot.get_x_point(contour_middle[1] - bottom_offset), contour_middle[1] - bottom_offset)
        contour3_point = (contour3.get_x_point(contour1_point[1]), contour1_point[1])

        # === 5. Append Foot Curve (Smooth or Cornered) ===
        smooth_foot = True
        if smooth_foot:
            foot_curve = base.CatmullRomSpline([
                left_intersection,
                contour1_point,
                contour_slope1,
                contour_middle,
                contour_slope2,
                contour3_point,
                right_intersection
            ])
            points += foot_curve.sample()
        else:
            points += [
                left_intersection, contour1_point, contour_slope1,
                contour_middle, contour_slope2, contour3_point, right_intersection
            ]

        points.append(foot_line.get_end_point())
        points.append(right_intersection)

        # === 6. Inner Right Curve (Hip to Crotch) ===
        right_upper_corner_tangent = self.param.upper_corner_tangent
        # points.append(right_ground.get_point_distance(-5))
        points.append(right_intersection)
        points += right_curve_pts

        crotch_end = self.lines["crotch"].get_end_point()
        end_tangent = self.lines["crotch"].normal_line(crotch_end[0])
        right_inner_curve = base.Bezier([
            self.lines["slope_wide"].get_end_point(),
            end_tangent.get_point_distance(right_upper_corner_tangent),
            crotch_end
        ])
        points += right_inner_curve.sample()

        # === 7. Final Front Crotch Curve ===
        x1, y1 = self.lines["hip"].get_end_point()
        x2, y2 = self.lines["front"].get_start_point()
        end_curve_point = (x2, y2 - (x1 - x2))

        front_crotch_curve = base.Bezier([
            crotch_end,
            self.lines["crotch"].get_start_point(),
            self.lines["hip"].get_end_point(),
            self.lines["front"].get_start_point(),
            end_curve_point
        ])
        points += front_crotch_curve.sample()

        # Close loop at top waist
        points.append(waist_start_offset)

        # Debug prints
        # print(f"front_curve_points: {[waist_start_offset, waist_control_offset, waist_end_offset]}")
        # print(f"points: {points}")

        return points

    def get_lines_description(self):
        descriptions = []
        y_offset = -0.1
        x_offset = 0.5
        x_center_position = self.lines["center"].get_start_point()[0] + x_offset


        # waist description
        x_pos = self.lines["waist"].get_start_point()[1] + y_offset
        text = "WAIST LINE"
        descriptions.append(TextLine(x_center_position, x_pos, text))

        # hip description
        x_pos = self.lines["divide"].get_start_point()[1] + y_offset
        text = "HIP LINE"
        descriptions.append(TextLine(x_center_position, x_pos, text))

        # thight description
        x_pos = self.lines["hip"].get_start_point()[1] + y_offset
        text = "THIGHT LINE"
        descriptions.append(TextLine(x_center_position, x_pos, text))

        # knee description
        x_pos = self.lines["knee"].get_start_point()[1] + y_offset
        text = "KNEE LINE"
        descriptions.append(TextLine(x_center_position, x_pos, text))

        # calf description
        x_pos = self.lines["calf"].get_start_point()[1] + y_offset
        text = "CALF LINE"
        descriptions.append(TextLine(x_center_position, x_pos, text))

        # ankle description
        x_pos = self.lines["ankle"].get_start_point()[1] + y_offset
        text = "ANKLE LINE"
        descriptions.append(TextLine(x_center_position, x_pos, text))

        return descriptions

    def get_main_description(self, title = None):
        y_offset = -0.5*(self.lines["hip"].get_start_point()[1] - self.lines["knee"].get_start_point()[1])
        x_offset = 0.5

        x_pos = self.lines["center"].get_start_point()[0] + x_offset
        y_pos = self.lines["hip"].get_start_point()[1] + y_offset

        if not title:
            title = self.base.measurements['title']

        text = ("JOINED HOSEN\n"
                "\n"
                f"{title}\n"
                f"OP {self.base.measurements['OP']}\n"
                f"OS {self.base.measurements['OS']}\n"
                f"BDK {self.base.measurements['BDK']}\n"
                f"KD {self.base.measurements['KD']}\n"
                f"Ost {self.base.measurements['O_st']}")

        return TextLine(x_pos, y_pos, text)

    def get_important_points(self):
        points = []
        points.append(self.lines["knee"].get_start_point())
        points.append(self.lines["knee"].get_end_point())
        points.append(self.lines["hip"].get_end_point())

        return points
