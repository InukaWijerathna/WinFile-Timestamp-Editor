import os
import datetime
import calendar
import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# --- Win32 API Constants and Flags ---
# Used for CreateFileW access rights and sharing modes
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x80

# Win32 INVALID_HANDLE_VALUE constant for error checking
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

# --- Win32 FILETIME Structure ---
class FILETIME(ctypes.Structure):
    """
    Contains a 64-bit value representing the number of 100-nanosecond intervals 
    since January 1, 1601 (UTC).
    """
    _fields_ = [
        ("dwLowDateTime", wintypes.DWORD),
        ("dwHighDateTime", wintypes.DWORD)
    ]

# Bind to kernel32.dll natively via ctypes
kernel32 = ctypes.windll.kernel32

# Function prototypes for robust ctypes calling with strict argument types
kernel32.CreateFileW.restype = wintypes.HANDLE
kernel32.CreateFileW.argtypes = [
    wintypes.LPCWSTR,      # lpFileName
    wintypes.DWORD,        # dwDesiredAccess
    wintypes.DWORD,        # dwShareMode
    ctypes.c_void_p,       # lpSecurityAttributes
    wintypes.DWORD,        # dwCreationDisposition
    wintypes.DWORD,        # dwFlagsAndAttributes
    wintypes.HANDLE        # hTemplateFile
]

kernel32.SetFileTime.restype = wintypes.BOOL
kernel32.SetFileTime.argtypes = [
    wintypes.HANDLE,          # hFile
    ctypes.POINTER(FILETIME), # lpCreationTime
    ctypes.POINTER(FILETIME), # lpLastAccessTime
    ctypes.POINTER(FILETIME)  # lpLastWriteTime
]

kernel32.CloseHandle.restype = wintypes.BOOL
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]

# --- Date/Time Utility Functions ---
# Win32 FILETIME measures 100-nanosecond intervals since January 1, 1601 UTC.
# Unix epoch is January 1, 1970 UTC.
# The Win32 calendar offset in 100-ns intervals between 1601 and 1970 is exactly 116444736000000000.
EPOCH_AS_FILETIME = 116444736000000000
HUNDREDS_OF_NANOSECONDS = 10000000

def dt_to_filetime(dt: datetime.datetime) -> FILETIME:
    """
    Converts a Python datetime object to a Win32 FILETIME structure.
    Utilizes structural byte-shifting to populate the low and high DWORDs.
    """
    # .timestamp() yields seconds since Unix epoch
    timestamp = dt.timestamp()
    
    # Calculate total 100-nanosecond intervals since 1601
    filetime_val = int((timestamp * HUNDREDS_OF_NANOSECONDS) + EPOCH_AS_FILETIME)
    
    ft = FILETIME()
    # Structural byte-shifting logic to divide the 64-bit integer into two 32-bit blocks
    ft.dwLowDateTime = filetime_val & 0xFFFFFFFF  # Mask the lower 32 bits
    ft.dwHighDateTime = filetime_val >> 32        # Shift right 32 bits for the higher DWORD
    
    return ft

class DatePicker(tk.Toplevel):
    """A native Tkinter Date Picker utility built using the built-in calendar module."""
    def __init__(self, parent, initial_date=None, on_date_selected=None):
        super().__init__(parent)
        self.title("Select Date")
        self.geometry("260x220")
        self.resizable(False, False)
        
        # Make the dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.on_date_selected = on_date_selected
        
        if initial_date:
            self.current_year = initial_date.year
            self.current_month = initial_date.month
        else:
            now = datetime.datetime.now()
            self.current_year = now.year
            self.current_month = now.month
            
        self.build_ui()
        
    def build_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(header_frame, text="<", width=3, command=self.prev_month).pack(side=tk.LEFT, padx=10)
        month_name = calendar.month_name[self.current_month]
        ttk.Label(header_frame, text=f"{month_name} {self.current_year}", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, expand=True)
        ttk.Button(header_frame, text=">", width=3, command=self.next_month).pack(side=tk.RIGHT, padx=10)
        
        cal_frame = ttk.Frame(self)
        cal_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            ttk.Label(cal_frame, text=day, font=("Segoe UI", 8, "bold")).grid(row=0, column=i, padx=4, pady=2)
            
        month_cal = calendar.monthcalendar(self.current_year, self.current_month)
        for row, week in enumerate(month_cal):
            for col, day in enumerate(week):
                if day != 0:
                    btn = ttk.Button(cal_frame, text=str(day), width=3, 
                                     command=lambda d=day: self.select_date(d))
                    btn.grid(row=row+1, column=col, padx=2, pady=2)
                    
    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.build_ui()
        
    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.build_ui()
        
    def select_date(self, day):
        if self.on_date_selected:
            self.on_date_selected(datetime.date(self.current_year, self.current_month, day))
        self.destroy()

class TimePicker(tk.Toplevel):
    """A native Tkinter Time Picker utility using Spinboxes."""
    def __init__(self, parent, initial_time=None, on_time_selected=None):
        super().__init__(parent)
        self.title("Select Time")
        self.geometry("200x120")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.on_time_selected = on_time_selected
        
        if initial_time:
            self.current_hour = initial_time.hour
            self.current_minute = initial_time.minute
            self.current_second = initial_time.second
        else:
            now = datetime.datetime.now()
            self.current_hour = now.hour
            self.current_minute = now.minute
            self.current_second = now.second
            
        self.build_ui()
        
    def build_ui(self):
        # Time Selection Frame
        time_frame = ttk.Frame(self, padding=20)
        time_frame.pack(fill=tk.BOTH, expand=True)
        
        # Hour
        self.hour_var = tk.StringVar(value=f"{self.current_hour:02d}")
        ttk.Spinbox(time_frame, from_=0, to=23, textvariable=self.hour_var, width=3, wrap=True).grid(row=0, column=0, padx=2)
        ttk.Label(time_frame, text=":").grid(row=0, column=1)
        
        # Minute
        self.minute_var = tk.StringVar(value=f"{self.current_minute:02d}")
        ttk.Spinbox(time_frame, from_=0, to=59, textvariable=self.minute_var, width=3, wrap=True).grid(row=0, column=2, padx=2)
        ttk.Label(time_frame, text=":").grid(row=0, column=3)
        
        # Second
        self.second_var = tk.StringVar(value=f"{self.current_second:02d}")
        ttk.Spinbox(time_frame, from_=0, to=59, textvariable=self.second_var, width=3, wrap=True).grid(row=0, column=4, padx=2)
        
        # Action Frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Center the confirm button
        btn_frame.columnconfigure(0, weight=1)
        ttk.Button(btn_frame, text="Confirm", command=self.confirm).grid(row=0, column=0)
        
    def confirm(self):
        if self.on_time_selected:
            try:
                h = int(self.hour_var.get())
                m = int(self.minute_var.get())
                s = int(self.second_var.get())
                
                # Boundaries check
                h = max(0, min(23, h))
                m = max(0, min(59, m))
                s = max(0, min(59, s))
                
                self.on_time_selected(datetime.time(h, m, s))
            except ValueError:
                pass
        self.destroy()

class TimestampForgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows File Timestamp Forge")
        self.root.geometry("640x380")
        self.root.resizable(False, False)
        
        # Apply Windows 'vista' theme if available for a clean native look
        style = ttk.Style()
        if 'vista' in style.theme_names():
            style.theme_use('vista')
            
        # Reactive string variables for binding GUI fields
        self.file_path = tk.StringVar()
        self.ctime_var = tk.StringVar()
        self.mtime_var = tk.StringVar()
        self.atime_var = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # 1. Target File Selection Frame
        file_frame = ttk.LabelFrame(self.root, text="Target File Configuration", padding=15)
        file_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Entry(file_frame, textvariable=self.file_path, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).pack(side=tk.RIGHT)
        
        # 2. File Metadata Editor Frame
        meta_frame = ttk.LabelFrame(self.root, text="Low-Level System Metadata (YYYY-MM-DD HH-MM-SS)", padding=15)
        meta_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Creation Time (ctime)
        ttk.Label(meta_frame, text="Creation Time:").grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.ctime_var, width=30).grid(row=0, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅", width=3, command=lambda: self.pick_date(self.ctime_var)).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(meta_frame, text="⏰", width=3, command=lambda: self.pick_time(self.ctime_var)).grid(row=0, column=3, padx=(0, 10))
        
        # Modified Time (mtime)
        ttk.Label(meta_frame, text="Modified Time:").grid(row=1, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.mtime_var, width=30).grid(row=1, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅", width=3, command=lambda: self.pick_date(self.mtime_var)).grid(row=1, column=2, padx=(0, 5))
        ttk.Button(meta_frame, text="⏰", width=3, command=lambda: self.pick_time(self.mtime_var)).grid(row=1, column=3, padx=(0, 10))
        
        # Accessed Time (atime)
        ttk.Label(meta_frame, text="Accessed Time:").grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Entry(meta_frame, textvariable=self.atime_var, width=30).grid(row=2, column=1, sticky=tk.EW, padx=15, pady=8)
        ttk.Button(meta_frame, text="📅", width=3, command=lambda: self.pick_date(self.atime_var)).grid(row=2, column=2, padx=(0, 5))
        ttk.Button(meta_frame, text="⏰", width=3, command=lambda: self.pick_time(self.atime_var)).grid(row=2, column=3, padx=(0, 10))
        
        meta_frame.columnconfigure(1, weight=1)
        
        # 3. Action Control Frame
        action_frame = ttk.Frame(self.root, padding=10)
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

    def pick_date(self, var):
        """Opens the date picker dialog and updates the variable while keeping existing time."""
        current_str = var.get()
        current_date = None
        current_time_str = "00-00-00"
        
        # Attempt to parse existing value to retain the time component and current date
        try:
            dt = datetime.datetime.strptime(current_str, "%Y-%m-%d %H-%M-%S")
            current_date = dt.date()
            current_time_str = dt.strftime("%H-%M-%S")
        except ValueError:
            pass # Use defaults if format is invalid
            
        def on_date_selected(date_obj):
            var.set(f"{date_obj.strftime('%Y-%m-%d')} {current_time_str}")
            
        DatePicker(self.root, initial_date=current_date, on_date_selected=on_date_selected)

    def pick_time(self, var):
        """Opens the time picker dialog and updates the variable while keeping existing date."""
        current_str = var.get()
        current_time = None
        current_date_str = "1970-01-01"
        
        # Attempt to parse existing value to retain the date component
        try:
            dt = datetime.datetime.strptime(current_str, "%Y-%m-%d %H-%M-%S")
            current_time = dt.time()
            current_date_str = dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
            
        def on_time_selected(time_obj):
            var.set(f"{current_date_str} {time_obj.strftime('%H-%M-%S')}")
            
        TimePicker(self.root, initial_time=current_time, on_time_selected=on_time_selected)

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

        # Convert datetimes to Win32 FILETIME structs
        c_ft = dt_to_filetime(c_dt)
        a_ft = dt_to_filetime(a_dt)
        m_ft = dt_to_filetime(m_dt)

        # Retrieve a Windows kernel write-handle
        handle = kernel32.CreateFileW(
            path,
            GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE, 
            None,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            None
        )
        
        if handle == INVALID_HANDLE_VALUE:
            error_code = ctypes.GetLastError()
            messagebox.showerror(
                "Kernel Hook Error", 
                f"Failed to acquire file handle.\nError Code: {error_code}\nCheck if the file is locked by another process."
            )
            return
            
        try:
            # Inject new metadata via SetFileTime
            success = kernel32.SetFileTime(handle, ctypes.byref(c_ft), ctypes.byref(a_ft), ctypes.byref(m_ft))
            if not success:
                error_code = ctypes.GetLastError()
                messagebox.showerror("Kernel Hook Error", f"SetFileTime operation failed.\nError Code: {error_code}")
            else:
                messagebox.showinfo("Operation Successful", "File timestamps have been successfully forged.")
        finally:
            # Always safely release the handle
            kernel32.CloseHandle(handle)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimestampForgeApp(root)
    root.mainloop()
