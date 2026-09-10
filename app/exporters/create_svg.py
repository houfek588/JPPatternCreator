from typing import List, Tuple

class SVGCreator:
    def __init__(self, width=500, height=500):
        self.width = width
        self.height = height
        self.elements = []

    def add_line(self, start: Tuple[float, float], end: Tuple[float, float], color: str = "black", line_width: int = 1):
        """Draw a single line element in SVG."""
        x1, y1 = start
        x2, y2 = end
        element = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:{color};stroke-width:{line_width}" />'
        self.elements.append(element)

    def add_lines(self, lines: List, color: str = "black", line_width: int = 1):
        """Draw multiple lines from geometric Line objects."""
        for line in lines:
            self.add_line(line.get_start_point(), line.get_end_point(), color=color, line_width=line_width)

    def add_curve(self, points):
        """Draw a cubic Bezier curve with 4 control points."""
        if len(points) != 4:
            raise ValueError("Cubic Bezier requires exactly 4 control points")
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = points
        path_data = f"M{x0},{y0} C{x1},{y1} {x2},{y2} {x3},{y3}"
        element = f'<path d="{path_data}" style="fill:none;stroke:red;stroke-width:2" />'
        self.elements.append(element)

    def add_curve_by_points(self, points, color: str = "red", line_width: int = 2):
        """Draw a polyline path through a series of points."""
        if not points:
            return
        path_data = f"M{points[0][0]},{points[0][1]} " + " ".join(f"L{x},{y}" for x, y in points[1:])
        element = f'<path d="{path_data}" style="fill:none;stroke:{color};stroke-width:{line_width}" />'
        self.elements.append(element)

    def add_text(self, position, text):
        """Add text element to SVG."""
        x, y = position
        element = f'<text x="{x}" y="{y}" fill="black" text-anchor="middle">{text}</text>'
        self.elements.append(element)

    def save(self, filename="output.svg"):
        """Save the SVG content to a file."""
        svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">'
        svg_content = "\n  ".join(self.elements)
        svg_footer = "</svg>"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{svg_header}\n  {svg_content}\n{svg_footer}")

    def to_string(self):
        """Return the SVG content as an XML string."""
        svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">'
        svg_content = "\n  ".join(self.elements)
        svg_footer = "</svg>"
        return f"{svg_header}\n  {svg_content}\n{svg_footer}"
