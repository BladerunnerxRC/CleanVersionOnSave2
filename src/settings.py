import adsk.core, adsk.fusion, traceback, os

_handlers = []
_palette = None

def create_settings_command(ui):
    cmdDefs = ui.commandDefinitions
    cmdId = 'CleanVersionSettings'
    cmdName = 'CleanVersion Settings'
    cmdTooltip = 'Configure CleanVersion options'

    # Create the command definition if it doesn't exist
    cmdDef = cmdDefs.itemById(cmdId)
    if not cmdDef:
        icons_folder = os.path.join(os.path.dirname(__file__), 'resources', 'icons')
        cmdDef = cmdDefs.addButtonDefinition(cmdId, cmdName, cmdTooltip, icons_folder)
        # Assign toolbar icons
        cmdDef.resourceFolder      = icons_folder
        cmdDef.smallIconFilename   = os.path.join(icons_folder, 'icon16.png')
        cmdDef.largeIconFilename   = os.path.join(icons_folder, 'icon32.png')

        # Handle command creation
        onCreated = SettingsCreatedHandler()
        cmdDef.commandCreated.add(onCreated)
        _handlers.append(onCreated)

    # Add the button to the Scripts & Add-ins panel
    panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
    panel.controls.addCommand(cmdDef)


class SettingsCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        try:
            cmd = args.command
            onExecute = SettingsExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)
        except:
            ui = adsk.core.Application.get().userInterface
            ui.messageBox(f'Settings command creation failed:\n{traceback.format_exc()}')


class SettingsExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        global _palette
        ui = adsk.core.Application.get().userInterface
        try:
            # If palette exists, just show it
            if _palette:
                _palette.isVisible = True
                return

            # Create and display the HTML palette
            html_path = os.path.join(os.path.dirname(__file__), 'resources', 'settings.html')
            _palette = ui.palettes.add(
                'CleanVersionSettingsPanel',  # unique ID
                'Settings',                   # display name
                html_path, True, True, True, 600, 400
            )

            # Assign your custom icons
            icons_folder = os.path.join(os.path.dirname(__file__), 'resources', 'icons')
            _palette.smallIconFilename = os.path.join(icons_folder, 'icon16.png')
            _palette.largeIconFilename = os.path.join(icons_folder, 'icon32.png')

            # Dock it on the right and show
            _palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight
            _palette.isVisible = True

        except:
            ui.messageBox(f'Failed to show settings palette:\n{traceback.format_exc()}')


def cleanup_settings(ui):
    global _palette

    # Remove the palette
    if _palette:
        _palette.deleteMe()
        _palette = None

    # Remove the command definition
    cmdDef = ui.commandDefinitions.itemById('CleanVersionSettings')
    if cmdDef:
        cmdDef.deleteMe()

    # Clear all event handlers
    _handlers.clear()