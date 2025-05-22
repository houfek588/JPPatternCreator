from flask import Flask, render_template, request, jsonify, send_file
import random
# import cairosvg
import io
import json

app = Flask(__name__)
SAVE_PATH = "saved_data.json"

# Dummy vector graphic generator
def generate_svg(slider_values, inputs):
    x = 50 + int(slider_values['slider1']) * 5
    y = 50 + int(slider_values['slider2']) * 5
    size = 20 + int(slider_values['slider3']) * 2
    color = "red" if int(slider_values['slider4']) % 2 == 0 else "blue"
    return f'<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">' \
           f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}" /></svg>'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    sliders = request.json.get("sliders", {})
    inputs = request.json.get("inputs", {})
    svg = generate_svg(sliders, inputs)
    return jsonify({"svg": svg})

@app.route("/export/pdf", methods=["POST"])
def export_pdf():
    svg = request.json.get("svg", "")
    print("Export PDF activated")
    # pdf_data = cairosvg.svg2pdf(bytestring=svg.encode("utf-8"))
    # return send_file(io.BytesIO(pdf_data), mimetype='application/pdf', as_attachment=True, download_name='pattern.pdf')

@app.route("/export/png", methods=["POST"])
def export_png():
    svg = request.json.get("svg", "")
    print("Export PNG activated")
    # png_data = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
    # return send_file(io.BytesIO(png_data), mimetype='image/png', as_attachment=True, download_name='pattern.png')

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "ok", "message": "Data saved successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# index.html template to be saved in /templates/index.html
# Create the HTML as follows: