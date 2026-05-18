import tkinter as tk
from tkinter import ttk
from single_editor_tab import SingleEditorTab
from batch_editor_tab import BatchEditorTab

class TimestampEditorApp:
    """The main entry loader for the modular Timestamp-Editor application."""
    def __init__(self, root):
        self.root = root
        self.root.title("Timestamp-Editor")
        self.root.geometry("680x440")
        self.root.resizable(False, False)
        
        # Apply Windows 'vista' theme if available for a clean native look
        style = ttk.Style()
        if 'vista' in style.theme_names():
            style.theme_use('vista')
            
        self.create_widgets()
        
    def create_widgets(self):
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
