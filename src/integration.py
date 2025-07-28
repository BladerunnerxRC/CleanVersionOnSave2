import adsk.core, adsk.fusion, traceback
import commands, settings, timer

handlers     = []
sync_timer   = timer.SyncTimer()

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # 1) Register ONLY your Settings & Export buttons
        commands.register_commands()

        # 2) Hook the auto-rename on save
        from clean_version import DocumentSavingHandler
        saveHandler = DocumentSavingHandler()
        app.documentSaving.add(saveHandler)
        handlers.append(saveHandler)

        # 3) Start any background timer you have
        sync_timer.start()

    except Exception:
        if ui:
            ui.messageBox(f'Add-In start failed:\n{traceback.format_exc()}')

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # 1) Remove save handlers
        for h in handlers:
            app.documentSaving.remove(h)
        handlers.clear()

        # 2) Stop background timer
        sync_timer.stop()

        # 3) Tear down your two buttons
        commands.cleanup_commands()

    except Exception:
        if ui:
            ui.messageBox(f'Add-In stop failed:\n{traceback.format_exc()}')