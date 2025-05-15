from reportlab.lib.units import mm, cm
import geometry.base as base
from geometry.skeleton import cm_to_pt, pt_to_cm
from geometry.measurements import LowerMeasurements
import math
from typing import Optional, Dict
from dataclasses import dataclass
# import geomdl


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
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, scale: float = 1):
        self.raw_measurements = measurements
        self.measurements = self.raw_measurements.get_all_measurements(scale, "pt")
        self.x_pos = cm_to_pt(x_pos)
        self.y_pos = cm_to_pt(y_pos)
        self.factory = LineFactory(self.x_pos, self.y_pos, self.measurements)

    def get_center_line(self):
        return self.factory.center_line()

    def get_hip_line(self):
        y_offset = self.measurements["KD"]
        width = self.measurements["OS"] / 4.0 + cm_to_pt(6)
        return self.factory.horizontal_line_at(y_offset, width)

    def get_knee_line(self):
        y_offset = (self.measurements["KD"] / 2.0) + cm_to_pt(6)
        width = self.measurements["O_nk"]
        return self.factory.horizontal_line_at(y_offset, width)

    def get_calf_line(self):
        y_offset = (self.measurements["KD"] / 3.0) + cm_to_pt(4)
        width = self.measurements["O_l"]
        return self.factory.horizontal_line_at(y_offset, width)

    def get_ankle_line(self):
        y_offset = cm_to_pt(11)
        width = self.measurements["O_kot"] + cm_to_pt(5)
        return self.factory.horizontal_line_at(y_offset, width)

    def get_ground_line(self):
        y_offset = 0
        width = self.measurements["O_kot"] + cm_to_pt(7)
        return self.factory.horizontal_line_at(y_offset, width)

    def corner_divide_line(self):
        hip_height = self.get_hip_line().get_start_point()[1] - self.get_center_line().get_start_point()[1]
        y_offset = self.measurements["BDK"] - hip_height*0.5
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
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, scale: float = 1):
        self.base = HosenBaseSkeleton(x_pos, y_pos, measurements, scale)

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

        line_wide = (self.base.measurements["OP"]/4.0) + cm_to_pt(4)
        x_start = front_point_x
        x_end = x_start - line_wide

        return base.Line((x_start, y_level), (x_end, y_level))

    def get_back_waist_line(self):
        waist_point = self.get_front_waist_line().get_end_point()

        help_line_wide = (self.base.measurements["OP"]/4.0)
        y_end = waist_point[1] - cm_to_pt(5)
        x_end = waist_point[0] - help_line_wide

        help = base.Line(waist_point, (x_end, y_end))

        line_wide = (self.base.measurements["OP"] / 4.0) + cm_to_pt(5)
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
        dist = self.base.measurements["O_st"]/4
        print(f"dist: {dist}")
        end_point = normal.get_point_distance(-self.base.measurements["O_st"]/4)

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
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, scale: float = 1):
        self.base = HosenBaseSkeleton(x_pos, y_pos, measurements, scale)

    def corner_slope(self):
        hip = self.base.get_hip_line().get_end_point()
        const = -15
        x_end = hip[0] - cm_to_pt(const)
        y_end = hip[1] - cm_to_pt(const)

        return base.Line(hip, (x_end, y_end))

    def crotch_back(self):
        slope = self.corner_slope()
        wide = self.base.measurements["OS"]/20 + cm_to_pt(4)
        p = slope.get_point_distance(wide)
        normal = slope.normal_line(p[0])

        div_x, div_y = self.base.corner_divide_line().get_end_point()
        end = normal.get_x_point(div_y)

        return base.Line(normal.get_start_point(), (end, div_y))

    def slope_wide(self):
        help_line = self.corner_slope()
        help1 = base.Line(self.crotch_back().get_start_point(), vector=help_line.get_vector())
        dist = self.base.measurements["O_st"]/4 + cm_to_pt(3)
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

class HosenSkeleton:
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, scale: float = 1):
        self.base = HosenBaseSkeleton(x_pos, y_pos, measurements, scale)
        self.front = HosenFrontContour(x_pos, y_pos, measurements, scale)
        self.crotch = HosenCrotchSkeleton(x_pos, y_pos, measurements, scale)

    def get_skeleton_lines(self):
        base = self.base.get_skeleton_lines()
        front = self.front.get_skeleton_lines()
        crotch = self.crotch.get_skeleton_lines()

        # Return them organized by name
        return {**base, **front, **crotch}