# Release Notes

All notable changes to the **WinFile-Timestamp-Editor** project will be documented in this file.

---

## [1.1.0] - 2026-05-19

### Changed
* **Asset Organization:** Relocated the application icon (`logo.ico`) to a dedicated `src/assets/` directory to clean up the root `src` namespace.
* **Icon Path Resolution:** Updated `gui_app.py` to correctly resolve the new nested assets path dynamically.
* **Process Identification:** Updated the low-level Windows process registration (`AppUserModelID`) to version `1.1` to ensure correct OS-level taskbar grouping.
* **UI Layout:** Restored clean title bar name (`Timestamp-Editor`) and added a subtly integrated `version 1.1` string in the application footer.

---

## [1.0.0] - 2026-05-18

### Added
* **Direct NTFS Kernel Manipulation:** Implemented direct system calls to the Windows OS kernel via `ctypes` (`CreateFileW`, `SetFileTime`, `CloseHandle`) to bypass high-level runtime timestamp restrictions (enabling Birthtime/Creation Time modification).
* **Responsive GUI:** Modularized Tkinter structure with two main tabs:
  * **Single File Editor:** Quick metadata viewing and editing for individual files.
  * **Batch File Editor:** Multi-file support with bulk timestamp updates and randomized range spreads.
* **DateTime Pickers:** Custom native-feeling dialog overlays with micro-animations for picking unified dates and time (HMS precision).
* **Dynamic Centering:** Added high-DPI aware window centering logic to prevent picker coordinate drift.
* **Branding:** Integrated high-quality native taskbar grouping using `logo.ico`.
