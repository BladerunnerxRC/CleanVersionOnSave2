# src/integration.py

import adsk.core, adsk.fusion, traceback
from .commands import register_commands, cleanup_commands
from .clean_version import DocumentSavingHandler, sync_latest_rename
from .timer import SyncTimer

# Store handlers so they can be removed on stop()
_handlers = []
# Pass the clean_version sync function into the timer
_sync_timer = SyncTimer(sync_latest_rename, interval_sec=300)

def run(context):
    """
    Called by CleanVersionOnSave2.py when the Add-In starts.
    """
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # 1) Build your UI buttons
        register_commands()

        # 2) Hook the on-save handler
        save_handler = DocumentSavingHandler()
        app.documentSaving.add(save_handler)
        _handlers.append(save_handler)

        # 3) Start periodic sync if desired
        _sync_timer.start()

    except Exception:
        if ui:
            ui.messageBox(
                'Failed to initialize CleanVersionOnSave2:\n{}'.format(traceback.format_exc())
            )

def stop(context):
    """
    Called by CleanVersionOnSave2.py when the Add-In stops.
    """
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # 1) Unhook all on-save handlers
        for h in _handlers:
            try:
                app.documentSaving.remove(h)
            except:
                pass
        _handlers.clear()

        # 2) Tear down UI commands
        cleanup_commands()

        # 3) Stop the sync timer
        _sync_timer.stop()

    except Exception:
        if ui:
            ui.messageBox(
                'Failed to shutdown CleanVersionOnSave2:\n{}'.format(traceback.format_exc())
            )