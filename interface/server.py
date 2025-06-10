from flask import Flask, render_template, request, jsonify, send_file
import random
# import cairosvg
import io
import json
import output.gen_hosen_files as file_gen
import geometry.measurements as meas

app = Flask(__name__)
SAVE_PATH = "saved_data.json"

# Dummy vector graphic generator
def slider_values_scale(slider_values):
    print(f"slider_values: {slider_values}")

    a = float(slider_values['slider1']) * 1
    b = float(slider_values['slider2']) * 1
    c = float(slider_values['slider3']) * 1
    d = float(slider_values['slider4']) * 1
    e = float(slider_values['slider5']) * 1
    f = float(slider_values['slider6']) * 1
    g = float(slider_values['slider7']) * 1

    return (a,b,c,d,e,f,g)

def generate_svg(slider_values, inputs):

    a, b, c, d, e, f, g = slider_values_scale(slider_values)

    return file_gen.gen_hosen_svg_string("interface/server_data/meas_test02.json", a, b, c, d, e, f, g)
    # return f'<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">' \
    #        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}" /></svg>'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    print("generate activated")
    sliders = request.json.get("sliders", {})
    inputs = request.json.get("inputs", {})

    print(f"inputs: {inputs}")
    m = meas.LowerMeasurements(inputs)
    m.save_to_json("interface/server_data/meas_test02.json")

    svg = generate_svg(sliders, inputs)
    return jsonify({"svg": svg})

@app.route("/export/pdf", methods=["POST"])
def export_pdf():
    sliders = request.json.get("sliders", {})
    # inputs = request.json.get("inputs", {})

    a, b, c, d, e, f, g = slider_values_scale(sliders)

    file_gen.save_hosen_to_pdf("interface/server_data/meas_test02.json", a, b, c, d, e, f, g)

    # svg = request.json.get("svg", "")
    print("Export PDF activated")

    return send_file("server_data/server_test03.pdf", mimetype='application/pdf', as_attachment=True)

@app.route("/export/png", methods=["POST"])
def export_png():
    sliders = request.json.get("sliders", {})
    # inputs = request.json.get("inputs", {})

    a, b, c, d, e, f, g = slider_values_scale(sliders)

    file_gen.save_hosen_to_pdf("interface/server_data/meas_test02.json", a, b, c, d, e, f, g, png=True)
    print("Export PNG activated")
    # png_data = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
    # return send_file(io.BytesIO(png_data), mimetype='image/png', as_attachment=True, download_name='pattern.png')
    # return send_file("server_data/server_test03.png", mimetype='application/pdf', as_attachment=True)
    return send_file("interface/server_data/server_test03.png", mimetype='image/png', as_attachment=True, download_name="pattern.png")

@app.route("/save", methods=["POST"])
def save():
    print("save inputs activated")
    data = request.json
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "ok", "message": "Data saved successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def start_server():
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)

# index.html template to be saved in /templates/index.html
# Create the HTML as follows: