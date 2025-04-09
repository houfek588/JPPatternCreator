# create directly pdf
if __name__ == "__main__":
    import matplotlib.pyplot as plt

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

    # Remove axes/labels
    ax.axis('off')

    # Save to PDF
    plt.savefig("technical_drawing_mm.pdf", dpi=300)