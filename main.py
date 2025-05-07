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

def generate_bodice_front(c):
    """Draw a very simple bodice front pattern"""
    start_x = mm_to_pt(20)
    start_y = mm_to_pt(250)

    bust = MEASUREMENTS["bust"] / 4 + 2  # Ease
    waist = MEASUREMENTS["waist"] / 4 + 2
    length = mm_to_pt(270 - 150)  # torso length

    bust_width = mm_to_pt(bust)
    waist_width = mm_to_pt(waist)

    # Draw rectangle for bodice front (simplified)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)

    # Bust line
    c.line(start_x, start_y, start_x + bust_width, start_y)
    # Waist line
    c.line(start_x, start_y - length, start_x + waist_width, start_y - length)
    # Side seam
    c.line(start_x + bust_width, start_y, start_x + waist_width, start_y - length)
    # Center front
    c.line(start_x, start_y, start_x, start_y - length)

    # Add text labels
    c.setFont("Helvetica", 8)
    c.drawString(start_x, start_y + mm_to_pt(5), "Bust Line")
    c.drawString(start_x, start_y - length - mm_to_pt(5), "Waist Line")
    c.drawString(start_x, start_y - length - mm_to_pt(15), "Front Bodice (simplified)")

def export_pattern():
    c = canvas.Canvas("bodice_front.pdf", pagesize=paper.A2)
    generate_bodice_front(c)
    c.showPage()
    c.save()

# def add_text(c, x_pos, y_pos, text):
#     c.saveState()
#     c.translate(x_pos, y_pos)  # Move to desired position
#     c.scale(1, -1)  # Flip horizontally
#     c.drawString(0, 0, text)
#     c.restoreState()

def gener(file, OH, OP, DZ, Szad):
    # file = "test_outputs/test01.pdf"
    p = pdf.MakePdf(file, "A2", False)

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
    position_y = 3
    sk = skel.BackContour(position_x, position_y, m)
    lines = sk.get_skeleton_lines()

    # print(list(lines.values()))
    # print(list(lines.keys()))
    # print(len(list(lines.values())))
    # c.lines(lines.values())
    p.add_lines(lines.values())

    for k in lines.keys():
        orig = lines[k].get_start_point()
        end = lines[k].get_end_point()
        print(f"{k}: origin: {orig}, end: {end}")
    # p.add_line(orig, end)
    #
    # orig = lines["back"].get_start_point()
    # end = lines["back"].get_end_point()
    # print(f"BACK: origin: {orig}, end: {end}")

    points = sk.get_contour()
    print(points)
    p.add_curve_by_points(points)

    p.add_text(position_x, lines["side"].get_start_point()[1] + 5, "Test pattern from Python")

    p.add_mark(sk.get_armhole_edges()[0], 5)
    p.add_mark(sk.get_armhole_edges()[1], 5)

    # p.add_bezier(points[1][0], points[1][1], points[2][0], points[2][1], points[3][0], points[3][1], points[3][0],
    #              points[3][1])
    # neck_width = math.fabs(points[3][0] - points[2][0])
    # print(f"neck_width: {neck_width}")
    # c = [points[1], (points[3][0] + neck_width*(5.0/6), points[2][1]), points[3]]
    # print(f"c: {c}")
    # b1 = CatmullRomSpline(c)
    # b2 = Bezier(c)
    # n = 50
    # p_cat = b1.sample(n)
    # p_bez = b2.sample(n)
    # p.add_curve_by_points(p_cat)
    # p.add_curve_by_points(p_bez)
    #
    # plot = True
    # # print(po)
    #
    # # print(b1.get_point(1))
    #
    # if plot:
    #     # n = 100
    #
    #     xb1 = []
    #     yb1 = []
    #     xb2 = []
    #     yb2 = []
    #     xc = []
    #     yc = []
    #     po = p_cat
    #     for i in po:
    #         xb1.append(i[0])
    #         yb1.append(i[1])
    #
    #     po = p_bez
    #     for i in po:
    #         xb2.append(i[0])
    #         yb2.append(i[1])
    #
    #     for k in c:
    #         xc.append(k[0])
    #         yc.append(k[1])
    #
    #     print(po)
    #
    #     plt.plot(xc, yc)
    #     plt.plot(xb1, yb1)
    #     plt.plot(xb2, yb2)
    #     plt.show()

    p.save_pdf()

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
