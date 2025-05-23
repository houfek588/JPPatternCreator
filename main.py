import math

import output.create_pdf as pdf
import geometry.skeleton as skel
import geometry.hosen as hosen
import output.create_svg as svg
import data.manage as mn

from reportlab.lib.units import mm, cm
import reportlab.lib.pagesizes as paper
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
    my_paper = (skel.cm_to_pt(120), skel.cm_to_pt(140))
    p = pdf.MakePdf("test_outputs/test03.pdf", landscape=False, paper_size=my_paper)
    s = svg.SVGCreator(120, 140)
    print(f"my_paper: {my_paper}")
    # print(paper.A1)
    # print(skel.pt_to_cm(paper.A1[0]))
    # print(skel.pt_to_cm(paper.A1[1]))

    OS = 116
    OP = 98
    BDK = 122
    KD = 90
    O_st = 61
    O_nk = 46
    O_l = 40
    O_kot = 26


    m = hosen.LowerMeasurements()
    m.add_waist(OP)
    m.add_hips(OS)
    m.add_side_hose_length(BDK)
    m.add_step_length(KD)
    m.add_circumference_thigh(O_st)
    m.add_circumference_above_knee(O_nk)
    m.add_circumference_calf(O_l)
    m.add_circumference_ankle(O_kot)
    print(m.get_all_measurements(1, "cm"))

    # position_x = 30
    # position_y = 8
    position_x = 120 * 0.5
    position_y = 8

    # back part pattern
    sk = hosen.HosenPattern(position_x, position_y, m)


    lines = sk.get_skeleton_lines()
    points = sk.get_pattern_points()
    new = mn.scale_lines(lines, cm)

    p.add_lines(new.values())
    p.add_curve_by_points(mn.scale_points(points, cm), line_width=3)
    s.add_lines(lines.values())

    x_text = (new["hip"].get_end_point()[0] - new["hip"].get_start_point()[0]) * 0.35 + \
             new["hip"].get_start_point()[0]
    y_text = new["hip"].get_start_point()[1] + 20
    text = ("HOSEN\n"
            "\n"
            "TEST PATTERN\n"
            f"OP {OP}\n"
            f"OS {OS}\n"
            f"BDK {BDK}\n"
            f"KD {KD}\n"
            f"Ost {O_st}")
    p.add_text(x_text, y_text, text, font_size=32)

    p.save_pdf()
    s.save("test_outputs/svg_test03.svg")

    js = mn.SaveLinesToJson(lines)
    js.save("test_outputs/json_test03.json")

    # load = mn.LoadLinesFromJson("test_outputs/json_test03.json")
    # # print(load.get_lines())
    # print(f"hip line: {lines['hip'].get_edge_points()}")
    # print(f"new line: {new['hip'].get_edge_points()}")


def gener(file, OH, OP, DZ, Szad):
    # # file = "test_outputs/test01.pdf"
    # p = pdf.MakePdf(file, landscape=False)
    #
    # # OH = 100
    # # OP = 80
    # # DZ = 40
    # # Szad = 42
    # m = skel.Measurements()
    # m.add_chest(OH)
    # m.add_waist(OP)
    # m.add_back_length(DZ)
    # m.add_back_width(Szad)
    # print(m.get_all_measurements(1, "mm"))
    #
    # position_x = 3
    # position_y = 8
    #
    # # back part pattern
    #
    # sk = skel.BackPattern(position_x, position_y, m)
    # collar = sk.generate_collar(12)
    #
    # lines = sk.get_skeleton_lines()
    #
    # p.add_lines(lines.values())
    #
    #
    # points = sk.get_contour()
    # p.add_curve_by_points(points, closed=False)
    #
    # p.add_mark(sk.get_armhole_edges()[0], 5)
    # p.add_mark(sk.get_armhole_edges()[1], 5)
    # p.add_curve_by_points(sk.get_pattern_points(collar=True, bezier_contour=False), line_width=3, closed=False)
    #
    # # collar part pattern
    # # collar1 = skel.CollarPattern(position_x, position_y, m)
    #
    #
    # # collar = sk.generate_collar()
    #
    # p.add_curve_by_points(collar.get_pattern_points(), line_width=3)
    #
    # x_text = (lines["chest"].get_end_point()[0] - lines["chest"].get_start_point()[0])*0.35 + lines["chest"].get_start_point()[0]
    # y_text = lines["chest"].get_start_point()[1] + 20
    # text = ("ZADNÍ DÍL\n"
    #         "\n"
    #         "TEST PATTERN\n"
    #         f"OH {OH}\n"
    #         f"OP {OP}\n"
    #         f"DZ {DZ}")
    # p.add_text(x_text, y_text, text, font_size=16)
    #
    # # p.save_pdf()
    # p.save_png()



    # gen_back_body()
    gen_hosen()
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
