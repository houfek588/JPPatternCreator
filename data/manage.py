import json
from typing import Optional, Dict, List
import geometry.base as base
from reportlab.lib.units import mm, cm


class SaveLinesToJson():
    def __init__(self, lines: List):
        self.lines = lines
        print(self.lines)

    def _unpack(self, single_line):
        # print(single_line)
        dict = {"start": single_line.get_start_point(),
                "end": single_line.get_end_point()}
        # return (single_line.get_start_point(), single_line.get_end_point())
        return dict

    def save(self, filename):
        unpacked_lines = {}
        for l in self.lines.keys():
            unpacked_lines[l] = self._unpack(self.lines[l])
        print(unpacked_lines)
        data = json.dumps(unpacked_lines, indent=4)
        with open(filename, "w") as f:
            f.write(data)


class LoadLinesFromJson():
    def __init__(self, filename):
        with open(filename, "r") as f:
            data = f.read()

        self.lines = json.loads(data)

    def _read_json_line(self, line):
        line_points = []
        for key in line:
            # print(line[key])
            line_points.append(tuple(line[key]))
        return tuple(line_points)

    def get_list_points(self):
        list_points = []
        for key in self.lines:
            list_points.append(self._read_json_line(self.lines[key]))
        return list_points

    def get_lines(self):
        list_points = self.get_list_points()

        lines = {}
        for i, key in enumerate(self.lines):
            lines[key] = base.Line(list_points[i][0], list_points[i][1])
        return lines

        # return base.Line(normal.get_start_point(), (end, div_y))


class TextLine():
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def get_text(self, position_scale: float = 1):
        return (self.x * position_scale, self.y * position_scale, self.text)


def mm_to_pt(val):
    return val * mm


def cm_to_pt(val):
    return val * cm


def pt_to_cm(val):
    return val/cm

def scale_line(line: base.Line, scale):
    start, end = line.get_edge_points()

    new_start = (start[0] * scale, start[1] * scale)
    new_end = (end[0] * scale, end[1] * scale)
    return base.Line(new_start, new_end)

def scale_lines(lines, scale):
    scaled = {}
    for key in lines.keys():
        scaled[key] = scale_line(lines[key], scale)

    return scaled

def scale_points(point_list, scale):
    new = []
    for point in point_list:
        x, y = point
        new.append((x*scale, y*scale))

    return new

def scale_one_point(point, scale):
    x, y = point
    return (x*scale, y*scale)
