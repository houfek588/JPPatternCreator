import math

import output.create_pdf as pdf
import geometry.skeleton as skel
import geometry.hosen as hosen
import output.create_svg as svg
import data.manage as mn
import output.gen_hosen_files as file_gen
from reportlab.lib.units import mm, cm
import interface.server as srv

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

def gen_back_body():
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

    x_text = (lines["chest"].get_end_point()[0] - lines["chest"].get_start_point()[0]) * 0.35 + \
             lines["chest"].get_start_point()[0]
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


def gen_hosen():
    file_gen.gen_hosen_svg_string()
    file_gen.save_hosen_to_pdf("test_outputs/test03.pdf")
    # s.save("test_outputs/svg_test03.svg")


def gener(file, OH, OP, DZ, Szad):

    # gen_back_body()
    gen_hosen()

    return file

# create directly pdf
if __name__ == "__main__":


    # gener(file, OH, OP, DZ, Szad)
    print("starting server...")
    srv.start_server()