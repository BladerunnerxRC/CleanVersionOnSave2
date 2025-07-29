import adsk.core, adsk.fusion, traceback
from ..settings import load, featureEnabled, customVersionText

class SettingsCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        ui     = adsk.core.Application.get().userInterface
        cmd    = args.command
        inputs = cmd.commandInputs

        # Reload from disk in case it changed
        cfg = load()

        # Checkbox
        inputs.addBoolValueInput(
            'chkEnableClean',
            'Remove version numbers on save',
            True,
            '',
            cfg['featureEnabled']
        )

        # Text field (7-char max)
        inputs.addStringValueInput(
            'txtCustomVer',
            'Custom version text (max 7 chars)',
            cfg['customVersionText']
        )

        # Input-changed handler to enforce 7 chars
        class InputChanged(adsk.core.InputChangedEventHandler):
            def notify(self, args):
                inp = args.input
                if inp.id == 'txtCustomVer' and len(inp.value or '') > 7:
                    ui.messageBox('Max 7 characters')
                    inp.value = inp.value[:7]

        onChange = InputChanged()
        cmd.inputChanged.add(onChange)
        args.firingEvent.add(onChange)

        # Execute handler to write back to settings.json
        class OnExecute(adsk.core.CommandEventHandler):
            def notify(self, args):
                inputs = args.command.commandInputs
                from ..settings import save, featureEnabled, customVersionText

                featureEnabled    = inputs.itemById('chkEnableClean').value
                customVersionText = inputs.itemById('txtCustomVer').value
                save()

                ui.messageBox(
                    f'Settings saved:\n'
                    f' • Remove versions: {featureEnabled}\n'
                    f' • Custom text: "{customVersionText}"'
                )

        onExec = OnExecute()
        cmd.execute.add(onExec)
        args.firingEvent.add(onExec)