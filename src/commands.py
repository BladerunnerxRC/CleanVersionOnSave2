import os
import adsk.core, adsk.fusion
import settings, export_hook

# keep handlers alive
handlers = []

# 1) Settings command
class SettingsCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        cmd    = args.command
        inputs = cmd.commandInputs

        # Checkbox to enable/disable clean-on-save
        inputs.addBoolValueInput(
            'chkEnableClean',
            'Remove version numbers on save',
            True, '', settings.featureEnabled
        )

        # 7-char max custom version text
        inputs.addStringValueInput(
            'txtCustomVer',
            'Custom version text (max 7 chars)',
            settings.customVersionText
        )

        # Enforce length limit as user types
        class InputChanged(adsk.core.InputChangedEventHandler):
            def notify(self, args):
                inp = args.input
                if inp.id == 'txtCustomVer':
                    text = inp.value or ''
                    if len(text) > 7:
                        adsk.core.Application.get().userInterface.messageBox(
                            'Custom version text must be 7 characters or fewer.'
                        )
                        inp.value = text[:7]

        onChanged = InputChanged()
        cmd.inputChanged.add(onChanged)
        handlers.append(onChanged)

        # Save settings when OK clicked
        class OnExecute(adsk.core.CommandEventHandler):
            def notify(self, args):
                inputs               = args.command.commandInputs
                settings.featureEnabled    = inputs.itemById('chkEnableClean').value
                settings.customVersionText = inputs.itemById('txtCustomVer').value
                settings.save()
                adsk.core.Application.get().userInterface.messageBox(
                    f'Settings saved:\n'
                    f' • Remove versions: {settings.featureEnabled}\n'
                    f' • Custom text: "{settings.customVersionText}"'
                )

        onExec = OnExecute()
        cmd.execute.add(onExec)
        handlers.append(onExec)


# 2) Register & clean up commands
def register_commands():
    app = adsk.core.Application.get()
    ui  = app.userInterface
    panel = ui.allToolbarPanels.itemById('SolidCreatePanel')

    # Settings button
    settings_cmd = ui.commandDefinitions.itemById('CleanVerSettings')
    if not settings_cmd:
        settings_cmd = ui.commandDefinitions.addButtonDefinition(
            'CleanVerSettings',
            'CleanVersion Settings',
            'Configure clean-on-save behavior',
            os.path.join(os.path.dirname(__file__), '../resources/icons')
        )
    settings_cmd.commandCreated.add(SettingsCommandCreatedEventHandler())
    handlers.append(SettingsCommandCreatedEventHandler())
    panel.controls.addCommand(settings_cmd)

    # Export button
    export_cmd = ui.commandDefinitions.itemById('cmdExport')
    if not export_cmd:
        export_cmd = ui.commandDefinitions.addButtonDefinition(
            'cmdExport',
            'Export Clean Version',
            'Export STEP with cleaned name',
            os.path.join(os.path.dirname(__file__), '../resources/icons')
        )
    export_cmd.commandCreated.add(export_hook.ExportCommandCreatedEventHandler())
    handlers.append(export_hook.ExportCommandCreatedEventHandler())
    panel.controls.addCommand(export_cmd)


def cleanup_commands():
    app = adsk.core.Application.get()
    ui  = app.userInterface
    panel = ui.allToolbarPanels.itemById('SolidCreatePanel')

    # Helper to remove definition + control
    def remove_command(cmd_id):
        cmd_def = ui.commandDefinitions.itemById(cmd_id)
        if cmd_def:
            ctrl = panel.controls.itemById(cmd_id)
            if ctrl:
                ctrl.deleteMe()
            cmd_def.deleteMe()

    remove_command('CleanVerSettings')
    remove_command('cmdExport')