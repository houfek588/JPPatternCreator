import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QSlider, QLineEdit, QTextEdit, QFileDialog, QMessageBox, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QPalette, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import QTimer
import exporters.gen_hosen_files as file_gen
import geometry.measurements as meas
import config

class PatternCreatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hosen Pattern Creator")
        self.resize(1200, 900)

        self.inputs = {}
        self.sliders = {}

        self.meas_file = config.DESKTOP_MEAS_FILE

        n = 175
        self.svg_widget = QSvgWidget()
        self.svg_widget.setStyleSheet("background-color: white;")
        self.svg_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.svg_widget.setMinimumSize(3*n, 4*n)  # 3:4 aspect ratio (width:height)

        self.setStyleSheet("""
                    QWidget {
                        background-color: #f4f4f4;
                    }
                    QLineEdit, QTextEdit {
                        background-color: #dfe6e9;
                        color: black;
                        border: 1px solid #ccc;
                        padding: 4px;
                        font-size: 14px;
                    }
                    QLabel {
                        color: #701516;
                        font-weight: bold;
                    }
                    QPushButton {
                        background-color: #701516;
                        color: white;
                        border: none;
                        padding: 6px 12px;
                        font-size: 14px;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #8e2b28;
                    }
                    QPushButton:pressed {
                        background-color: #5c0f10;
                    }
                    QSlider::groove:vertical {
                        background: #dfe6e9;
                        width: 6px;
                        margin: 0px;
                    }
                    QSlider::handle:vertical {
                        background: #701516;
                        height: 20px;
                        margin: 0 -2px;
                        border-radius: 3px;
                    }
                """)

        self.init_ui()
        self.generate_svg()

        self.generate_timer = QTimer(self)
        self.generate_timer.setSingleShot(True)
        self.generate_timer.timeout.connect(self.generate_svg)

    def init_ui(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()

        # Logo
        logo = QLabel()
        logo.setPixmap(QPixmap(config.LOGO_PATH).scaledToWidth(100, Qt.TransformationMode.SmoothTransformation))
        left_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Input fields with initial values
        form_layout = QGridLayout()
        input_labels = [
            ("title", "Title"), ("VP", "Height"), ("OP", "Waist"),
            ("OS", "Hips"), ("BDK", "Side length"), ("KD", "Crotch length"),
            ("O_st", "Thigh c."), ("O_nk", "Above knee c."),
            ("O_l", "Calf c."), ("O_kot", "Ankle c.")
        ]
        init_values = {
            "title": "Sample Pattern",
            "VP": "175", "OP": "98", "OS": "116",
            "BDK": "122", "KD": "90", "O_st": "61",
            "O_nk": "46", "O_l": "40", "O_kot": "26"
        }
        init_shortcuts = {
            "title": " ",
            "VP": "VP", "OP": "OP", "OS": "OS",
            "BDK": "BDK", "KD": "KD", "O_st": "OST",
            "O_nk": "ONK", "O_l": "OL", "O_kot": "OK"
        }

        for i, (key, label_text) in enumerate(input_labels):
            row = i // 2
            col = (i % 2) * 3
            form_layout.addWidget(QLabel(label_text), row, col)
            form_layout.addWidget(QLabel(init_shortcuts[key]), row, col + 1)
            field = QLineEdit()
            field.setText(init_values.get(key, ""))
            # self.inputs[key] = field
            # form_layout.addWidget(field, row, col + 2)

            self.inputs[key] = field
            # field.textChanged.connect(self.generate_svg)
            field.textChanged.connect(self.schedule_generate_svg)
            form_layout.addWidget(field, row, col + 2)
        # for i, label in enumerate(input_labels):
        #     form_layout.addWidget(QLabel("Waist"), i // 2, (i % 2) * 2)
        #     form_layout.addWidget(QLabel(label), i // 2, (i % 2) * 2 + 1)
        #     field = QLineEdit()
        #     field.setText(init_values.get(label, ""))
        #     self.inputs[label] = field
        #     form_layout.addWidget(field, i // 2, (i % 2) * 2 + 2)
        left_layout.addLayout(form_layout)

        # Sliders (7 total)
        slider_layout = QHBoxLayout()
        minima = [0, -15, 0, -10, -10, 0, 0]
        maxima = [25, 10, 24, 15, 15, 10, 24]
        slider_init = [5, 0, 12, 0, 0, 5, 12]
        slider_names = ["Lowering\nwaist",
                        "Divide\nline",
                        "Corner\nshape",
                        "Left\noffset",
                        "Right\noffset",
                        "Foot\nshape",
                        "Instep\nwide"]

        for i in range(1, 8):
            vbox = QVBoxLayout()
            slider = QSlider(Qt.Orientation.Vertical)
            slider.setMinimum(minima[i-1])
            slider.setMaximum(maxima[i-1])
            slider.setValue(slider_init[i-1])
            # slider.valueChanged.connect(self.generate_svg)
            slider.valueChanged.connect(lambda value, i=i: self.update_slider_label(i, value))
            label = QLabel(f"{slider_names[i-1]}")
            value_label = QLabel(f"Value: {slider.value()}")
            self.sliders[f"slider{i}"] = (slider, label, value_label)
            vbox.addWidget(label)
            vbox.addWidget(slider)
            vbox.addWidget(value_label)
            slider_layout.addLayout(vbox)
        left_layout.addLayout(slider_layout)

        # Buttons
        button_layout = QHBoxLayout()
        gen_btn = QPushButton("Generate")
        gen_btn.clicked.connect(self.generate_svg)
        # save_btn = QPushButton("Save JSON")
        # save_btn.clicked.connect(self.save_json)
        export_btn = QPushButton("Export PDF")
        export_btn.clicked.connect(self.export_pdf)
        button_layout.addWidget(gen_btn)
        # button_layout.addWidget(save_btn)
        button_layout.addWidget(export_btn)
        left_layout.addLayout(button_layout)

        # SVG display on the right
        right_layout = QVBoxLayout()
        svg_label = QLabel("Generated Pattern:")
        svg_label.setStyleSheet("font-size: 18px; color: #701516;")
        right_layout.addWidget(svg_label)
        right_layout.addWidget(self.svg_widget)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 3)

        self.setLayout(main_layout)

    def slider_values(self):
        return {f"slider{i}": self.sliders[f"slider{i}"][0].value() for i in range(1, 8)}

    def update_slider_label(self, i, value):
        self.sliders[f'slider{i}'][2].setText(f"Value: {value}")
        self.generate_svg()

    def schedule_generate_svg(self):
        self.generate_timer.start(500)

    def input_values(self):
        result = {}
        for key, widget in self.inputs.items():
            text = widget.text().strip()
            if not text:
                result[key] = None
            else:
                try:
                    result[key] = float(text)
                except ValueError:
                    result[key] = text
        return result

    def generate_svg(self):
        sliders = self.slider_values()
        inputs = self.input_values()

        a, b, c, d, e, f, g = self.slider_values_scale(sliders)

        try:
            m = meas.LowerMeasurements(inputs)
            m.save_to_json(self.meas_file)
            svg_str = file_gen.gen_hosen_svg_string(self.meas_file, a, b, c, d, e, f, g)
            self.svg_widget.load(bytearray(svg_str, encoding='utf-8'))
        except meas.ValidationError as err:
            print(f"Validation Error (SVG drawing skipped): {err}")

    def slider_values_scale(self, sliders):
        a = int(sliders['slider1']) * 1
        b = int(sliders['slider7']) * 1
        c = int(sliders['slider6']) * 1
        d = int(sliders['slider3']) * 1
        e = int(sliders['slider2']) * 1
        f = int(sliders['slider4']) * 1
        g = int(sliders['slider5']) * 1
        return (a, b, c, d, e, f, g)

    def save_json(self):
        data = {
            'sliders': self.slider_values(),
            'inputs': self.input_values()
        }
        path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "pattern.json", "JSON Files (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            QMessageBox.information(self, "Saved", f"Data saved to {path}")

    def export_pdf(self):
        try:
            inputs = self.input_values()
            m = meas.LowerMeasurements(inputs)
        except meas.ValidationError as err:
            QMessageBox.warning(self, "Validation Error", f"Cannot export PDF: {err}")
            return

        sliders = self.slider_values()
        a, b, c, d, e, f, g = self.slider_values_scale(sliders)

        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "pattern.pdf", "PDF Files (*.pdf)")
        if not path:
            return

        file_gen.save_hosen_to_pdf(self.meas_file, path, a, b, c, d, e, f, g, png=False)
        QMessageBox.information(self, "Exported", f"PDF has been generated and saved to {path}")

def start_window():
    app = QApplication(sys.argv)
    window = PatternCreatorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    start_window()
    # app = QApplication(sys.argv)
    # window = PatternCreatorApp()
    # window.show()
    # sys.exit(app.exec())
