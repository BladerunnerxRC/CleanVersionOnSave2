# CleanVersionOnSave2

A Fusion 360 Add-In that enforces clean filenames on save & export, logs changes, and syncs externally.

## Features

- Auto-rename documents by stripping trailing version tags  
- Log every rename with timestamp, old/new names  
- Validate filenames against custom rules  
- Export to multiple formats (STEP, IGES, DXF)  
- Configurable via a docked settings palette  
- Sync rename history to your REST API or Google Sheets  
- Version bumping (SemVer or timestamp)  

## Installation

1. Clone this repo into your Fusion 360 Add-Ins folder:  
   `~/Autodesk/Fusion 360/API/AddIns/CleanVersionOnSave2`  
2. Place icons in `resources/icons/`:  
   - `icon16.png`, `icon32.png`, `icon128.png`  
3. Launch Fusion 360. Enable the Add-In under **Scripts and Add-Ins**.

## Usage

- **Auto-save hook** runs on every Document Save  
- **Manual export**: Toolbar buttons “CleanVersion Settings” & “Export Clean Version”  
- **Settings**: click the palette icon to open configuration UI  

## Configuration

Open **CleanVersion Settings** to:

- Adjust allowed character regex  
- Toggle logging & change log path  
- Set export formats & sync interval  
- Define your `apiEndpoint` and `apiKey` for external sync  

Settings persist in `data/config.json`.

## Contributing

1. Fork & branch  
2. Run tests in CI (`.github/workflows/python-package.yml`)  
3. Submit PR with descriptive changes  

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

