# Known Issues & Troubleshooting

This document lists known limitations, platform dependencies, common issues, and troubleshooting steps for the **WinFile-Timestamp-Editor**.

---

## 🚨 Essential Platform Requirement

> [!IMPORTANT]
> **Windows OS is Mandatory**  
> This application communicates directly with the Windows kernel via the Win32 API using `ctypes` (specifically `kernel32.dll`). It **cannot** run on macOS, Linux, or WSL (Windows Subsystem for Linux) unless executed within a fully native Windows environment.

---

## 🔍 Common Issues & Resolutions

### 1. `PermissionError` or Failure to Forge Timestamps
* **Symptom:** The program displays an error or fails to update metadata when you click "Forge Timestamps".
* **Reason:** The file might be write-protected, located in a system directory (e.g., `C:\Windows` or `C:\Program Files`), or currently open and locked by another application.
* **Resolution:**
  1. Ensure the file is not open in another program.
  2. Run the Command Prompt or terminal as **Administrator** before executing the tool:
     ```powershell
     python src/gui_app.py
     ```
  3. Verify that your user account has write permissions for the parent folder.

### 2. Low-Level Timestamp Resolution Discrepancies
* **Symptom:** Forged timestamps appear slightly rounded or differ slightly on non-NTFS volumes.
* **Reason:** This tool operates on the **NTFS** file system specification which supports 100-nanosecond intervals. Older formats like **FAT32** have strict limits:
  * **Creation Time:** 10-millisecond resolution.
  * **Write/Modified Time:** 2-second resolution.
  * **Access Time:** 1-day resolution.
* **Resolution:** Run the tool on files stored on modern NTFS or exFAT formatted drives for full resolution precision.

### 3. File Timestamp Out-of-Bounds
* **Symptom:** Setting extremely old dates (e.g., prior to 1601) results in system errors.
* **Reason:** Windows standard `FILETIME` structures represent the number of 100-nanosecond intervals since **January 1, 1601**. Dates before this boundary are physically unsupported by the NTFS file system.
* **Resolution:** Ensure all input dates are at or after `1601-01-01 00:00:00`.

---

## 🛠️ How to Report a New Issue

If you encounter an unlisted bug or unexpected behavior, please prepare a report with the following details:
1. **Operating System:** Exact Windows version (e.g., Windows 11 Home 23H2).
2. **Environment:** Python version (e.g., Python 3.11.2).
3. **Execution Context:** Standard User vs. Run as Administrator.
4. **Target File Details:** File extension (e.g., `.txt`, `.exe`) and file system type (NTFS / exFAT / FAT32).
5. **Console Output / Logs:** Any traceback printed in the terminal or error message popups.
