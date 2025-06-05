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


def gen_hosen_svg_string(a, b, c, d):
    my_paper = (120, 160)

    svg_scale = 4
    s = svg.SVGCreator(my_paper[0] * svg_scale, my_paper[1] * svg_scale)

    m = hosen.LowerMeasurements()
    m.load_from_json("server_data/meas_test01.json")
    # m.save_to_json("meas_test01.json")

    position_x = 120 * 0.5
    position_y = 8

    # back part pattern
    sk = hosen.HosenPattern(position_x, position_y, m)
    sk_par = hosen.HosenPatternParameter(a, b, c, d)

    lines = sk.get_skeleton_lines()
    points = sk.get_pattern_points(sk_par)

    s.add_lines(mn.scale_lines(lines, svg_scale).values())
    s.add_curve_by_points(mn.scale_points(points, svg_scale))

    return s.to_string()

    # load = mn.LoadLinesFromJson("test_outputs/json_test03.json")
    # # print(load.get_lines())
    # print(f"hip line: {lines['hip'].get_edge_points()}")
    # print(f"new line: {new['hip'].get_edge_points()}")

def save_hosen_to_pdf(a, b, c, d):
    my_paper = (120, 160)
    p = pdf.MakePdf("server_data/server_test03.pdf", landscape=False, paper_size=mn.scale_one_point(my_paper, cm))

    m = hosen.LowerMeasurements()
    m.load_from_json("server_data/meas_test01.json")
    m.save_to_json("server_data/meas_test01.json")

    position_x = my_paper[0] * 0.5
    position_y = 8

    # back part pattern
    sk = hosen.HosenPattern(position_x, position_y, m)
    sk_par = hosen.HosenPatternParameter(a, b, c, d)

    lines = sk.get_skeleton_lines()
    points = sk.get_pattern_points(sk_par)
    new = mn.scale_lines(lines, cm)
    new_points = mn.scale_points(points, cm)

    p.add_lines(new.values())
    p.add_curve_by_points(new_points, line_width=3)


    main_description = sk.get_main_description()
    x, y, text = main_description.get_text(cm)
    p.add_text(x, y, text, font_size=32)

    line_descriptions = sk.get_lines_description()
    for d in line_descriptions:
        x, y, text = d.get_text(cm)
        p.add_text(x, y, text, font_size=26)

    marks = sk.get_important_points()
    for m in marks:
        p.add_mark(mn.scale_one_point(m, cm), 15)

    p.save_pdf()

    js = mn.SaveLinesToJson(lines)
    js.save("server_data/json_test03.json")


def gen_hosen():
    my_paper = (120, 160)
    p = pdf.MakePdf("test_outputs/test03.pdf", landscape=False, paper_size=mn.scale_one_point(my_paper,cm))

    svg_scale = 10
    s = svg.SVGCreator(my_paper[0] * svg_scale, my_paper[1] * svg_scale)
    print(f"my_paper: {my_paper}")
    # print(paper.A1)
    # print(skel.pt_to_cm(paper.A1[0]))
    # print(skel.pt_to_cm(paper.A1[1]))



    m = hosen.LowerMeasurements()


    m.load_from_json("meas_test01.json")

    print("GET ALL MEASUREMENTS")
    print(m.get_all_measurements(1, "cm"))
    m.save_to_json("meas_test01.json")

    # position_x = 30
    # position_y = 8
    position_x = 120 * 0.5
    position_y = 8

    # back part pattern
    sk = hosen.HosenPattern(position_x, position_y, m)
    sk_par = hosen.HosenPatternParameter()

    lines = sk.get_skeleton_lines()
    points = sk.get_pattern_points(sk_par)
    new = mn.scale_lines(lines, cm)
    new_points = mn.scale_points(points, cm)

    p.add_lines(new.values())
    p.add_curve_by_points(new_points, line_width=3)
    s.add_lines(mn.scale_lines(lines, svg_scale).values())
    s.add_curve_by_points(mn.scale_points(points, svg_scale))


    main_description = sk.get_main_description()
    x, y, text = main_description.get_text(cm)
    p.add_text(x, y, text, font_size=32)

    line_descriptions = sk.get_lines_description()
    for d in line_descriptions:
        # pos = mn.scale_one_point((d[0], d[1]), cm)
        x, y, text = d.get_text(cm)
        p.add_text(x, y, text, font_size=26)

    marks = sk.get_important_points()
    for m in marks:
        p.add_mark(mn.scale_one_point(m, cm), 15)

    p.save_pdf()

    s.save("test_outputs/svg_test03.svg")

    js = mn.SaveLinesToJson(lines)
    js.save("test_outputs/json_test03.json")

    # load = mn.LoadLinesFromJson("test_outputs/json_test03.json")
    # # print(load.get_lines())
    # print(f"hip line: {lines['hip'].get_edge_points()}")
    # print(f"new line: {new['hip'].get_edge_points()}")


def gener(file, OH, OP, DZ, Szad):

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
