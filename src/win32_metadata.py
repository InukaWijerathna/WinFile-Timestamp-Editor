import os
import datetime
import ctypes
from ctypes import wintypes

# --- Win32 API Constants and Flags ---
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x80
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

# --- Date/Time Utility Constants ---
EPOCH_AS_FILETIME = 116444736000000000
HUNDREDS_OF_NANOSECONDS = 10000000

def dt_to_filetime(dt: datetime.datetime) -> FILETIME:
    """
    Converts a Python datetime object to a Win32 FILETIME structure.
    Utilizes structural byte-shifting to populate the low and high DWORDs.
    """
    timestamp = dt.timestamp()
    
    # Calculate total 100-nanosecond intervals since 1601
    filetime_val = int((timestamp * HUNDREDS_OF_NANOSECONDS) + EPOCH_AS_FILETIME)
    
    ft = FILETIME()
    ft.dwLowDateTime = filetime_val & 0xFFFFFFFF  # Mask the lower 32 bits
    ft.dwHighDateTime = filetime_val >> 32        # Shift right 32 bits for the higher DWORD
    
    return ft

def set_file_timestamps(path: str, ctime: datetime.datetime, mtime: datetime.datetime, atime: datetime.datetime) -> bool:
    """
    Retrieves a Windows kernel write-handle and updates low-level file timestamps.
    Raises OSError if kernel operation fails.
    """
    c_ft = dt_to_filetime(ctime)
    a_ft = dt_to_filetime(atime)
    m_ft = dt_to_filetime(mtime)

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
        raise OSError(error_code, f"Failed to acquire file handle. Windows Error Code: {error_code}")
        
    try:
        success = kernel32.SetFileTime(handle, ctypes.byref(c_ft), ctypes.byref(a_ft), ctypes.byref(m_ft))
        if not success:
            error_code = ctypes.GetLastError()
            raise OSError(error_code, f"SetFileTime operation failed. Windows Error Code: {error_code}")
        return True
    finally:
        kernel32.CloseHandle(handle)
