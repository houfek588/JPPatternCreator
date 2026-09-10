import os
import uuid
import tempfile
from flask import Flask, send_from_directory, request, jsonify, send_file, after_this_request
import app.exporters.gen_hosen_files as file_gen
import app.geometry.measurements as meas
import config

# Path to built React frontend
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'dist')

if os.path.exists(FRONTEND_DIST):
    app = Flask(
        __name__,
        static_folder=os.path.join(FRONTEND_DIST, 'assets'),
        static_url_path='/assets'
    )
else:
    app = Flask(__name__)


@app.route("/")
def index():
    if os.path.exists(FRONTEND_DIST):
        return send_from_directory(FRONTEND_DIST, "index.html")
    return "JPPatternCreator Web API Server running. Frontend dist directory not found."


@app.route("/<path:path>")
def static_proxy(path):
    if os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    return jsonify({"error": "File not found"}), 404


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    pattern_type = data.get("patternType", data.get("pattern_type", "hosen"))
    inputs = data.get("inputs", data.get("measurements", {}))
    sliders = data.get("sliders", {})
    part = data.get("part", "all")

    try:
        if pattern_type == "bodice":
            collar_depth = float(sliders.get("slider1", 12))
            svg_str = file_gen.gen_bodice_svg_string(inputs, collar_depth=collar_depth, part=part)
            handles = file_gen.get_bodice_handles(inputs, collar_depth=collar_depth)
        else:
            a = float(sliders.get("slider1", 5))
            b = float(sliders.get("slider2", 12))
            c = float(sliders.get("slider3", 5))
            d = float(sliders.get("slider4", 12))
            e = float(sliders.get("slider5", 0))
            f = float(sliders.get("slider6", 0))
            g = float(sliders.get("slider7", 0))
            svg_str = file_gen.gen_hosen_svg_string(inputs, a, b, c, d, e, f, g, part=part)
            handles = file_gen.get_hosen_handles(inputs, a, b, c, d, e, f, g)

        return jsonify({"svg": svg_str, "handles": handles, "status": "success"})
    except meas.ValidationError as err:
        return jsonify({"message": str(err), "status": "error"}), 400
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route("/export/pdf", methods=["POST"])
def export_pdf():
    data = request.get_json() or {}
    pattern_type = data.get("patternType", data.get("pattern_type", "hosen"))
    inputs = data.get("inputs", data.get("measurements", {}))
    sliders = data.get("sliders", {})
    part = data.get("part", "all")

    temp_id = str(uuid.uuid4())
    temp_pdf = os.path.join(tempfile.gettempdir(), f"{temp_id}.pdf")

    try:
        if pattern_type == "bodice":
            collar_depth = float(sliders.get("slider1", 12))
            file_gen.save_bodice_to_pdf(inputs, temp_pdf, collar_depth=collar_depth, png=False, part=part)
        else:
            a = float(sliders.get("slider1", 5))
            b = float(sliders.get("slider2", 12))
            c = float(sliders.get("slider3", 5))
            d = float(sliders.get("slider4", 12))
            e = float(sliders.get("slider5", 0))
            f = float(sliders.get("slider6", 0))
            g = float(sliders.get("slider7", 0))
            file_gen.save_hosen_to_pdf(inputs, temp_pdf, a, b, c, d, e, f, g, png=False, part=part)

        @after_this_request
        def remove_temp_file(response):
            try:
                if os.path.exists(temp_pdf):
                    os.remove(temp_pdf)
            except Exception:
                pass
            return response

        title = inputs.get("title", "pattern") if isinstance(inputs, dict) else "pattern"
        safe_title = "".join(c for c in str(title) if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_') or "pattern"
        return send_file(temp_pdf, as_attachment=True, download_name=f"{safe_title}.pdf", mimetype="application/pdf")
    except Exception as e:
        if os.path.exists(temp_pdf):
            try:
                os.remove(temp_pdf)
            except Exception:
                pass
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route("/export/png", methods=["POST"])
def export_png():
    data = request.get_json() or {}
    pattern_type = data.get("patternType", data.get("pattern_type", "hosen"))
    inputs = data.get("inputs", data.get("measurements", {}))
    sliders = data.get("sliders", {})
    part = data.get("part", "all")

    temp_id = str(uuid.uuid4())
    temp_pdf = os.path.join(tempfile.gettempdir(), f"{temp_id}.pdf")
    temp_png = os.path.join(tempfile.gettempdir(), f"{temp_id}.png")

    try:
        if pattern_type == "bodice":
            collar_depth = float(sliders.get("slider1", 12))
            file_gen.save_bodice_to_pdf(inputs, temp_pdf, collar_depth=collar_depth, png=True, part=part)
        else:
            a = float(sliders.get("slider1", 5))
            b = float(sliders.get("slider2", 12))
            c = float(sliders.get("slider3", 5))
            d = float(sliders.get("slider4", 12))
            e = float(sliders.get("slider5", 0))
            f = float(sliders.get("slider6", 0))
            g = float(sliders.get("slider7", 0))
            file_gen.save_hosen_to_pdf(inputs, temp_pdf, a, b, c, d, e, f, g, png=True, part=part)

        @after_this_request
        def remove_temp_files(response):
            for path in (temp_pdf, temp_png):
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except Exception:
                    pass
            return response

        title = inputs.get("title", "pattern") if isinstance(inputs, dict) else "pattern"
        safe_title = "".join(c for c in str(title) if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_') or "pattern"
        return send_file(temp_png, as_attachment=True, download_name=f"{safe_title}.png", mimetype="image/png")
    except Exception as e:
        for path in (temp_pdf, temp_png):
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
        return jsonify({"message": str(e), "status": "error"}), 500


def start_server(host="127.0.0.1", port=5000, debug=True):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    start_server()
