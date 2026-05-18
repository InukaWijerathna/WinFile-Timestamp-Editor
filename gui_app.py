import sys
import os

# Append 'src' folder to Python path to import components cleanly
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    import tkinter as tk
    from gui_app import TimestampEditorApp
    
    root = tk.Tk()
    app = TimestampEditorApp(root)
    root.mainloop()
