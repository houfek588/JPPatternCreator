import os
import math
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
    factor = svg_scale / cm

    if part in ('all', 'back'):
        svg_creator.add_lines(mn.scale_lines(sk.get_skeleton_lines(), factor).values())
        svg_creator.add_curve_by_points(mn.scale_points(sk.get_pattern_points(collar=True), factor))

    if part in ('all', 'collar'):
        svg_creator.add_curve_by_points(mn.scale_points(collar.get_pattern_points(), factor), color="blue")

    return svg_creator.to_string()


def get_hosen_handles(meas_file=None, a=5, b=12, c=2, d=15, e=0, f=0, g=0):
    """
    Calculate exact 2D coordinates for CAD Smart Handles on the hosen pattern canvas.
    Coordinates match the SVG canvas coordinate space (cm * SVG_SCALE).
    """
    paper_width_cm = getattr(config, "PAPER_WIDTH_CM", 120)
    origin_y = getattr(config, "PATTERN_ORIGIN_Y_CM", 8)
    svg_scale = getattr(config, "SVG_SCALE", 4)
    origin_x = paper_width_cm * 0.5
    measurements = _load_lower_measurements(meas_file)
    parameters = hosen.HosenPatternParameter(a, b, c, d, e, f, g)
    pattern = hosen.HosenPattern(origin_x, origin_y, measurements, parameters)

    # 1. Waist (center of front waistline curve)
    waist_start = pattern.lines["waist"].get_start_point()
    waist_control = pattern.lines["waist"].get_end_point()
    waist_mid_x = (waist_start[0] + waist_control[0]) / 2.0
    waist_y = waist_start[1] + a

    # 2. Crotch curve / tangent control point
    crotch_end = pattern.lines["crotch"].get_end_point()
    end_tangent = pattern.lines["crotch"].normal_line(crotch_end[0])
    crotch_ctrl = end_tangent.get_point_distance(d)

    # 3. Divide / hip line
    div_line = pattern.lines["divide"]
    div_x = origin_x - pattern.base.measurements["OS"] / 4.0
    div_y = div_line.get_start_point()[1]

    # 4. Instep width
    foot_y = origin_y + pattern.base.measurements["BDK"] - 11
    foot_x = origin_x + b / 2.0

    # 5. Toe / crakow tip
    toe_x = origin_x
    toe_y = origin_y + pattern.base.measurements["BDK"] + 3 + c

    # 6. Outer thigh apex (left side)
    side_wide_end = pattern.lines["side_wide"].get_end_point()
    thigh_left_x = side_wide_end[0]
    thigh_left_y = side_wide_end[1]
    side_wide_vec = pattern.lines["side_wide"].get_vector()
    thigh_left_angle = round((math.degrees(math.atan2(side_wide_vec[1], side_wide_vec[0])) + 180.0) % 360.0, 1)

    # 7. Inner crotch / inseam apex (right side)
    slope_wide_end = pattern.lines["slope_wide"].get_end_point()
    thigh_right_x = slope_wide_end[0]
    thigh_right_y = slope_wide_end[1]
    slope_wide_vec = pattern.lines["slope_wide"].get_vector()
    thigh_right_angle = round(math.degrees(math.atan2(slope_wide_vec[1], slope_wide_vec[0])), 1)

    # Crotch curve tangent angle
    crotch_tangent_vec = end_tangent.get_vector()
    crotch_tangent_angle = round(math.degrees(math.atan2(crotch_tangent_vec[1], crotch_tangent_vec[0])), 1)

    return [
        {
            "id": "slider1",
            "param": "waist_offset",
            "name_cz": "Pas",
            "name_en": "Waist",
            "title_cz": "Snížení pasu",
            "title_en": "Waistline Lowering",
            "x": round(waist_mid_x * svg_scale, 1),
            "y": round(waist_y * svg_scale, 1),
            "direction": "vertical",
            "angle": 90.0,
            "min": 0,
            "max": 25,
            "step": 0.5,
            "value": round(a, 1),
            "unit": "cm",
            "color": "#f43f5e",
            "description_cz": "Tvarování a snížení předního pasového lemu",
            "description_en": "Shaping and lowering the front waistline"
        },
        {
            "id": "slider5",
            "param": "divide_line_offset",
            "name_cz": "Boky",
            "name_en": "Hip",
            "title_cz": "Posun sedové linie",
            "title_en": "Hip Line Level",
            "x": round(div_x * svg_scale, 1),
            "y": round(div_y * svg_scale, 1),
            "direction": "vertical",
            "angle": 90.0,
            "invert": True,
            "min": -15,
            "max": 10,
            "step": 0.5,
            "value": round(e, 1),
            "unit": "cm",
            "color": "#8b5cf6",
            "description_cz": "Posun dělicí linie boků a rozkroku",
            "description_en": "Vertical shift of hip and divide line"
        },
        {
            "id": "slider6",
            "param": "left_wide_offset",
            "name_cz": "Stehno vlevo",
            "name_en": "Left Thigh",
            "title_cz": "Levý posun stehna",
            "title_en": "Left Thigh Offset",
            "x": round(thigh_left_x * svg_scale, 1),
            "y": round(thigh_left_y * svg_scale, 1),
            "direction": "horizontal",
            "angle": thigh_left_angle,
            "invert": True,
            "min": -10,
            "max": 15,
            "step": 0.5,
            "value": round(f, 1),
            "unit": "cm",
            "color": "#3b82f6",
            "description_cz": "Rozšíření vnějšího obvodu stehna a boků vlevo",
            "description_en": "Outer thigh and hip width on the left"
        },
        {
            "id": "slider7",
            "param": "right_wide_offset",
            "name_cz": "Sed vpravo",
            "name_en": "Right Inseam",
            "title_cz": "Pravý posun sedu",
            "title_en": "Right Inseam Offset",
            "x": round(thigh_right_x * svg_scale, 1),
            "y": round(thigh_right_y * svg_scale, 1),
            "direction": "horizontal",
            "angle": thigh_right_angle,
            "min": -10,
            "max": 15,
            "step": 0.5,
            "value": round(g, 1),
            "unit": "cm",
            "color": "#ec4899",
            "description_cz": "Rozšíření vnitřního sedového oblouku a šířky rozkroku",
            "description_en": "Inseam crotch width and inner thigh offset"
        },
        {
            "id": "slider4",
            "param": "upper_corner_tangent",
            "name_cz": "Sed",
            "name_en": "Crotch",
            "title_cz": "Křivka sedu / klínu",
            "title_en": "Crotch Curve",
            "x": round(crotch_ctrl[0] * svg_scale, 1),
            "y": round(crotch_ctrl[1] * svg_scale, 1),
            "direction": "crotch",
            "angle": crotch_tangent_angle,
            "min": 0,
            "max": 24,
            "step": 0.5,
            "value": round(d, 1),
            "unit": "cm",
            "color": "#f59e0b",
            "description_cz": "Vyklenutí sedového klínu a anatomické prohnutí",
            "description_en": "Crotch gusset curve and anatomical shaping"
        },
        {
            "id": "slider2",
            "param": "instep_width",
            "name_cz": "Nárt",
            "name_en": "Instep",
            "title_cz": "Šířka nártu",
            "title_en": "Instep Width",
            "x": round(foot_x * svg_scale, 1),
            "y": round(foot_y * svg_scale, 1),
            "direction": "horizontal",
            "angle": 0.0,
            "min": 0,
            "max": 24,
            "step": 0.5,
            "value": round(b, 1),
            "unit": "cm",
            "color": "#06b6d4",
            "description_cz": "Šířka nártového oblouku a kotníkového přechodu",
            "description_en": "Width of instep arch and ankle transition"
        },
        {
            "id": "slider3",
            "param": "foot_finger_curve",
            "name_cz": "Špička",
            "name_en": "Crakow",
            "title_cz": "Délka špičky (crakow)",
            "title_en": "Pointed Toe Curve",
            "x": round(toe_x * svg_scale, 1),
            "y": round(toe_y * svg_scale, 1),
            "direction": "vertical",
            "angle": 90.0,
            "min": 0,
            "max": 10,
            "step": 0.5,
            "value": round(c, 1),
            "unit": "cm",
            "color": "#10b981",
            "description_cz": "Délka a zakřivení historické špičky (crakow)",
            "description_en": "Length and curve of historical pointed toe"
        }
    ]


def get_bodice_handles(meas_file=None, collar_depth=12):
    """
    Calculate exact 2D coordinates for CAD Smart Handles on the bodice/doublet canvas.
    """
    svg_scale = getattr(config, "SVG_SCALE", 4)
    factor = svg_scale / cm
    m = _load_upper_measurements(meas_file)
    position_x = 3
    position_y = 8
    sk = skeleton.BackPattern(position_x, position_y, m)
    back = skeleton.base.Line(sk.get_neck_line().get_start_point(), sk.get_chest_line().get_start_point())
    v_neck = back.get_point_distance(skeleton.cm_to_pt(collar_depth))

    return [
        {
            "id": "slider1",
            "param": "collar_depth",
            "name_cz": "Límec",
            "name_en": "Collar",
            "title_cz": "Hloubka výstřihu límce",
            "title_en": "Collar Neckline Depth",
            "x": round(v_neck[0] * factor, 1),
            "y": round(v_neck[1] * factor, 1),
            "direction": "vertical",
            "angle": 90.0,
            "min": 5,
            "max": 30,
            "step": 0.5,
            "value": round(collar_depth, 1),
            "unit": "cm",
            "color": "#f43f5e",
            "description_cz": "Hloubka a vykrojení stojáčkového límce kabátce",
            "description_en": "Neckline opening depth for doublet standing collar"
        }
    ]


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
