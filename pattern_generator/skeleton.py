
class Measurements:
    def __init__(self):
        self.meas = {}

    def add_chest(self, value):
        self.meas.update({"OH": value})

    def add_waist(self, value):
        self.meas.update({"OP": value})

    def add_back_length(self, value):
        self.meas.update({"DZ": value})

    def add_back_width(self, value):
        self.meas.update({"Szad": value})

    def get_all_measurements(self, scale: float = 1):
        if scale == 1:
            return self.meas
        else:
            for key in self.meas.keys():
                self.meas[key] = self.meas[key] * 10

            return self.meas

class BackSkeleton:
    def __init__(self, measurements:Measurements, scale: float):
        self.m = measurements.get_all_measurements(scale)
        OH = self.m["OH"]
        OP = self.m["OP"]
        DZ = self.m["DZ"]
        Szad = self.m["Szad"]

        self.polygon = [(0,0),
                        (0, DZ),
                        (OP/4, DZ),
                        (OH/4, DZ/2),
                        (Szad/2, DZ/2),
                        (Szad/2, 0)]

    def get_polygon(self, x_pos, y_pos):
        gl = []
        for p in self.polygon:
            gl.append((p[0]+x_pos, p[1]+y_pos))

        return gl

    def get_center_line(self, x_pos, y_pos):
        origin = (0 + x_pos, 0 + y_pos)
        end = (0 + x_pos, self.m["DZ"] + y_pos)
        return [origin, end]

    def get_waist_line(self, x_pos, y_pos):
        origin = (0 + x_pos, self.m["DZ"] + y_pos)
        end = ((1.2*self.m["OH"]/4) + x_pos, self.m["DZ"] + y_pos)
        return [origin, end]

    def get_chest_line(self, x_pos, y_pos):
        origin = (0 + x_pos, (self.m["DZ"]/2) + y_pos)
        end = ((1.2*self.m["OH"]/4) + x_pos, (self.m["DZ"]/2) + y_pos)
        return [origin, end]

    def get_neck_line(self, x_pos, y_pos):
        origin = (0 + x_pos, 0 + y_pos)
        end = ((1.2*self.m["OH"]/4) + x_pos, 0 + y_pos)
        return [origin, end]

    def get_side_line(self, x_pos, y_pos):
        chest_line = self.get_chest_line(x_pos, y_pos)
        waist_line = self.get_waist_line(x_pos, y_pos)

        origin = ((self.m["OH"]/4) + x_pos, chest_line[1][1])
        end = ((self.m["OH"]/4) + x_pos, waist_line[1][1])
        return [origin, end]

    def get_back_line(self, x_pos, y_pos):
        chest_line = self.get_chest_line(x_pos, y_pos)
        neck_line = self.get_neck_line(x_pos, y_pos)

        origin = ((self.m["Szad"] / 2) + x_pos, chest_line[1][1])
        end = ((self.m["Szad"] / 2) + x_pos, neck_line[1][1])
        return [origin, end]