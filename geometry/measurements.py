from reportlab.lib.units import cm

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
