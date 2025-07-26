import adsk.core, adsk.fusion, traceback
import re, logger, validator
import commands, timer
sync_timer = timer.SyncTimer()


handlers = []

class DocumentSavingHandler(adsk.core.DocumentEventHandler):
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            doc = app.activeDocument
            original = doc.name
            clean = re.sub(r'\s*v\d+$', '', original)

            if validator.is_valid(clean):
                doc.name = clean
                logger.log_rename(original, clean, 'autosave')
            else:
                app.userInterface.messageBox(f"Invalid name: {clean}")
        except:
            logger.log_error(traceback.format_exc())

def run(context):
    try:
        app = adsk.core.Application.get()
        handler = DocumentSavingHandler()
        app.documentSaving.add(handler)
        handlers.append(handler)

        commands.register_commands()
        sync_timer.start()
    except:
        logger.log_error(traceback.format_exc())

def stop(context):
    try:
        app = adsk.core.Application.get()
        for h in handlers:
            app.documentSaving.remove(h)
        handlers.clear()

        sync_timer.stop()
    except:
        logger.log_error(traceback.format_exc())
