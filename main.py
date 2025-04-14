import output.create_pdf as pdf
import  geometry.skeleton as skel
# === PDF Export ===
# === Pattern Generation ===
import json
from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as paper
from reportlab.lib.units import mm

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
    # for l in lines.keys():
    #     p.add_line(lines[l][0], lines[l][1])

    # p.add_mark(lines["center"][0], 5, line_width=5)
    # p.add_mark(lines["center"][1], 5, line_width=5)
    # # p.add_mark(60, 60, 5)
    # p.add_text(lines["side"][0][1]/2, lines["side"][0][1], "Test pattern from Python", 20)
    #
    # p.save_pdf("test_outputs/test01.pdf")

    # c = canvas.Canvas("test_outputs/test01.pdf", pagesize=paper.A2)
    #
    # # Move origin to top-left, flip Y so it goes down
    # width, height = paper.A2
    # c.translate(skel.mm_to_pt(10), height - skel.mm_to_pt(10))  # Top-left margin
    # c.scale(1, -1)

    # for l in lines.keys():
    #     # p.add_line(lines[l][0], lines[l][1])
    #     c.line(lines[l][0][0], lines[l][0][1], lines[l][1][0], lines[l][1][1])
    print(list(lines.values()))
    # c.lines(lines.values())
    p.add_lines(lines.values())

    points = sk.get_contour()
    p.add_curve_by_points(points)

    p.add_text(position_x, lines["side"][1] + 5, "Test pattern from Python")

    p.add_bezier(points[1][0], points[1][1], points[2][0], points[2][1], points[3][0], points[3][1], points[3][0],
                 points[3][1])

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
    # export_pattern()
    # pdf.basic_pdf("test_outputs/test01.pdf")
    # p = pdf.MakePdf("test_outputs/test01.pdf", "A2", False)
    #
    #
    #
    #
    # OH = 100
    # OP = 80
    # DZ = 40
    # Szad = 42
    # m = skel.Measurements()
    # m.add_chest(OH)
    # m.add_waist(OP)
    # m.add_back_length(DZ)
    # m.add_back_width(Szad)
    # print(m.get_all_measurements(1, "mm"))
    #
    # position_x = 3
    # position_y = 3
    # sk = skel.BackContour(position_x, position_y, m)
    # lines = sk.get_skeleton_lines()
    # # for l in lines.keys():
    # #     p.add_line(lines[l][0], lines[l][1])
    #
    #
    # # p.add_mark(lines["center"][0], 5, line_width=5)
    # # p.add_mark(lines["center"][1], 5, line_width=5)
    # # # p.add_mark(60, 60, 5)
    # # p.add_text(lines["side"][0][1]/2, lines["side"][0][1], "Test pattern from Python", 20)
    # #
    # # p.save_pdf("test_outputs/test01.pdf")
    #
    # # c = canvas.Canvas("test_outputs/test01.pdf", pagesize=paper.A2)
    # #
    # # # Move origin to top-left, flip Y so it goes down
    # # width, height = paper.A2
    # # c.translate(skel.mm_to_pt(10), height - skel.mm_to_pt(10))  # Top-left margin
    # # c.scale(1, -1)
    #
    #
    # # for l in lines.keys():
    # #     # p.add_line(lines[l][0], lines[l][1])
    # #     c.line(lines[l][0][0], lines[l][0][1], lines[l][1][0], lines[l][1][1])
    # print(list(lines.values()))
    # # c.lines(lines.values())
    # p.add_lines(lines.values())
    #
    # points = sk.get_contour()
    # p.add_curve_by_points(points)
    #
    # p.add_text(position_x, lines["side"][1] + 5, "Test pattern from Python")
    #
    # p.add_bezier(points[1][0],points[1][1], points[2][0],points[2][1], points[3][0],points[3][1], points[3][0],points[3][1])
    #
    # p.save_pdf()

    # points = sk.get_contour()
    # c.setLineWidth(2)
    # for i in range(len(points) - 1):
    #     x1, y1 = points[i]
    #     x2, y2 = points[i + 1]
    #     c.line(x1, y1, x2, y2)
    # c.line(points[1][0],points[1][1], points[3][0], points[3][1] + skel.cm_to_pt(12))



    # c.cross(points[0][0],points[0][1], skel.cm_to_pt(2))
    #
    # c.setFont("Helvetica", 20)
    # c.restoreState()
    # c.saveState()
    # c.translate(lines["side"][0][1]/2, lines["side"][0][1])  # Move to desired position
    # c.scale(1, -1)        # Flip horizontally
    # # c.drawString(lines["side"][0][1]/2, lines["side"][0][1], "Test pattern from Python")
    # c.drawString(0, 0, "Mirrored Text")
    # c.restoreState()

    # add_text(c, position_x, lines["side"][1] + 5, "Test pattern from Python")
    #
    # # generate_bodice_front(c)
    # c.showPage()
    # c.save()