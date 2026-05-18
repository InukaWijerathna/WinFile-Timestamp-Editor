# WinFile-Timestamp-Editor

A lightweight, native Windows desktop utility designed for system administrators, build-tool verification, and data caching testing. This tool allows users to programmatically view, modify, and update low-level file system metadata properties—specifically **Creation Date (Birthtime)**, **Last Modified Date**, and **Last Accessed Date**—through a clean, responsive graphical user interface.

Unlike high-level software abstractions that restrict developers from modifying core file attributes, this application interfaces directly with the Windows OS kernel layer via the Win32 API.

---

## 🛠️ Technical Architecture & Core Principles

Standard programming libraries usually limit metadata manipulation to the *Accessed* and *Modified* timestamps of a file. Altering the **Creation/Birth Time** requires a deeper dive into platform-specific kernel modules. 

This application utilizes Python's built-in Foreign Function Interface (`ctypes`) to bind the native Windows `kernel32.dll`, allowing it to bypass user-space constraints and interact straight with physical file system allocations:

* **File Descriptor Authorization:** The tool requests low-level write access on the physical file using the `CreateFileW` system call with `GENERIC_WRITE` (0x40000000) authorization flags.
* **Epoch-to-FILETIME Translation:** Standard UNIX epoch timestamps (floats representing seconds since January 1, 1970) are transformed into Windows `FILETIME` structures (64-bit values representing 100-nanosecond intervals since January 1, 1601) via bit-shifting and masking logic.
* **Kernel Execution:** The system invokes `SetFileTime` using memory reference pointers (`ctypes.byref`) to commit the updated timestamps directly into NTFS/FAT32 allocation records before releasing the handle securely with `CloseHandle`.

---

## ✨ Features

* **Zero Dependencies:** Runs natively out of the box using vanilla Python. No bulky external frameworks like PyQt, PySide, or WXPython required.
* **Reactive UI State Management:** The interface automatically keeps the "Forge & Save" actions locked out until a valid, active file path has been resolved through the file browser.
* **Automated Data Binding:** Instantly pulls and formats pre-existing system timestamps (`atime`, `mtime`, `ctime`) into user-friendly `YYYY-MM-DD HH:MM:SS` strings upon file loading.
* **Input Isolation & Exception Handlers:** Safely intercepts parsing errors, locked permissions, or malformed time syntax, handling them inside custom warning frames instead of letting the application execution threads freeze or crash.

---

## 🚀 Setup & Installation

Since the application relies exclusively on Python's built-in standard libraries, installation is instant.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/WinFile-Timestamp-Editor.git](https://github.com/YOUR-USERNAME/WinFile-Timestamp-Editor.git)
   cd WinFile-Timestamp-Editor
