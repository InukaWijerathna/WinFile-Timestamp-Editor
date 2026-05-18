import os
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from date_time_pickers import DatePicker, TimePicker
from win32_metadata import set_file_timestamps

class BatchEditorTab(ttk.Frame):
    """The Batch File Editor UI tab and logic."""
    def __init__(self, parent, root_window):
        super().__init__(parent)
        self.root_window = root_window
        
        # Reactive string variables for Batch
        self.batch_file_paths = []
        self.batch_ctime_var = tk.StringVar()
        self.batch_mtime_var = tk.StringVar()
        self.batch_atime_var = tk.StringVar()
        
        self.build_ui()
        
    def build_ui(self):
        # 1. Target Files Selection Frame
        files_frame = ttk.LabelFrame(self, text="Target Files Configuration", padding=15)
        files_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.batch_listbox = tk.Listbox(files_frame, selectmode=tk.EXTENDED, height=4)
        self.batch_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        scroll = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.batch_listbox.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.batch_listbox.config(yscrollcommand=scroll.set)
        
        btn_frame = ttk.Frame(files_frame)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(btn_frame, text="Browse...", command=self.browse_batch_files).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(btn_frame, text="Clear", command=self.clear_batch_files).pack(fill=tk.X)
        
        # 2. File Metadata Editor Frame
        meta_frame = ttk.LabelFrame(self, text="Batch Low-Level System Metadata", padding=15)
        meta_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Creation Time (ctime)
        ttk.Label(meta_frame, text="Creation Time:").grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.batch_ctime_var, width=30).grid(row=0, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅", width=3, command=lambda: self.pick_date(self.batch_ctime_var)).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(meta_frame, text="⏰", width=3, command=lambda: self.pick_time(self.batch_ctime_var)).grid(row=0, column=3, padx=(0, 10))
        
        # Modified Time (mtime)
        ttk.Label(meta_frame, text="Modified Time:").grid(row=1, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.batch_mtime_var, width=30).grid(row=1, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅", width=3, command=lambda: self.pick_date(self.batch_mtime_var)).grid(row=1, column=2, padx=(0, 5))
        ttk.Button(meta_frame, text="⏰", width=3, command=lambda: self.pick_time(self.batch_mtime_var)).grid(row=1, column=3, padx=(0, 10))
        
        # Accessed Time (atime)
        ttk.Label(meta_frame, text="Accessed Time:").grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.batch_atime_var, width=30).grid(row=2, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅", width=3, command=lambda: self.pick_date(self.batch_atime_var)).grid(row=2, column=2, padx=(0, 5))
        ttk.Button(meta_frame, text="⏰", width=3, command=lambda: self.pick_time(self.batch_atime_var)).grid(row=2, column=3, padx=(0, 10))
        
        meta_frame.columnconfigure(1, weight=1)
        
        # 3. Action Control Frame
        action_frame = ttk.Frame(self, padding=10)
        action_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.batch_save_btn = ttk.Button(action_frame, text="Forge Batch Timestamps", command=self.save_batch_metadata, state=tk.DISABLED)
        self.batch_save_btn.pack(side=tk.RIGHT)
        
    def browse_batch_files(self):
        """Opens file dialog to select multiple target files."""
        paths = filedialog.askopenfilenames(title="Select Target Files")
        if paths:
            self.batch_file_paths.extend(paths)
            self.update_batch_listbox()
            if not self.batch_ctime_var.get():
                self.load_metadata(paths[0])
            self.batch_save_btn.config(state=tk.NORMAL)
            
    def clear_batch_files(self):
        self.batch_file_paths.clear()
        self.update_batch_listbox()
        self.batch_save_btn.config(state=tk.DISABLED)
        
    def update_batch_listbox(self):
        self.batch_listbox.delete(0, tk.END)
        for p in self.batch_file_paths:
            self.batch_listbox.insert(tk.END, p)
            
    def load_metadata(self, path):
        """Extracts existing OS-level timestamps for a batch file and formats them into plaintext."""
        try:
            stat = os.stat(path)
            dt_format = "%Y-%m-%d %H-%M-%S"
            self.batch_ctime_var.set(datetime.datetime.fromtimestamp(stat.st_ctime).strftime(dt_format))
            self.batch_mtime_var.set(datetime.datetime.fromtimestamp(stat.st_mtime).strftime(dt_format))
            self.batch_atime_var.set(datetime.datetime.fromtimestamp(stat.st_atime).strftime(dt_format))
        except Exception as e:
            messagebox.showerror("Metadata Extraction Error", f"Failed to read file metadata:\n{e}")
            
    def pick_date(self, var):
        """Opens the date picker dialog and updates the variable while keeping existing time."""
        current_str = var.get()
        current_date = None
        current_time_str = "00-00-00"
        
        try:
            dt = datetime.datetime.strptime(current_str, "%Y-%m-%d %H-%M-%S")
            current_date = dt.date()
            current_time_str = dt.strftime("%H-%M-%S")
        except ValueError:
            pass # Use defaults if format is invalid
            
        def on_date_selected(date_obj):
            var.set(f"{date_obj.strftime('%Y-%m-%d')} {current_time_str}")
            
        DatePicker(self.root_window, initial_date=current_date, on_date_selected=on_date_selected)
        
    def pick_time(self, var):
        """Opens the time picker dialog and updates the variable while keeping existing date."""
        current_str = var.get()
        current_time = None
        current_date_str = "1970-01-01"
        
        try:
            dt = datetime.datetime.strptime(current_str, "%Y-%m-%d %H-%M-%S")
            current_time = dt.time()
            current_date_str = dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
            
        def on_time_selected(time_obj):
            var.set(f"{current_date_str} {time_obj.strftime('%H-%M-%S')}")
            
        TimePicker(self.root_window, initial_time=current_time, on_time_selected=on_time_selected)
        
    def save_batch_metadata(self):
        """Parses UI timestamps and writes them directly back to the OS file handles for all batch files."""
        if not self.batch_file_paths:
            return
            
        dt_format = "%Y-%m-%d %H-%M-%S"
        
        try:
            c_dt = datetime.datetime.strptime(self.batch_ctime_var.get(), dt_format)
            m_dt = datetime.datetime.strptime(self.batch_mtime_var.get(), dt_format)
            a_dt = datetime.datetime.strptime(self.batch_atime_var.get(), dt_format)
        except ValueError:
            messagebox.showerror(
                "Invalid Metadata Syntax",
                f"Date input format is invalid.\n\nExpected Syntax: YYYY-MM-DD HH-MM-SS\nExample: 2024-01-01 12-00-00"
            )
            return

        success_count = 0
        fail_count = 0
        
        for path in self.batch_file_paths:
            try:
                set_file_timestamps(path, c_dt, m_dt, a_dt)
                success_count += 1
            except Exception:
                fail_count += 1
                
        if fail_count == 0:
            messagebox.showinfo("Operation Successful", f"Successfully forged timestamps for {success_count} files.")
        else:
            messagebox.showwarning("Operation Partially Successful", f"Forged timestamps for {success_count} files.\nFailed for {fail_count} files.")
