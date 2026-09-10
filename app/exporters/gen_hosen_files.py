import os
from reportlab.lib.units import cm
import app.exporters.create_pdf as pdf
import app.geometry.hosen as hosen
import app.exporters.create_svg as svg
import app.data.manage as mn
import config
import app.geometry.skeleton as skeleton


def _load_lower_measurements(meas_file):
    """Helper to load LowerMeasurements from dict, file path, or default."""
    measurements = hosen.LowerMeasurements()
    if isinstance(meas_file, dict):
        measurements = hosen.LowerMeasurements(meas_file)
    elif isinstance(meas_file, str) and os.path.exists(meas_file):
        measurements.load_from_json(meas_file)
    else:
        # Default fallback values for testing
        default_meas = {
            "title": "Sample Pattern",
            "VP": 175, "OP": 98, "OS": 116,
            "BDK": 122, "KD": 90, "O_st": 61,
            "O_nk": 46, "O_l": 40, "O_kot": 26
        }
        measurements = hosen.LowerMeasurements(default_meas)
    return measurements


def _load_upper_measurements(meas_file):
    """Helper to load Measurements for upper body/bodice."""
    if isinstance(meas_file, dict):
        m = skeleton.Measurements(meas_file)
    elif isinstance(meas_file, str) and os.path.exists(meas_file):
        m = skeleton.Measurements()
        m.load_from_json(meas_file)
    else:
        m = skeleton.Measurements({
            "OH": 100,
            "OP": 80,
            "DZ": 40,
            "Szad": 42
        })
    return m


def gen_hosen_svg_string(meas_file=None, a=5, b=12, c=2, d=15, e=0, f=0, g=0, part='all'):
    """
    Generate an SVG string representing the hosen pattern based on measurements and parameters.

    :param meas_file: Path to JSON file containing body measurements or dict
    :param a, b, c, d, e, f, g: Parameters for HosenPatternParameter
    :param part: Part of garment to render ('all', 'main', 'crotch', 'skeleton', etc.)
    :return: SVG as string
    """
    paper_width_cm = getattr(config, "PAPER_WIDTH_CM", 120)
    paper_height_cm = getattr(config, "PAPER_HEIGHT_CM", 160)
    svg_scale = getattr(config, "SVG_SCALE", 4)

    svg_width = paper_width_cm * svg_scale
    svg_height = paper_height_cm * svg_scale

    svg_creator = svg.SVGCreator(svg_width, svg_height)
    measurements = _load_lower_measurements(meas_file)

    origin_x = paper_width_cm * 0.5
    origin_y = getattr(config, "PATTERN_ORIGIN_Y_CM", 8)

    parameters = hosen.HosenPatternParameter(a, b, c, d, e, f, g)
    pattern = hosen.HosenPattern(origin_x, origin_y, measurements, parameters)

    skeleton_lines = pattern.get_skeleton_lines()
    seam_points = pattern.get_pattern_points()

    texts = pattern.check_thigh()
    test_pos = pattern.get_lines_description()
    if len(test_pos) > 2:
        xy = (test_pos[2].x * svg_scale, (test_pos[2].y + 5) * svg_scale)
        svg_creator.add_text(xy, texts[0])

    if part == 'all':
        svg_creator.add_lines(mn.scale_lines(skeleton_lines, svg_scale).values())
        svg_creator.add_curve_by_points(mn.scale_points(seam_points, svg_scale))
    elif part == 'skeleton':
        svg_creator.add_lines(mn.scale_lines(skeleton_lines, svg_scale).values())
    elif part == 'contour' or part == 'main':
        svg_creator.add_curve_by_points(mn.scale_points(seam_points, svg_scale))
    elif part == 'crotch':
        crotch_lines = pattern.crotch.get_skeleton_lines()
        svg_creator.add_lines(mn.scale_lines(crotch_lines, svg_scale).values(), color="blue")
    else:
        svg_creator.add_lines(mn.scale_lines(skeleton_lines, svg_scale).values())
        svg_creator.add_curve_by_points(mn.scale_points(seam_points, svg_scale))

    return svg_creator.to_string()


def save_hosen_to_pdf(meas_file, pdf_file, a=5, b=12, c=2, d=15, e=0, f=0, g=0, png=False, part='all'):
    """
    Generates a pattern PDF (or PNG) from measurement data and parameters.
    """
    paper_width_cm = getattr(config, "PAPER_WIDTH_CM", 120)
    paper_height_cm = getattr(config, "PAPER_HEIGHT_CM", 160)
    paper_cm = (paper_width_cm, paper_height_cm)
    paper_pt = mn.scale_one_point(paper_cm, cm)

    p = pdf.MakePdf(pdf_file, landscape=False, paper_size=paper_pt)

    measurements = _load_lower_measurements(meas_file)

    position_x = paper_cm[0] * 0.5
    position_y = getattr(config, "PATTERN_ORIGIN_Y_CM", 8)

    parameters = hosen.HosenPatternParameter(a, b, c, d, e, f, g)
    pattern = hosen.HosenPattern(position_x, position_y, measurements, parameters)

    skeleton_lines = pattern.get_skeleton_lines()
    pattern_points = pattern.get_pattern_points()

    scaled_lines = mn.scale_lines(skeleton_lines, cm)
    scaled_points = mn.scale_points(pattern_points, cm)

    if part in ('all', 'skeleton'):
        p.add_lines(scaled_lines.values())
    if part in ('all', 'contour', 'main'):
        p.add_curve_by_points(scaled_points, line_width=3)
    elif part == 'crotch':
        crotch_lines = mn.scale_lines(pattern.crotch.get_skeleton_lines(), cm)
        p.add_lines(crotch_lines.values(), color="blue", line_width=2)

    main_description = pattern.get_main_description()
    x, y, text = main_description.get_text(cm)
    p.add_text(x, y, text, font_size=32)

    for desc in pattern.get_lines_description():
        x, y, text = desc.get_text(cm)
        p.add_text(x, y, text, font_size=26)

    for point in pattern.get_important_points():
        p.add_mark(mn.scale_one_point(point, cm), 15)

    if png:
        p.save_png()
    else:
        p.save_pdf()


def gen_bodice_svg_string(meas_file=None, collar_depth=12, part='all'):
    """
    Generate an SVG string representing the bodice/doublet pattern.
    """
    paper_width_cm = getattr(config, "PAPER_WIDTH_CM", 120)
    paper_height_cm = getattr(config, "PAPER_HEIGHT_CM", 160)
    svg_scale = getattr(config, "SVG_SCALE", 4)

    svg_width = paper_width_cm * svg_scale
    svg_height = paper_height_cm * svg_scale

    svg_creator = svg.SVGCreator(svg_width, svg_height)
    m = _load_upper_measurements(meas_file)

    position_x = 3
    position_y = 8

    sk = skeleton.BackPattern(position_x, position_y, m)
    collar = sk.generate_collar(collar_depth)

    if part in ('all', 'back'):
        svg_creator.add_lines(mn.scale_lines(sk.get_skeleton_lines(), svg_scale).values())
        svg_creator.add_curve_by_points(mn.scale_points(sk.get_pattern_points(collar=True), svg_scale))

    if part in ('all', 'collar'):
        svg_creator.add_curve_by_points(mn.scale_points(collar.get_pattern_points(), svg_scale), color="blue")

    return svg_creator.to_string()


def save_bodice_to_pdf(meas_file, pdf_file, collar_depth=12, png=False, part='all'):
    """
    Generate PDF/PNG for bodice/doublet pattern.
    """
    paper_width_cm = getattr(config, "PAPER_WIDTH_CM", 120)
    paper_height_cm = getattr(config, "PAPER_HEIGHT_CM", 160)
    paper_cm = (paper_width_cm, paper_height_cm)
    paper_pt = mn.scale_one_point(paper_cm, cm)

    p = pdf.MakePdf(pdf_file, landscape=False, paper_size=paper_pt)
    m = _load_upper_measurements(meas_file)

    position_x = 3
    position_y = 8

    sk = skeleton.BackPattern(position_x, position_y, m)
    collar = sk.generate_collar(collar_depth)

    if part in ('all', 'back'):
        lines = sk.get_skeleton_lines()
        p.add_lines(lines.values())
        p.add_curve_by_points(sk.get_pattern_points(collar=True), line_width=3, closed=False)

    if part in ('all', 'collar'):
        p.add_curve_by_points(collar.get_pattern_points(), line_width=3)

    if png:
        p.save_png()
    else:
        p.save_pdf()
