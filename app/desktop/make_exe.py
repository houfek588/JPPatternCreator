import PyInstaller.__main__
import os

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PyInstaller.__main__.run([
    os.path.join(root_dir, 'main.py'),
    '--onefile',
    '--windowed'
])
