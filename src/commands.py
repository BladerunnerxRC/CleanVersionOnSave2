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

    # Settings button
    settings_cmd = ui.commandDefinitions.addButtonDefinition(
        'cmdSettings',
        'CleanVersion Settings',
        'Configure renaming behavior'
    )
    settings_handler = SettingsCommandCreatedEventHandler()
    settings_cmd.commandCreated.add(settings_handler)
    handlers.append(settings_handler)

    # Manual export button
    export_cmd = ui.commandDefinitions.addButtonDefinition(
        'cmdExport',
        'Export Clean Version',
        'Export STEP with cleaned name'
    )
    export_handler = ExportCommandCreatedEventHandler()
    export_cmd.commandCreated.add(export_handler)
    handlers.append(export_handler)

    # Add to toolbar panel
    panel = ui.allToolbarPanels.itemById('FusionSolidCreatePanel')
    panel.controls.addCommand(settings_cmd)
    panel.controls.addCommand(export_cmd)
