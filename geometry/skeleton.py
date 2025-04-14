from reportlab.lib.units import mm, cm
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
        return [origin[0], origin[1], end[0], end[1]]

    def get_waist_line(self):
        """Returns a horizontal waist guideline defined by origin and end point coordinates."""

        # Calculate the vertical position of the waistline
        y_waist = self.m["DZ"] + self.y_pos

        # Calculate the start and end x-positions
        x_start = self.x_pos
        x_end = x_start + (1.2 * self.m["OH"] / 4)  # 1.2 * quarter of outer height

        # Return as a flat list: [x1, y1, x2, y2]
        return [x_start, y_waist, x_end, y_waist]

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
        return [x_start, y_chest, x_end, y_chest]

    def get_armhole_line(self):
        """Returns a horizontal armhole guideline as a flat list of coordinates: [x1, y1, x2, y2]."""

        # Calculate vertical Y position for the armhole line
        y_armhole = (self.m["DZ"] / 3) + (self.m["DZ"] / 8) + self.y_pos

        # Define horizontal start and end X positions
        x_start = self.x_pos
        x_end = x_start + (1.2 * self.m["OH"] / 4)  # Adjusted line width

        # Return line coordinates as a flat list
        return [x_start, y_armhole, x_end, y_armhole]

    def get_neck_line(self):
        """Returns a horizontal neckline guideline as a flat list of coordinates: [x1, y1, x2, y2]."""

        y_neck = self.y_pos
        x_start = self.x_pos
        x_end = x_start + (1.2 * self.m["OH"] / 4)  # Line width based on opening height (OH)

        return [x_start, y_neck, x_end, y_neck]

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
        y_top = armhole_line[3]  # end y of armhole line
        y_bottom = waist_line[3]  # end y of waist line

        return [x, y_top, x, y_bottom]

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
        y_top = neck_line[3]  # end y of neck line
        y_bottom = armhole_line[3]  # end y of armhole line

        return [x, y_bottom, x, y_top]

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
        print(f"sk: {sk}")

        points = []

        points.append((sk["back"][0], sk["neck"][1]))
        points.append((sk["neck"][0] + self.m["OH"] / 12, sk["neck"][1] - offset3cm))
        points.append((sk["neck"][0] + self.m["OH"] / 12, sk["neck"][1]))
        points.append((sk["neck"][0],sk["neck"][1]))
        points.append((sk["chest"][0], sk["chest"][1]))
        points.append((sk["waist"][0] + offset2cm, sk["waist"][1]))
        points.append((sk["waist"][0] + offset2cm + self.m["OP"] / 4 - offset1cm, sk["waist"][1] + offset1cm))
        points.append((sk["side"][0], sk["chest"][1]))
        points.append((sk["side"][0] + offset1cm, sk["armhole"][1]))


        print(f"points: {points}")

        return points
