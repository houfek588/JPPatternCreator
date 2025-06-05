from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as paper
from typing import List, Tuple
from data.manage import cm_to_pt
import colordict
from pdf2image import convert_from_path
import os


class MakePdf:
    def __init__(self, file_name: str, paper_size=paper.A2, landscape: bool = False):
        """
                Initialize the PDF canvas and set coordinate system to top-left origin.
                """
        self.file_name = file_name
        self.canvas = canvas.Canvas(file_name, pagesize=paper_size)

        # Move origin to top-left corner and flip Y-axis downwards
        width, height = paper_size
        self.canvas.translate(cm_to_pt(1), height - cm_to_pt(1))  # Add 1 cm top/left margin
        self.canvas.scale(1, -1)

    def _set_stroke(self, color: str, line_width: float):
        """
               Helper to set stroke color and line width.
               """
        rgb = colordict.ColorDict(norm=1)[color]
        self.canvas.setStrokeColorRGB(*rgb)
        self.canvas.setLineWidth(line_width)

    def add_mark(self, pos: Tuple[float, float], radius: float, color: str = "black", line_width: int = 1):
        """
                Draw a circular mark at a given position.
                """
        self._set_stroke(color, line_width)
        self.canvas.circle(pos[0], pos[1], radius, stroke=1, fill=1)

    def add_curve_by_points(self, points: List[Tuple[float, float]], color: str = "black", line_width: int = 1, closed: bool = False):
        """
                Draw a polyline through a list of points.
                """
        self._set_stroke(color, line_width)
        for i in range(len(points) - 1):
            self.canvas.line(*points[i], *points[i + 1])
        if closed:
            self.canvas.line(*points[-1], *points[0])

        # self.c.line(points[1][0], points[1][1], points[3][0], points[3][1] + cm_to_pt(12))

    def add_line(self, start: Tuple[float, float], end: Tuple[float, float], color: str = "black", line_width: int = 1):
        """
                Draw a single line from start to end.
                """
        self._set_stroke(color, line_width)
        self.canvas.line(*start, *end)

    def add_lines(self, lines: List, color: str = "black", line_width: int = 1):
        """
                Draw multiple lines from line objects with get_start_point() and get_end_point().
                """
        self._set_stroke(color, line_width)
        draw_lines = [
            [*line.get_start_point(), *line.get_end_point()]
            for line in lines
        ]
        self.canvas.lines(draw_lines)

    def add_bezier(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
                Draw a cubic Bézier curve with four control points.
                """
        self.canvas.bezier(x1, y1, x2, y2, x3, y3, x4, y4)

    def add_text(self, x: float, y: float, text: str, font_size: int = 11, align: str = "center", leading=None):
        """
                Draw text at the given position, flipped upright.
                """
        # self.canvas.setFont("Helvetica", font_size)
        self.canvas.saveState()
        self.canvas.translate(x, y)
        self.canvas.scale(1, -1)  # Flip text upright

        text_object = self.canvas.beginText()
        text_object.setFont("Helvetica", font_size)
        text_object.setTextOrigin(0, 0)

        if leading:
            text_object.setLeading(leading)

        for line in text.split("\n"):
            # print(line)
            text_object.textLine(line)

        # self.canvas.drawString(0, 0, text)
        self.canvas.drawText(text_object)
        self.canvas.restoreState()

    def save_pdf(self):
        """
                Finalize and save the PDF.
                """
        self.canvas.showPage()
        self.canvas.save()
        print(f"PDF saved to: {self.file_name}")

    def save_png(self):
        """
                Save the PDF and convert its first page to a PNG.
                """
        self.save_pdf()
        images = convert_from_path(self.file_name, dpi=300)

        base_name, _ = os.path.splitext(self.file_name)
        png_name = f"{base_name}.png"

        images[0].save(png_name, "PNG")
        print(f"PNG saved to: {png_name}")










