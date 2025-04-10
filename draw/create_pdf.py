import matplotlib.pyplot as plt

class MakePdf:
    def __init__(self, paper_size, landscape=False):
        # Set up figure with specific size in mm
        paper = PaperSizes()

        if landscape:
            page_width_mm = paper.get_paper_size(paper_size)[0]  # A4 width
            page_height_mm = paper.get_paper_size(paper_size)[1]  # A4 height
        else:
            page_width_mm = paper.get_paper_size(paper_size)[1]  # A4 width
            page_height_mm = paper.get_paper_size(paper_size)[0]  # A4 height

        # Convert mm to inches (matplotlib uses inches)
        mm_to_inch = 1 / 25.4
        self.fig = plt.figure(figsize=(page_width_mm * mm_to_inch, page_height_mm * mm_to_inch))

        # Create axes that match real-world mm coordinates
        self.ax = self.fig.add_axes((0, 0, 1, 1))  # full-page axes
        self.ax.set_xlim(0, page_width_mm)
        self.ax.set_ylim(0, page_height_mm)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()  # Optional: matches CAD-style Y-down layout
        # Remove axes/labels
        self.ax.axis('off')

    def add_mark(self, pos: tuple, radius, color="black", line_width=1, fill=False):
        x_pos = pos[0]
        y_pos = pos[1]
        circle = plt.Circle((x_pos, y_pos), radius, color=color, fill=fill, linewidth=line_width)

        add = 1.5*radius
        self.add_line((x_pos - add, y_pos),(x_pos + add, y_pos), color, line_width)
        self.add_line((x_pos, y_pos - add), (x_pos, y_pos + add), color, line_width)
        self.ax.add_patch(circle)

    def add_polygon(self, polygon, color="black", line_width=1, closed=True):
        square = plt.Polygon(polygon, closed=closed, fill=False, linewidth=line_width, color=color)
        self.ax.add_patch(square)


    def add_line(self, origin: tuple, end: tuple, color="black", line_width=1):
        self.ax.plot([origin[0], end[0]], [origin[1], end[1]], color=color, linewidth=line_width)

    def add_text(self, x_pos, y_pos, text, font_size=11, align="center"):
        # fontsize = desired_mm / 0.3528
        self.ax.text(x_pos, y_pos, text, fontsize=font_size, ha=align, va="bottom")

    def save_pdf(self, file_name):
        # Save to PDF
        plt.savefig(file_name, dpi=300)


class PaperSizes:
    def __init__(self):
        self.sizes = {"A4": (297, 210),
                      "A3": (420, 297),
                      "A2": (594, 420)}
    def get_paper_size(self, size):
        return self.sizes.get(size)
def basic_pdf(file_name):
    # Set up figure with specific size in mm
    page_width_mm = 210  # A4 width
    page_height_mm = 297  # A4 height

    # Convert mm to inches (matplotlib uses inches)
    mm_to_inch = 1 / 25.4
    fig = plt.figure(figsize=(page_width_mm * mm_to_inch, page_height_mm * mm_to_inch))

    # Create axes that match real-world mm coordinates
    ax = fig.add_axes([0, 0, 1, 1])  # full-page axes
    ax.set_xlim(0, page_width_mm)
    ax.set_ylim(0, page_height_mm)
    ax.set_aspect('equal')
    ax.invert_yaxis()  # Optional: matches CAD-style Y-down layout

    # --- Drawing Shapes in mm ---

    # Circle at (30, 30) with radius 10 mm
    circle = plt.Circle((30, 30), 10, fill=False, linewidth=0.5)
    ax.add_patch(circle)

    # Square with side 12 mm, bottom-left at (60, 30)
    square = plt.Polygon([
        (60, 30),
        (72, 30),
        (72, 42),
        (60, 42),
    ], closed=True, fill=False, linewidth=0.5)
    ax.add_patch(square)

    # Line from (10, 10) to (100, 95)
    ax.plot([10, 100], [10, 95], color='black', linewidth=0.5)




