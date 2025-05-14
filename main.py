import math

import output.create_pdf as pdf
import geometry.skeleton as skel
from geometry.base import CatmullRomSpline, Bezier
# === PDF Export ===
# === Pattern Generation ===
import json
from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as paper
from reportlab.lib.units import mm
import matplotlib.pyplot as plt

# Use reportlab.lib.units for real-world sizing
# Group curves and segments into “pattern pieces” for layout
# Add a simple GUI later with Tkinter, PyQt, or Streamlit
# Save a DXF/SVG version using libraries like ezdxf or svgwrite for digital cutters

# === Measurements ===
MEASUREMENTS = {
    "bust": 100,
    "waist": 70,
    "hip": 94,
    "height": 165
}
# === Utility Functions ===

# def generate_bodice_front(c):
#     """Draw a very simple bodice front pattern"""
#     start_x = mm_to_pt(20)
#     start_y = mm_to_pt(250)
#
#     bust = MEASUREMENTS["bust"] / 4 + 2  # Ease
#     waist = MEASUREMENTS["waist"] / 4 + 2
#     length = mm_to_pt(270 - 150)  # torso length
#
#     bust_width = mm_to_pt(bust)
#     waist_width = mm_to_pt(waist)
#
#     # Draw rectangle for bodice front (simplified)
#     c.setStrokeColorRGB(0, 0, 0)
#     c.setLineWidth(1)
#
#     # Bust line
#     c.line(start_x, start_y, start_x + bust_width, start_y)
#     # Waist line
#     c.line(start_x, start_y - length, start_x + waist_width, start_y - length)
#     # Side seam
#     c.line(start_x + bust_width, start_y, start_x + waist_width, start_y - length)
#     # Center front
#     c.line(start_x, start_y, start_x, start_y - length)
#
#     # Add text labels
#     c.setFont("Helvetica", 8)
#     c.drawString(start_x, start_y + mm_to_pt(5), "Bust Line")
#     c.drawString(start_x, start_y - length - mm_to_pt(5), "Waist Line")
#     c.drawString(start_x, start_y - length - mm_to_pt(15), "Front Bodice (simplified)")

# def export_pattern():
#     c = canvas.Canvas("bodice_front.pdf", pagesize=paper.A2)
#     generate_bodice_front(c)
#     c.showPage()
#     c.save()

# def add_text(c, x_pos, y_pos, text):
#     c.saveState()
#     c.translate(x_pos, y_pos)  # Move to desired position
#     c.scale(1, -1)  # Flip horizontally
#     c.drawString(0, 0, text)
#     c.restoreState()

def gener(file, OH, OP, DZ, Szad):
    # file = "test_outputs/test01.pdf"
    p = pdf.MakePdf(file, landscape=False)

    # OH = 100
    # OP = 80
    # DZ = 40
    # Szad = 42
    m = skel.Measurements()
    m.add_chest(OH)
    m.add_waist(OP)
    m.add_back_length(DZ)
    m.add_back_width(Szad)
    print(m.get_all_measurements(1, "mm"))

    position_x = 3
    position_y = 8

    # back part pattern

    sk = skel.BackPattern(position_x, position_y, m)
    collar = sk.generate_collar(12)

    lines = sk.get_skeleton_lines()

    p.add_lines(lines.values())


    points = sk.get_contour()
    p.add_curve_by_points(points, closed=False)

    p.add_mark(sk.get_armhole_edges()[0], 5)
    p.add_mark(sk.get_armhole_edges()[1], 5)
    p.add_curve_by_points(sk.get_pattern_points(collar=True, bezier_contour=False), line_width=3, closed=False)

    # collar part pattern
    # collar1 = skel.CollarPattern(position_x, position_y, m)


    # collar = sk.generate_collar()

    p.add_curve_by_points(collar.get_pattern_points(), line_width=3)

    x_text = (lines["chest"].get_end_point()[0] - lines["chest"].get_start_point()[0])*0.35 + lines["chest"].get_start_point()[0]
    y_text = lines["chest"].get_start_point()[1] + 20
    text = ("ZADNÍ DÍL\n"
            "\n"
            "TEST PATTERN\n"
            f"OH {OH}\n"
            f"OP {OP}\n"
            f"DZ {DZ}")
    p.add_text(x_text, y_text, text, font_size=16)

    # p.save_pdf()
    p.save_png()

    return file

# create directly pdf
if __name__ == "__main__":
    OH = 100
    OP = 80
    DZ = 40
    Szad = 42
    file = "test_outputs/test01.pdf"

    gener(file, OH, OP, DZ, Szad)
    print("FILE GENERATED")
