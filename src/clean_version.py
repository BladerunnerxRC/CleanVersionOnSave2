import adsk.core, adsk.fusion, traceback
import re, logger, validator, settings, timer

sync_timer = timer.SyncTimer()
handlers    = []

class DocumentSavingHandler(adsk.core.DocumentEventHandler):
    def notify(self, args):
        try:
            # Only rename if feature is turned on
            if not settings.featureEnabled:
                return

            app      = adsk.core.Application.get()
            doc      = app.activeDocument
            original = doc.name

            # Strip trailing ' v<digits>' tag
            baseName = re.sub(r'\s*v\d+$', '', original)

            # Append custom text (if set), else leave baseName
            newName = (
                f"{baseName}{settings.customVersionText}"
                if settings.customVersionText
                else baseName
            )

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

        # Register UI buttons
        import commands
        commands.register_commands()

        # Start any external sync you have
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

        # Stop sync timer
        sync_timer.stop()

        # Tear down commands (delete definitions & controls)
        import commands
        commands.cleanup_commands()

    except:
        logger.log_error(traceback.format_exc())