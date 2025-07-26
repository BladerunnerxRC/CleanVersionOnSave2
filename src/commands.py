import os
import adsk.core, adsk.fusion
import settings, export_hook

handlers = []

class SettingsCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        settings.show_settings()

class ExportCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        export_hook.on_export(None)

def register_commands():
    app = adsk.core.Application.get()
    ui = app.userInterface

    # Absolute path to your icons folder
    ICON_FOLDER = os.path.join(os.path.dirname(__file__), 'resources', 'icons')

    # Settings button
    settings_cmd = ui.commandDefinitions.addButtonDefinition(
        'cmdSettings',                   # internal ID
        'CleanVersion Settings',         # displayed name
        'Configure renaming behavior',   # tooltip description
        ICON_FOLDER                      # path to your icons
    )
    settings_handler = SettingsCommandCreatedEventHandler()
    settings_cmd.commandCreated.add(settings_handler)
    handlers.append(settings_handler)

    # Manual export button
    export_cmd = ui.commandDefinitions.addButtonDefinition(
        'cmdExport',                       # internal ID
        'Export Clean Version',            # displayed name
        'Export STEP with cleaned name',   # tooltip description
        ICON_FOLDER                        # path to your icons
    )
    export_handler = ExportCommandCreatedEventHandler()
    export_cmd.commandCreated.add(export_handler)
    handlers.append(export_handler)

    # Add commands to the Solid Create panel
    panel = ui.allToolbarPanels.itemById('SolidCreatePanel')
    panel.controls.addCommand(settings_cmd)
    panel.controls.addCommand(export_cmd)