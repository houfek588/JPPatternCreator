import output.create_pdf as pdf
import geometry.hosen as hosen
import output.create_svg as svg
import data.manage as mn

from reportlab.lib.units import cm


def gen_hosen_svg_string(meas_file, a, b, c, d):
    """
    Generate an SVG string representing the back part of hosen pattern based on measurements and parameters.

    :param meas_file: Path to JSON file containing body measurements
    :param a, b, c, d: Parameters for HosenPatternParameter (shape modifiers)
    :return: SVG as string
    """
    # Define SVG canvas size in centimeters
    paper_width_cm, paper_height_cm = 120, 160

    # Define drawing scale: 1 cm = 4 SVG units (for higher resolution)
    svg_scale = 4
    svg_width = paper_width_cm * svg_scale
    svg_height = paper_height_cm * svg_scale

    # Initialize SVG drawing context
    svg_creator = svg.SVGCreator(svg_width, svg_height)

    # Load body measurements from JSON
    measurements = hosen.LowerMeasurements()
    measurements.load_from_json(meas_file)

    # Define pattern origin point (X centered on page, Y at margin)
    origin_x = paper_width_cm * 0.5
    origin_y = 8  # cm from top

    # Create hosen pattern and parameters
    pattern = hosen.HosenPattern(origin_x, origin_y, measurements)
    pattern_param = hosen.HosenPatternParameter(a, b, c, d)

    # Generate construction lines and seam curve
    skeleton_lines = pattern.get_skeleton_lines()
    seam_points = pattern.get_pattern_points(pattern_param)

    # Add scaled elements to SVG
    svg_creator.add_lines(mn.scale_lines(skeleton_lines, svg_scale).values())
    svg_creator.add_curve_by_points(mn.scale_points(seam_points, svg_scale))

    # Export SVG as string
    return svg_creator.to_string()


def save_hosen_to_pdf(meas_file, a, b, c, d, png=False):
    """
    Generates a pattern PDF (or PNG) from measurement data and parameters.

    Parameters:
    - meas_file: path to the measurement JSON file
    - a, b, c, d: pattern parameters (floats)
    - png (bool): if True, export as PNG; else export as PDF and JSON
    """

    # Define paper size in centimeters (width, height)
    paper_cm = (120, 160)
    paper_pt = mn.scale_one_point(paper_cm, cm)

    # Create PDF document
    p = pdf.MakePdf("server_data/server_test03.pdf", landscape=False, paper_size=paper_pt)

    # Load and immediately re-save measurement data
    m = hosen.LowerMeasurements()
    m.load_from_json(meas_file)
    m.save_to_json(meas_file)

    # Set pattern drawing origin point
    position_x = paper_cm[0] * 0.5
    position_y = 8

    # Create pattern object and parameters
    pattern = hosen.HosenPattern(position_x, position_y, m)
    parameters = hosen.HosenPatternParameter(a, b, c, d)

    # Generate geometry: lines and points
    skeleton_lines = pattern.get_skeleton_lines()
    pattern_points = pattern.get_pattern_points(parameters)

    # Scale to points (PDF units)
    scaled_lines = mn.scale_lines(skeleton_lines, cm)
    scaled_points = mn.scale_points(pattern_points, cm)

    # Add pattern to PDF
    p.add_lines(scaled_lines.values())
    p.add_curve_by_points(scaled_points, line_width=3)

    # Add main title/label text
    main_description = pattern.get_main_description()
    x, y, text = main_description.get_text(cm)
    p.add_text(x, y, text, font_size=32)

    # Add annotations for specific lines
    for desc in pattern.get_lines_description():
        x, y, text = desc.get_text(cm)
        p.add_text(x, y, text, font_size=26)

    # Mark key construction points
    for point in pattern.get_important_points():
        p.add_mark(mn.scale_one_point(point, cm), 15)

    # Export PDF or PNG
    if png:
        p.save_png()
    else:
        p.save_pdf()

        # Also export construction data as JSON
        js = mn.SaveLinesToJson(skeleton_lines)
        js.save("server_data/json_test03.json")
