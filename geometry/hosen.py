from reportlab.lib.units import mm, cm
import geometry.base as base
from geometry.skeleton import cm_to_pt
import math
from typing import Optional
# import geomdl


class LowerMeasurements:
    def __init__(self):
        self.meas = {}

    def add_hips(self, value):
        self.meas.update({"OS": float(value)})

    def add_waist(self, value):
        self.meas.update({"OP": float(value)})

    def add_side_hose_length(self, value):
        self.meas.update({"BDK": float(value)})

    def add_step_length(self, value):
        self.meas.update({"KD": float(value)})

    def add_circumference_thigh(self, value):
        self.meas.update({"O_st": float(value)})

    def add_circumference_above_knee(self, value):
        self.meas.update({"O_nk": float(value)})

    def add_circumference_calf(self, value):
        self.meas.update({"O_l": float(value)})

    def add_circumference_ankle(self, value):
        self.meas.update({"O_kot": float(value)})

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


class HosenSkeleton:
    def __init__(self, x_pos, y_pos, measurements: LowerMeasurements, scale: float = 1):
        # self.m = measurements.get_all_measurements(scale, "pt")
        self.measurements = measurements
        # self.scale = scale
        self.m = self.measurements.get_all_measurements(scale, "pt")
        self.x_pos = cm_to_pt(x_pos)
        self.y_pos = cm_to_pt(y_pos)


    # def _get_measurements(self):
    #     return self.measurements.get_all_measurements(self.scale, "pt")
    def _middle_vertical_line(self, point, length):
        line_wide = length
        x_start = point - line_wide / 2
        x_end = point + line_wide / 2

        return (x_start, x_end)

    def get_center_line(self):
        origin = (0 + self.x_pos, 0 + self.y_pos)
        end = (0 + self.x_pos, self.y_pos + self.m["BDK"])
        # return [origin, end]
        return base.Line(origin, end)
        # return [origin[0], origin[1], end[0], end[1]]

    def get_hip_line(self):

        waist_point = self.get_center_line().get_start_point()
        ground_point = self.get_center_line().get_end_point()

        y_level = ground_point[1] - self.m["KD"]
        line_wide = (self.m["OS"] / 4.0) + cm_to_pt(6)
        x_start, x_end = self._middle_vertical_line(self.x_pos, line_wide)

        # x_start = self.x_pos - line_wide/2
        # x_end = self.x_pos + line_wide/2


        # Calculate the start and end x-positions
        # x_start = self.x_pos
        # x_end = x_start + (1.2 * self.m["OH"] / 4)  # 1.2 * quarter of outer height

        # Return as a flat list: [(x1, y1), (x2, y2)]
        return base.Line((x_start, y_level), (x_end, y_level))



    def get_knee_line(self):
        waist_point = self.get_center_line().get_start_point()
        ground_point = self.get_center_line().get_end_point()

        y_level = ground_point[1] - ((self.m["KD"]/2)+cm_to_pt(6))

        line_wide = self.m["O_nk"]
        x_start, x_end = self._middle_vertical_line(self.x_pos, line_wide)
        # x_start = self.x_pos - line_wide/2
        # x_end = self.x_pos + line_wide/2


        # Calculate the start and end x-positions
        # x_start = self.x_pos
        # x_end = x_start + (1.2 * self.m["OH"] / 4)  # 1.2 * quarter of outer height

        # Return as a flat list: [(x1, y1), (x2, y2)]
        return base.Line((x_start, y_level), (x_end, y_level))

    def get_calf_line(self):
        waist_point = self.get_center_line().get_start_point()
        ground_point = self.get_center_line().get_end_point()

        y_level = ground_point[1] - ((self.m["KD"]/3)+cm_to_pt(4))

        line_wide = self.m["O_l"]
        x_start, x_end = self._middle_vertical_line(self.x_pos, line_wide)
        # x_start = self.x_pos - line_wide/2
        # x_end = self.x_pos + line_wide/2


        # Calculate the start and end x-positions
        # x_start = self.x_pos
        # x_end = x_start + (1.2 * self.m["OH"] / 4)  # 1.2 * quarter of outer height

        # Return as a flat list: [(x1, y1), (x2, y2)]
        return base.Line((x_start, y_level), (x_end, y_level))

    def get_ankle_line(self):
        waist_point = self.get_center_line().get_start_point()
        ground_point = self.get_center_line().get_end_point()

        y_level = ground_point[1] - cm_to_pt(11)

        line_wide = self.m["O_kot"] + cm_to_pt(5)
        x_start, x_end = self._middle_vertical_line(self.x_pos, line_wide)
        # x_start = self.x_pos - line_wide/2
        # x_end = self.x_pos + line_wide/2


        # Calculate the start and end x-positions
        # x_start = self.x_pos
        # x_end = x_start + (1.2 * self.m["OH"] / 4)  # 1.2 * quarter of outer height

        # Return as a flat list: [(x1, y1), (x2, y2)]
        return base.Line((x_start, y_level), (x_end, y_level))

    def get_ground_line(self):
        waist_point = self.get_center_line().get_start_point()
        ground_point = self.get_center_line().get_end_point()

        y_level = ground_point[1]

        line_wide = self.m["O_kot"] + cm_to_pt(7)
        x_start, x_end = self._middle_vertical_line(self.x_pos, line_wide)
        # x_start = self.x_pos - line_wide / 2
        # x_end = self.x_pos + line_wide / 2

        # Calculate the start and end x-positions
        # x_start = self.x_pos
        # x_end = x_start + (1.2 * self.m["OH"] / 4)  # 1.2 * quarter of outer height

        # Return as a flat list: [(x1, y1), (x2, y2)]
        return base.Line((x_start, y_level), (x_end, y_level))

    def get_front_line(self):
        hip_x, hip_y = self.get_hip_line().get_end_point()

        x_level = hip_x - self.m["OS"]/20

        y_start = hip_y

        waist = self.get_center_line().get_start_point()
        y_end = waist[1]

        return base.Line((x_level, y_start), (x_level, y_end))

    def get_front_waist_line(self):

        front_point_x, front_point_y = self.get_front_line().get_end_point()
        waist_point = self.get_center_line().get_start_point()
        ground_point = self.get_center_line().get_end_point()

        y_level = front_point_y

        line_wide = (self.m["OP"]/4.0) + cm_to_pt(4)
        x_start = front_point_x
        x_end = x_start - line_wide

        return base.Line((x_start, y_level), (x_end, y_level))

    def get_back_waist_line(self):
        waist_point = self.get_front_waist_line().get_end_point()

        help_line_wide = (self.m["OP"]/4.0)
        y_end = waist_point[1] - cm_to_pt(5)
        x_end = waist_point[0] - help_line_wide

        help = base.Line(waist_point, (x_end, y_end))

        line_wide = (self.m["OP"] / 4.0) + cm_to_pt(5)
        end = help.get_point_distance(-line_wide)

        return base.Line(waist_point, end)

    def get_front_side_right(self, mode: int = 1):
        knee = self.get_knee_line()
        line_wide = knee.line_length() / 2
        x_start, x_end = self._middle_vertical_line(self.x_pos, line_wide)

        if mode == 1:
            return base.Line(self.get_hip_line().get_start_point(), (x_start, knee.get_start_point()[1]))
        else:
            return base.Line(self.get_hip_line().get_end_point(), (x_end, knee.get_end_point()[1]))

    def get_front_side_left(self):
        return base.Line(self.get_hip_line().get_end_point(), self.get_knee_line().get_end_point())

    def get_right_wide(self):
        right_front = self.get_front_side_right(1)
        normal = right_front.normal_line()
        dist = self.m["O_st"]/4
        print(f"dist: {dist}")
        end_point = normal.get_point_distance(-self.m["O_st"]/4)

        return base.Line(right_front.get_start_point(), end_point)

    def corner_slope(self):
        hip = self.get_hip_line().get_end_point()

        const = -15
        x_end = hip[0] - cm_to_pt(const)
        y_end = hip[1] - cm_to_pt(const)

        return base.Line(hip, (x_end, y_end))

    def crotch_back(self):
        slope = self.corner_slope()
        wide = self.m["OS"]/20 + cm_to_pt(4)
        p = slope.get_point_distance(wide)
        normal = slope.normal_line(p[0])

        div_x, div_y = self.corner_divide_line().get_end_point()
        end = normal.get_x_point(div_y)

        return base.Line(normal.get_start_point(), (end, div_y))

    def upper_crotch(self):
        waist = self.get_back_waist_line()
        normal = waist.normal_line(waist.get_end_point()[0])

        div_x, div_y = self.corner_divide_line().get_end_point()
        end = normal.get_x_point(div_y)

        return base.Line(waist.get_end_point(), (end, div_y))

    def slope_wide(self):
        help_line = self.corner_slope()
        help1 = base.Line(self.crotch_back().get_start_point(), vector=help_line.get_vector())
        dist = self.m["O_st"]/4 + cm_to_pt(3)
        end = help1.get_point_distance(dist)

        return base.Line(help_line.get_end_point(), end)

    def corner_divide_line(self):
        hip_height = self.get_hip_line().get_start_point()[1] - self.get_front_waist_line().get_start_point()[1]
        y_level = self.y_pos + hip_height*0.5

        line_wide = self.m["OS"]
        x_start, x_end = self._middle_vertical_line(self.x_pos, line_wide)

        return base.Line((x_start, y_level), (x_end, y_level))

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
        w_line = self.get_front_waist_line()
        wb_line = self.get_back_waist_line()
        k_line = self.get_knee_line()
        ca_line = self.get_calf_line()
        a_line = self.get_ankle_line()
        g_line = self.get_ground_line()
        fr_line = self.get_front_line()
        fsr_line = self.get_front_side_right(1)
        fsl_line = self.get_front_side_right(2)
        rw_line = self.get_right_wide()
        cor_sl = self.corner_slope()
        cr = self.crotch_back()
        up_cr = self.upper_crotch()
        sl_w = self.slope_wide()
        div = self.corner_divide_line()



        # Return them organized by name
        return {
            "hip": h_line,
            "waist": w_line,
            "waist_b": wb_line,
            "center": c_line,
            "knee": k_line,
            "calf": ca_line,
            "ankle": a_line,
            "ground": g_line,
            "front": fr_line,
            "side_right": fsr_line,
            "side_left": fsl_line,
            "side_wide": rw_line,
            "cor_slope": cor_sl,
            "crotch": cr,
            "upper_crotch": up_cr,
            "slope_wide": sl_w,
            "divide": div
        }
