from typing import List, Tuple

class SVGCreator:
    def __init__(self, width=500, height=500):
        self.width = width
        self.height = height
        self.elements = []

    def add_line(self, start: Tuple[float, float], end: Tuple[float, float], color: str = "black", line_width: int = 1):
        """
        Draws a single line from a list of exactly two (x, y) tuples: origin and end point.
        """
        # print(f"points: {points}")
        # if len(points) != 2:
        #     raise ValueError("add_line requires exactly two points: origin and end point")
        x1, y1 = start
        x2, y2 = end
        element = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:black;stroke-width:1" />'
        self.elements.append(element)

    def add_lines(self, lines: List, color: str = "black", line_width: int = 1):
        """
        Draws multiple lines. Each line is defined by exactly two (x, y) tuples in a list.
        """
        # print(f"lines: {lines}")
        for line in lines:
            self.add_line(line.get_start_point(), line.get_end_point())

    def add_curve(self, points):
        """
        Draws a smooth cubic Bezier curve from a list of (x, y) control points.
        Currently supports exactly 4 points for a single cubic Bezier.
        """
        if len(points) != 4:
            raise ValueError("Cubic Bezier requires exactly 4 control points")
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = points
        path_data = f"M{x0},{y0} C{x1},{y1} {x2},{y2} {x3},{y3}"
        element = f'<path d="{path_data}" style="fill:none;stroke:red;stroke-width:2" />'
        self.elements.append(element)

    def add_curve_by_points(self, points):
        """
        Draws a general smooth path connecting all points with straight segments.
        """
        if not points:
            return
        path_data = f"M{points[0][0]},{points[0][1]} " + " ".join(f"L{x},{y}" for x, y in points[1:])
        element = f'<path d="{path_data}" style="fill:none;stroke:red;stroke-width:2" />'
        self.elements.append(element)

    def add_text(self, position, text):
        x, y = position
        element = f'<text x="{x}" y="{y}" fill="black" text-anchor="middle">{text}</text>'
        self.elements.append(element)

    def save(self, filename="output.svg"):
        """
        Saves the SVG file with current elements.
        """
        svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">'
        svg_content = "\n  ".join(self.elements)
        svg_footer = "</svg>"
        with open(filename, "w") as f:
            f.write(f"{svg_header}\n  {svg_content}\n{svg_footer}")

    def to_string(self):
        """
        Returns the full SVG markup as a string.
        Useful for embedding in web pages.
        """
        svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">'
        svg_content = "\n  ".join(self.elements)
        svg_footer = "</svg>"
        return f"{svg_header}\n  {svg_content}\n{svg_footer}"