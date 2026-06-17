# Constants: paper size, units, margins, settings
import os

# Project root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Paper dimensions in cm
PAPER_WIDTH_CM = 120
PAPER_HEIGHT_CM = 160

# SVG renderer settings
SVG_SCALE = 4

# Pattern placement offset from top (in cm)
PATTERN_ORIGIN_Y_CM = 8

# Desktop client settings
DESKTOP_MEAS_FILE = os.path.join(ROOT_DIR, "desktop", "meas_Qt01.json")

# Web server settings
SERVER_SAVE_PATH = os.path.join(ROOT_DIR, "saved_data.json")
SERVER_MEAS_FILE = os.path.join(ROOT_DIR, "web", "server_data", "meas_test02.json")
SERVER_PDF_FILE = os.path.join(ROOT_DIR, "web", "server_data", "server_test03.pdf")
SERVER_PNG_FILE = os.path.join(ROOT_DIR, "web", "server_data", "server_test03.png")

# Asset paths
LOGO_PATH = os.path.join(ROOT_DIR, "web", "static", "logo.png")