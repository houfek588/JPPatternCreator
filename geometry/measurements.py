from reportlab.lib.units import cm
import json

class ValidationError(ValueError):
    """Exception raised for invalid measurements."""
    pass

class Measurements:
    def __init__(self, meas: dict = None):
        if meas:
            self.meas = meas
            self.validate()
        else:
            self.meas = {}

    def add_chest(self, value):
        self.meas.update({"OH": float(value)})

    def add_waist(self, value):
        self.meas.update({"OP": float(value)})

    def add_back_length(self, value):
        self.meas.update({"DZ": float(value)})

    def add_back_width(self, value):
        self.meas.update({"Szad": float(value)})

    def validate(self):
        """Validates upper body measurements."""
        required_keys = ["OH", "OP", "DZ", "Szad"]
        for key in required_keys:
            if key not in self.meas or self.meas[key] is None:
                raise ValidationError(f"Missing required measurement: {key}")
            try:
                val = float(self.meas[key])
                if val <= 0:
                    raise ValidationError(f"Measurement {key} must be positive, got {val}")
                self.meas[key] = val
            except (ValueError, TypeError):
                raise ValidationError(f"Measurement {key} must be a number, got {self.meas[key]}")

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
            "in": 1 / 2.54,  # 1 cm = 1/2.54 inches
            "pt": cm  # ReportLab point (1 pt = 1/72 inch = 0.3528 mm)
        }

        if unit not in unit_map:
            raise ValueError(f"Unsupported unit '{unit}'. Choose from: {list(unit_map.keys())}")

        conversion_factor = unit_map[unit]

        # Optional: return a new dictionary instead of modifying in place
        scaled_meas = {key: val * scale * conversion_factor for key, val in self.meas.items()}

        return scaled_meas

    def save_to_json(self, filename):
        print(f"self.meas: {self.meas}")
        data = json.dumps(self.meas, indent=4)
        with open(filename, "w") as f:
            f.write(data)
        print(f"measurements saved to: {filename}")

    def load_from_json(self, filename):
        with open(filename, "r") as f:
            data = f.read()
        self.meas = json.loads(data)
        self.validate()
        print(f"measurements load from: {filename}")

    def __str__(self):
        text = "Measured parameters:\n"
        for key in self.meas.keys():
            text_line = f"parameter {key}: value {self.meas[key]}"
            text = text + text_line + "\n"

        return text

class LowerMeasurements:
    def __init__(self, meas: dict = None):
        if meas:
            self.meas = meas
            self.validate()
        else:
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

    def validate(self):
        """Validates lower body measurements."""
        if "title" not in self.meas or not isinstance(self.meas["title"], str) or not self.meas["title"].strip():
            self.meas["title"] = "Sample Pattern"

        required_keys = ["VP", "OP", "OS", "BDK", "KD", "O_st", "O_nk", "O_l", "O_kot"]
        for key in required_keys:
            if key not in self.meas or self.meas[key] is None:
                raise ValidationError(f"Missing required measurement: {key}")
            try:
                val = float(self.meas[key])
                if val <= 0:
                    raise ValidationError(f"Measurement {key} must be positive, got {val}")
                self.meas[key] = val
            except (ValueError, TypeError):
                raise ValidationError(f"Measurement {key} must be a number, got {self.meas[key]}")

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
            "in": 1 / 2.54,  # 1 cm = 1/2.54 inches
            "pt": cm  # ReportLab point (1 pt = 1/72 inch = 0.3528 mm)
        }

        if unit not in unit_map:
            raise ValueError(f"Unsupported unit '{unit}'. Choose from: {list(unit_map.keys())}")

        conversion_factor = unit_map[unit]

        # Optional: return a new dictionary instead of modifying in place
        scaled_meas = {}
        for key, val in self.meas.items():
            if val:
                scaled_meas[key] = val * scale * conversion_factor

        # scaled_meas = {key: val * scale * conversion_factor for key, val in self.meas.items()}

        return scaled_meas

    def save_to_json(self, filename):
        # unpacked_lines = {}
        # for l in self.lines.keys():
        #     unpacked_lines[l] = self._unpack(self.lines[l])
        # print(unpacked_lines)
        print(f"self.meas: {self.meas}")
        data = json.dumps(self.meas, indent=4)
        with open(filename, "w") as f:
            f.write(data)

        print(f"measurements saved to: {filename}")

    def load_from_json(self, filename):
        with open(filename, "r") as f:
            data = f.read()

        self.meas = json.loads(data)
        self.validate()
        print(f"measurements load from: {filename}")

    def __str__(self):
        text = "Measured parameters:\n"
        for key in self.meas.keys():
            text_line = f"parameter {key}: value {self.meas[key]}"
            text = text + text_line + "\n"

        return text
