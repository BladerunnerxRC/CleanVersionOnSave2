import adsk.core, adsk.fusion, traceback
import re, logger, validator, settings, timer, commands

sync_timer = timer.SyncTimer()
handlers    = []

class DocumentSavingHandler(adsk.core.DocumentEventHandler):
    def notify(self, args):
        try:
            settings.load()  # pick up any external changes
            if not settings.featureEnabled:
                return

            app      = adsk.core.Application.get()
            doc      = app.activeDocument
            original = doc.name

            baseName = re.sub(r'\s*v\d+$', '', original)
            if settings.customVersionText:
                newName = f"{baseName}{settings.customVersionText}"
            else:
                newName = baseName

            if validator.is_valid(newName):
                doc.name = newName
                logger.log_rename(original, newName, 'autosave')
            else:
                app.userInterface.messageBox(f"Invalid name: {newName}")

        except:
            logger.log_error(traceback.format_exc())

def run(context):
    try:
        app = adsk.core.Application.get()

        # Hook the save event
        saveHandler = DocumentSavingHandler()
        app.documentSaving.add(saveHandler)
        handlers.append(saveHandler)

        # Register only your two UI commands
        commands.register_commands()

        # Start any sync timer you have
        sync_timer.start()

    except:
        logger.log_error(traceback.format_exc())

def stop(context):
    try:
        app = adsk.core.Application.get()

        # Remove save handler
        for h in handlers:
            app.documentSaving.remove(h)
        handlers.clear()

        # Stop sync
        sync_timer.stop()

        # Tear down only your commands
        commands.cleanup_commands()

    except:
        logger.log_error(traceback.format_exc())