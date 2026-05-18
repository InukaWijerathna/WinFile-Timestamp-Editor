import os
import datetime
import random
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
        self.batch_ctime_end_var = tk.StringVar()
        self.batch_ctime_rand_var = tk.BooleanVar(value=False)
        
        self.batch_mtime_var = tk.StringVar()
        self.batch_mtime_end_var = tk.StringVar()
        self.batch_mtime_rand_var = tk.BooleanVar(value=False)
        
        self.batch_atime_var = tk.StringVar()
        self.batch_atime_end_var = tk.StringVar()
        self.batch_atime_rand_var = tk.BooleanVar(value=False)
        
        self.build_ui()
        
    def build_ui(self):
        # 3. Action Control Frame (Packed at the absolute bottom first to guarantee visibility)
        action_frame = ttk.Frame(self, padding=10)
        action_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=5)
        
        self.batch_save_btn = ttk.Button(action_frame, text="Forge Batch Timestamps", command=self.save_batch_metadata, state=tk.DISABLED)
        self.batch_save_btn.pack(side=tk.RIGHT)

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
        ttk.Label(meta_frame, text="Creation Time:").grid(row=0, column=0, sticky=tk.W, pady=(8, 2))
        self.ctime_start_entry = ttk.Entry(meta_frame, textvariable=self.batch_ctime_var, width=30)
        self.ctime_start_entry.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=(8, 2))
        self.ctime_start_btn = ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.batch_ctime_var))
        self.ctime_start_btn.grid(row=0, column=2, padx=(0, 10), pady=(8, 2))
        
        self.ctime_rand_chk = ttk.Checkbutton(meta_frame, text="Randomize within range", variable=self.batch_ctime_rand_var, command=self.toggle_ctime_fields)
        self.ctime_rand_chk.grid(row=1, column=0, sticky=tk.W, padx=(5, 5), pady=(2, 8))
        self.ctime_end_entry = ttk.Entry(meta_frame, textvariable=self.batch_ctime_end_var, width=30)
        self.ctime_end_entry.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=(2, 8))
        self.ctime_end_btn = ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.batch_ctime_end_var))
        self.ctime_end_btn.grid(row=1, column=2, padx=(0, 10), pady=(2, 8))
        
        # Modified Time (mtime)
        ttk.Label(meta_frame, text="Modified Time:").grid(row=2, column=0, sticky=tk.W, pady=(8, 2))
        self.mtime_start_entry = ttk.Entry(meta_frame, textvariable=self.batch_mtime_var, width=30)
        self.mtime_start_entry.grid(row=2, column=1, sticky=tk.EW, padx=10, pady=(8, 2))
        self.mtime_start_btn = ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.batch_mtime_var))
        self.mtime_start_btn.grid(row=2, column=2, padx=(0, 10), pady=(8, 2))
        
        self.mtime_rand_chk = ttk.Checkbutton(meta_frame, text="Randomize within range", variable=self.batch_mtime_rand_var, command=self.toggle_mtime_fields)
        self.mtime_rand_chk.grid(row=3, column=0, sticky=tk.W, padx=(5, 5), pady=(2, 8))
        self.mtime_end_entry = ttk.Entry(meta_frame, textvariable=self.batch_mtime_end_var, width=30)
        self.mtime_end_entry.grid(row=3, column=1, sticky=tk.EW, padx=10, pady=(2, 8))
        self.mtime_end_btn = ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.batch_mtime_end_var))
        self.mtime_end_btn.grid(row=3, column=2, padx=(0, 10), pady=(2, 8))
        
        # Accessed Time (atime)
        ttk.Label(meta_frame, text="Accessed Time:").grid(row=4, column=0, sticky=tk.W, pady=(8, 2))
        self.atime_start_entry = ttk.Entry(meta_frame, textvariable=self.batch_atime_var, width=30)
        self.atime_start_entry.grid(row=4, column=1, sticky=tk.EW, padx=10, pady=(8, 2))
        self.atime_start_btn = ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.batch_atime_var))
        self.atime_start_btn.grid(row=4, column=2, padx=(0, 10), pady=(8, 2))
        
        self.atime_rand_chk = ttk.Checkbutton(meta_frame, text="Randomize within range", variable=self.batch_atime_rand_var, command=self.toggle_atime_fields)
        self.atime_rand_chk.grid(row=5, column=0, sticky=tk.W, padx=(5, 5), pady=(2, 8))
        self.atime_end_entry = ttk.Entry(meta_frame, textvariable=self.batch_atime_end_var, width=30)
        self.atime_end_entry.grid(row=5, column=1, sticky=tk.EW, padx=10, pady=(2, 8))
        self.atime_end_btn = ttk.Button(meta_frame, text="📅 Edit...", command=lambda: self.pick_date_time(self.batch_atime_end_var))
        self.atime_end_btn.grid(row=5, column=2, padx=(0, 10), pady=(2, 8))
        
        meta_frame.columnconfigure(1, weight=1)
        
        # Initialize disabled state for end datetime pickers
        self.toggle_ctime_fields()
        self.toggle_mtime_fields()
        self.toggle_atime_fields()
        
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
            
    def toggle_ctime_fields(self):
        is_rand = self.batch_ctime_rand_var.get()
        state = tk.NORMAL if is_rand else tk.DISABLED
        self.ctime_end_entry.config(state=state)
        self.ctime_end_btn.config(state=state)
        if is_rand and not self.batch_ctime_end_var.get():
            self.batch_ctime_end_var.set(self.batch_ctime_var.get())

    def toggle_mtime_fields(self):
        is_rand = self.batch_mtime_rand_var.get()
        state = tk.NORMAL if is_rand else tk.DISABLED
        self.mtime_end_entry.config(state=state)
        self.mtime_end_btn.config(state=state)
        if is_rand and not self.batch_mtime_end_var.get():
            self.batch_mtime_end_var.set(self.batch_mtime_var.get())

    def toggle_atime_fields(self):
        is_rand = self.batch_atime_rand_var.get()
        state = tk.NORMAL if is_rand else tk.DISABLED
        self.atime_end_entry.config(state=state)
        self.atime_end_btn.config(state=state)
        if is_rand and not self.batch_atime_end_var.get():
            self.batch_atime_end_var.set(self.batch_atime_var.get())

    def load_metadata(self, path):
        """Extracts existing OS-level timestamps for a batch file and formats them into plaintext."""
        try:
            stat = os.stat(path)
            dt_format = "%Y-%m-%d %H-%M-%S"
            self.batch_ctime_var.set(datetime.datetime.fromtimestamp(stat.st_ctime).strftime(dt_format))
            self.batch_mtime_var.set(datetime.datetime.fromtimestamp(stat.st_mtime).strftime(dt_format))
            self.batch_atime_var.set(datetime.datetime.fromtimestamp(stat.st_atime).strftime(dt_format))
            
            # Populate the end variables too, if they are empty
            if not self.batch_ctime_end_var.get():
                self.batch_ctime_end_var.set(self.batch_ctime_var.get())
            if not self.batch_mtime_end_var.get():
                self.batch_mtime_end_var.set(self.batch_mtime_var.get())
            if not self.batch_atime_end_var.get():
                self.batch_atime_end_var.set(self.batch_atime_var.get())
        except Exception as e:
            messagebox.showerror("Metadata Extraction Error", f"Failed to read file metadata:\n{e}")
            
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
        
    def save_batch_metadata(self):
        """Parses UI timestamps and writes them directly back to the OS file handles for all batch files."""
        if not self.batch_file_paths:
            return
            
        dt_format = "%Y-%m-%d %H-%M-%S"
        
        # 1. Parse and Validate all active inputs first
        try:
            # Creation Time parsing
            c_dt_start = datetime.datetime.strptime(self.batch_ctime_var.get(), dt_format)
            if self.batch_ctime_rand_var.get():
                c_dt_end = datetime.datetime.strptime(self.batch_ctime_end_var.get(), dt_format)
                if c_dt_start > c_dt_end:
                    c_dt_start, c_dt_end = c_dt_end, c_dt_start
            else:
                c_dt_end = c_dt_start
                
            # Modified Time parsing
            m_dt_start = datetime.datetime.strptime(self.batch_mtime_var.get(), dt_format)
            if self.batch_mtime_rand_var.get():
                m_dt_end = datetime.datetime.strptime(self.batch_mtime_end_var.get(), dt_format)
                if m_dt_start > m_dt_end:
                    m_dt_start, m_dt_end = m_dt_end, m_dt_start
            else:
                m_dt_end = m_dt_start
                
            # Accessed Time parsing
            a_dt_start = datetime.datetime.strptime(self.batch_atime_var.get(), dt_format)
            if self.batch_atime_rand_var.get():
                a_dt_end = datetime.datetime.strptime(self.batch_atime_end_var.get(), dt_format)
                if a_dt_start > a_dt_end:
                    a_dt_start, a_dt_end = a_dt_end, a_dt_start
            else:
                a_dt_end = a_dt_start
                
        except ValueError:
            messagebox.showerror(
                "Invalid Metadata Syntax",
                f"Date input format is invalid.\n\nExpected Syntax: YYYY-MM-DD HH-MM-SS\nExample: 2024-01-01 12-00-00"
            )
            return

        success_count = 0
        fail_count = 0
        
        # 2. Iterate and apply timestamps, generating random timestamps if requested
        for path in self.batch_file_paths:
            try:
                # Resolve Creation Time
                if self.batch_ctime_rand_var.get():
                    c_ts = random.uniform(c_dt_start.timestamp(), c_dt_end.timestamp())
                    c_dt = datetime.datetime.fromtimestamp(c_ts)
                else:
                    c_dt = c_dt_start
                    
                # Resolve Modified Time
                if self.batch_mtime_rand_var.get():
                    m_ts = random.uniform(m_dt_start.timestamp(), m_dt_end.timestamp())
                    m_dt = datetime.datetime.fromtimestamp(m_ts)
                else:
                    m_dt = m_dt_start
                    
                # Resolve Accessed Time
                if self.batch_atime_rand_var.get():
                    a_ts = random.uniform(a_dt_start.timestamp(), a_dt_end.timestamp())
                    a_dt = datetime.datetime.fromtimestamp(a_ts)
                else:
                    a_dt = a_dt_start
                    
                set_file_timestamps(path, c_dt, m_dt, a_dt)
                success_count += 1
            except Exception:
                fail_count += 1
                
        if fail_count == 0:
            messagebox.showinfo("Operation Successful", f"Successfully forged timestamps for {success_count} files.")
        else:
            messagebox.showwarning("Operation Partially Successful", f"Forged timestamps for {success_count} files.\nFailed for {fail_count} files.")
