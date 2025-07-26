# CleanVersionOnSave2

A Fusion 360 Add-In that enforces clean filenames on save & export, logs changes, and syncs externally.

---

## Overview

**CleanVersionOnSave2** automates the process of maintaining clean and standardized file names within Fusion 360. By hooking into document save and export events, this add-in ensures your filenames are consistent, versioned, and compliant with custom rules. It also logs every change, supports multiple export formats, and can synchronize filename changes to external systems such as REST APIs or Google Sheets.

---

## Features

- **Auto-Rename on Save/Export:**  
  Automatically removes trailing version tags and enforces clean, standard file names.

- **Comprehensive Logging:**  
  Every rename action is logged with a timestamp, including both the old and new names.

- **Custom Filename Validation:**  
  Enforces user-defined filename rules (via regex).

- **Multi-Format Export:**  
  Supports exporting files in STEP, IGES, and DXF formats.

- **Configurable UI:**  
  Provides a docked settings palette for easy configuration inside Fusion 360.

- **External Sync:**  
  Optionally syncs rename history to external APIs or Google Sheets.

- **Version Bumping:**  
  Supports semantic or timestamp-based versioning.

- **Persistent Settings:**  
  All configuration is saved in `data/config.json` for consistency.

---

## Installation

1. Clone or download this repository to your Fusion 360 Add-Ins directory:  
   `~/Autodesk/Fusion 360/API/AddIns/CleanVersionOnSave2`
2. Place your icons in `resources/icons/` as:  
   - `icon16.png`, `icon32.png`, `icon128.png`
3. Launch Fusion 360, open **Scripts and Add-Ins**, and enable **CleanVersionOnSave2**.

---

## Usage

- The add-in automatically processes filenames on every save and export.
- Toolbar buttons and a settings palette allow for manual controls or configuration.
- Change filename rules, export formats, and sync settings via the settings palette.

---

## Configuration

- Adjust allowed character regex for filenames.
- Set log file locations and enable/disable logging.
- Choose export formats and sync options.
- Define your `apiEndpoint` and `apiKey` for REST or Google Sheets integration.
- All settings persist in `data/config.json`.

---

## Contributing

1. Fork the repository and create a new branch for your feature or bugfix.
2. Run and test your changes.
3. Submit a pull request with a clear description of your changes.

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---