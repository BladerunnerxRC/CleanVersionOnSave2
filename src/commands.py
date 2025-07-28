import os
import adsk.core, adsk.fusion
import settings, export_hook

handlers = []

class SettingsCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        cmd    = args.command
        inputs = cmd.commandInputs
        ui     = adsk.core.Application.get().userInterface

        # 1) Checkbox: enable / disable clean-on-save
        inputs.addBoolValueInput(
            'chkEnableClean',
            'Remove version numbers on save',
            True,
            '',
            settings.featureEnabled
        )

        # 2) String input: custom version text (max 7 chars)
        inputs.addStringValueInput(
            'txtCustomVer',
            'Custom version text (max 7 chars)',
            settings.customVersionText
        )

        # 3) Enforce 7-char limit as user types
        inputChanged = SettingsInputChangedHandler()
        cmd.inputChanged.add(inputChanged)
        handlers.append(inputChanged)

        # 4) Save settings when user clicks OK
        onExecute = SettingsCommandExecuteHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)

class SettingsInputChangedHandler(adsk.core.InputChangedEventHandler):
    def notify(self, args):
        inp = args.input
        if inp.id == 'txtCustomVer':
            text = inp.value or ''
            if len(text) > 7:
                adsk.core.Application.get().userInterface.messageBox(
                    'Custom version text must be 7 characters or fewer.'
                )
                inp.value = text[:7]

class SettingsCommandExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        global handlers
        inputs               = args.command.commandInputs
        settings.featureEnabled    = inputs.itemById('chkEnableClean').value
        settings.customVersionText = inputs.itemById('txtCustomVer').value
        settings.save()  # writes out to config.json

        adsk.core.Application.get().userInterface.messageBox(
            f'Settings saved:\n'
            f' • Remove versions on save: {settings.featureEnabled}\n'
            f' • Custom text: "{settings.customVersionText}"'
        )

def register_commands():
    app = adsk.core.Application.get()
    ui  = app.userInterface

    # === SETTINGS BUTTON ===
    settings_cmd = ui.commandDefinitions.itemById('CleanVerSettings')
    if not settings_cmd:
        settings_cmd = ui.commandDefinitions.addButtonDefinition(
            'CleanVerSettings',
            'CleanVersion Settings',
            'Configure clean-on-save behavior',
            os.path.join(os.path.dirname(__file__), '../resources/icons')
        )

    onSettingsCreated = SettingsCommandCreatedEventHandler()
    settings_cmd.commandCreated.add(onSettingsCreated)
    handlers.append(onSettingsCreated)

    # Place it in the Solid Create panel
    panel = ui.allToolbarPanels.itemById('SolidCreatePanel')
    panel.controls.addCommand(settings_cmd)

    # === EXPORT BUTTON (unchanged) ===
    export_cmd = ui.commandDefinitions.itemById('cmdExport')
    if not export_cmd:
        export_cmd = ui.commandDefinitions.addButtonDefinition(
            'cmdExport',
            'Export Clean Version',
            'Export STEP with cleaned name',
            os.path.join(os.path.dirname(__file__), '../resources/icons')
        )

    onExportCreated = export_hook.ExportCommandCreatedEventHandler()
    export_cmd.commandCreated.add(onExportCreated)
    handlers.append(onExportCreated)

    panel.controls.addCommand(export_cmd)