import datetime
import calendar
import tkinter as tk
from tkinter import ttk

def center_toplevel(window, parent, width, height):
    """Centers the toplevel window relative to its parent window or fallback to screen center."""
    window.withdraw()
    window.update_idletasks()
    if parent and parent.winfo_ismapped():
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2
    else:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.deiconify()

class DatePicker(tk.Toplevel):
    """A native Tkinter Date Picker utility built using the built-in calendar module."""
    def __init__(self, parent, initial_date=None, on_date_selected=None):
        super().__init__(parent)
        self.title("Select Date")
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
        center_toplevel(self, parent, 260, 220)
        
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
        center_toplevel(self, parent, 200, 120)
        
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
