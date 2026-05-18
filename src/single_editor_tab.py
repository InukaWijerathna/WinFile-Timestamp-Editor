import os
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from date_time_pickers import DatePicker, TimePicker
from win32_metadata import set_file_timestamps

class SingleEditorTab(ttk.Frame):
    """The Single File Editor UI tab and logic."""
    def __init__(self, parent, root_window):
        super().__init__(parent)
        self.root_window = root_window
        
        # Reactive string variables for binding GUI fields
        self.file_path = tk.StringVar()
        self.ctime_var = tk.StringVar()
        self.mtime_var = tk.StringVar()
        self.atime_var = tk.StringVar()
        
        self.build_ui()
        
    def build_ui(self):
        # 1. Target File Selection Frame
        file_frame = ttk.LabelFrame(self, text="Target File Configuration", padding=15)
        file_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Entry(file_frame, textvariable=self.file_path, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).pack(side=tk.RIGHT)
        
        # 2. File Metadata Editor Frame
        meta_frame = ttk.LabelFrame(self, text="Low-Level System Metadata (YYYY-MM-DD HH-MM-SS)", padding=15)
        meta_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Creation Time (ctime)
        ttk.Label(meta_frame, text="Creation Time:").grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.ctime_var, width=30).grid(row=0, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.ctime_var)).grid(row=0, column=2, padx=(0, 10))
        
        # Modified Time (mtime)
        ttk.Label(meta_frame, text="Modified Time:").grid(row=1, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.mtime_var, width=30).grid(row=1, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.mtime_var)).grid(row=1, column=2, padx=(0, 10))
        
        # Accessed Time (atime)
        ttk.Label(meta_frame, text="Accessed Time:").grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.atime_var, width=30).grid(row=2, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.atime_var)).grid(row=2, column=2, padx=(0, 10))
        
        meta_frame.columnconfigure(1, weight=1)
        
        # 3. Action Control Frame
        action_frame = ttk.Frame(self, padding=10)
        action_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Save button is reactively disabled by default
        self.save_btn = ttk.Button(action_frame, text="Forge Timestamps", command=self.save_metadata, state=tk.DISABLED)
        self.save_btn.pack(side=tk.RIGHT)
        
    def browse_file(self):
        """Opens file dialog and loads existing metadata for the selected file."""
        path = filedialog.askopenfilename(title="Select Target File")
        if path:
            self.file_path.set(path)
            self.load_metadata(path)
            # Enable save button once a valid file path is resolved
            self.save_btn.config(state=tk.NORMAL)
            
    def load_metadata(self, path):
        """Extracts existing OS-level timestamps and formats them into plaintext."""
        try:
            stat = os.stat(path)
            # Format extracted timestamps
            dt_format = "%Y-%m-%d %H-%M-%S"
            self.ctime_var.set(datetime.datetime.fromtimestamp(stat.st_ctime).strftime(dt_format))
            self.mtime_var.set(datetime.datetime.fromtimestamp(stat.st_mtime).strftime(dt_format))
            self.atime_var.set(datetime.datetime.fromtimestamp(stat.st_atime).strftime(dt_format))
        except Exception as e:
            messagebox.showerror("Metadata Extraction Error", f"Failed to read file metadata:\n{e}")
            self.save_btn.config(state=tk.DISABLED)
            
    def pick_date_time(self, var):
        """Opens date picker first, and upon date selection, immediately opens time picker."""
        current_str = var.get()
        current_date = None
        current_time = None
        
        try:
            dt = datetime.datetime.strptime(current_str, "%Y-%m-%d %H-%M-%S")
            current_date = dt.date()
            current_time = dt.time()
        except ValueError:
            pass
            
        def on_date_selected(date_obj):
            def on_time_selected(time_obj):
                var.set(f"{date_obj.strftime('%Y-%m-%d')} {time_obj.strftime('%H-%M-%S')}")
            TimePicker(self.root_window, initial_time=current_time, on_time_selected=on_time_selected)
            
        DatePicker(self.root_window, initial_date=current_date, on_date_selected=on_date_selected)
        
    def save_metadata(self):
        """Parses UI timestamps and writes them directly back to the OS file handle."""
        path = self.file_path.get()
        if not path:
            return
            
        dt_format = "%Y-%m-%d %H-%M-%S"
        
        # Strict Error Isolation & Input Validation
        try:
            c_dt = datetime.datetime.strptime(self.ctime_var.get(), dt_format)
            m_dt = datetime.datetime.strptime(self.mtime_var.get(), dt_format)
            a_dt = datetime.datetime.strptime(self.atime_var.get(), dt_format)
        except ValueError:
            messagebox.showerror(
                "Invalid Metadata Syntax",
                f"Date input format is invalid.\n\nExpected Syntax: YYYY-MM-DD HH-MM-SS\nExample: 2024-01-01 12-00-00"
            )
            return

        try:
            set_file_timestamps(path, c_dt, m_dt, a_dt)
            messagebox.showinfo("Operation Successful", "File timestamps have been successfully forged.")
        except OSError as e:
            messagebox.showerror(
                "Kernel Hook Error", 
                f"Failed to acquire file handle or set file time.\nError Code: {e.errno}\nCheck if the file is locked by another process."
            )
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
