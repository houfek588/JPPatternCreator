from flask import Flask, render_template, request, send_file, send_from_directory, jsonify
# from your_pattern_module import export_pattern  # Replace with your actual module
from main import gener
import os

# app = Flask(__name__)
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         bust = float(request.form.get("bust", 100))
#         waist = float(request.form.get("waist", 80))
#         hip = float(request.form.get("hip", 41))
#         height = float(request.form.get("height", 42))
#         save_file = "test02.pdf"
#         # pdf_path =
#         pdf_path = gener(save_file, bust, waist, hip, height)
#         filename = os.path.basename(pdf_path)
#         # return render_template("index.html", pdf_url=f"{filename}", filename=filename)
#         return render_template("index.html", pdf_url=f"{filename}", filename=filename)
#
#     return render_template("index.html")
#
# @app.route("/<filename>")
# def view_pdf(filename):
#     return send_from_directory(directory=".", path=filename)
#
# @app.route('/browse/<path:filename>')
# def browse_files(filename):
#     return send_from_directory('.', filename)
#
# if __name__ == "__main__":
#     app.run(debug=True)

import random

app = Flask(__name__)

# Dummy vector graphic generator
def generate_svg(slider_values, inputs):
    # Here you'd recalculate your real vector data based on sliders and inputs
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

if __name__ == '__main__':
    app.run(debug=True)

# index.html template to be saved in /templates/index.html
# Create the HTML as follows: