import adsk.core, adsk.fusion, os, json

# Path to user settings
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'config.json')

# Default settings
DEFAULTS = {
    'allowedCharsRegex': r'^[\w\-\s]+$',
    'maxNameLength': 64,
    'loggingEnabled': True,
    'syncIntervalSec': 300,
    'exportFormats': ['STEP', 'IGES', 'DXF']
}

def load_settings():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except:
        return DEFAULTS.copy()

def save_settings(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(cfg, f, indent=2)

def show_settings_palette():
    app = adsk.core.Application.get()
    ui  = app.userInterface
    pal = ui.palettes.itemById('CleanVersionSettings')
    if pal:
        pal.isVisible = True
        return

    # Create the palette
    pal = ui.palettes.add('CleanVersionSettings',
                          'Settings',
                          'resources/palette/settings.html',
                          True, True, True, 300, 400)
    pal.dockingState = adsk.core.PaletteDockStates.PaletteDockStateRight
