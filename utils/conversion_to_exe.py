import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_save_path(filename):
    if getattr(sys, 'frozen', False):
        print('EXE')
        base_path = os.path.dirname(sys.executable)
    else:
        print("NOT EXE")
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        
    return os.path.join(base_path, filename)