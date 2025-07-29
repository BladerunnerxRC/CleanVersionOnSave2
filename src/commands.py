# src/commands.py

import os
import adsk.core, adsk.fusion, traceback

# Module‐level lists to track everything so we can clean up
_command_defs     = []
_command_handlers = []
_command_controls = []

# The two commands we want in the SOLID → Scripts & Add-Ins panel
_COMMANDS = [
    dict(
        id='CV_SettingsCmd',
        name='CV Settings',
        tooltip='Configure CleanVersion settings',
        handlerClassName='SettingsCommandCreatedHandler'
    ),
    dict(
        id='CV_ExportCmd',
        name='Export History',
        tooltip='Export CleanVersion history log',
        handlerClassName='ExportCommandCreatedHandler'
    ),
]

def register_commands():
    """
    Create command definitions, add them to the Fusion UI panel, and
    hook their CommandCreated events.
    """
    app = adsk.core.Application.get()
    ui  = app.userInterface

    # Locate the SOLID → Scripts & Add-Ins panel
    ws    = ui.workspaces.itemById('FusionSolidEnvironment')
    panel = ws.toolbarPanels.itemById('SolidScriptsAddinsPanel')

    # Where to find 16×16 and 32×32 icons
    resource_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'resources', 'icons')
    )

    for cmd in _COMMANDS:
        # 1) Command Definition
        cmd_def = ui.commandDefinitions.itemById(cmd['id'])
        if not cmd_def:
            cmd_def = ui.commandDefinitions.addButtonDefinition(
                cmd['id'],
                cmd['name'],
                cmd['tooltip'],
                resource_folder
            )
        _command_defs.append(cmd_def)

        # 2) Add to panel
        control = panel.controls.addCommand(cmd_def)
        _command_controls.append(control)

        # 3) Hook the creation event
        module_name = f"src.command_handlers.{cmd['handlerClassName']}"
        handler_module = __import__(module_name, fromlist=[cmd['handlerClassName']])
        handler_cls    = getattr(handler_module, cmd['handlerClassName'])
        handler        = handler_cls()
        cmd_def.commandCreated.add(handler)
        _command_handlers.append(handler)

def cleanup_commands():
    """
    Remove the UI controls and command definitions we added.
    """
    # 1) Remove controls
    for ctrl in _command_controls:
        try:
            ctrl.deleteMe()
        except:
            pass
    _command_controls.clear()

    # 2) Remove command event handlers
    for handler in _command_handlers:
        try:
            handler.deleteMe()
        except:
            pass
    _command_handlers.clear()

    # 3) Remove definitions
    for cmd_def in _command_defs:
        try:
            cmd_def.deleteMe()
        except:
            pass
    _command_defs.clear()