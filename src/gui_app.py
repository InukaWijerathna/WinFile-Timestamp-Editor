import os
import tkinter as tk
from tkinter import ttk
from single_editor_tab import SingleEditorTab
from batch_editor_tab import BatchEditorTab

class TimestampEditorApp:
    """The main entry loader for the modular Timestamp-Editor application."""
    def __init__(self, root):
        self.root = root
        self.root.title("Timestamp-Editor")
        self.root.geometry("780x540")
        self.root.resizable(False, False)
        
        # Force Windows to associate the application window with our custom brand icon in the taskbar
        try:
            import ctypes
            myappid = 'inukawijerathna.winfiletimestampeditor.forge.1.1'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass
            
        # Load and set native application icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Apply Windows 'vista' theme if available for a clean native look
        style = ttk.Style()
        if 'vista' in style.theme_names():
            style.theme_use('vista')
            
        self.create_widgets()
        
    def create_widgets(self):
        # Subtly integrated footer displaying the version aligned right
        self.footer = ttk.Label(self.root, text="version 1.1", anchor=tk.E, foreground="gray")
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 2))
        
        # Master Notebook Layout
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Instantiate separate tabs as reusable components
        self.single_tab = SingleEditorTab(self.notebook, self.root)
        self.batch_tab = BatchEditorTab(self.notebook, self.root)
        
        # Add frames as tabs to the notebook
        self.notebook.add(self.single_tab, text="Single File Editor")
        self.notebook.add(self.batch_tab, text="Batch File Editor")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimestampEditorApp(root)
    root.mainloop()
