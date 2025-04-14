# app.py
# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def home():
#     return "Hello from the cloud!"
#
# if __name__ == '__main__':
#     app.run()
from flask import Flask, render_template, request, send_file, send_from_directory
# from your_pattern_module import export_pattern  # Replace with your actual module
from main import gener
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bust = float(request.form.get("bust", 100))
        waist = float(request.form.get("waist", 80))
        hip = float(request.form.get("hip", 41))
        height = float(request.form.get("height", 42))
        save_file = "test02.pdf"
        # pdf_path =
        pdf_path = gener(save_file, bust, waist, hip, height)
        filename = os.path.basename(pdf_path)
        # return render_template("index.html", pdf_url=f"{filename}", filename=filename)
        return render_template("index.html", pdf_url=f"{filename}", filename=filename)

    return render_template("index.html")

@app.route("/<filename>")
def view_pdf(filename):
    return send_from_directory(directory=".", path=filename)

@app.route('/browse/<path:filename>')
def browse_files(filename):
    return send_from_directory('.', filename)

if __name__ == "__main__":
    app.run(debug=True)