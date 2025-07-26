import adsk.core, adsk.fusion, traceback
import re, logger, validator
import commands, timer
import os, datetime   # ← for custom logger

# === Custom File Logger (Fallback #4) ===
LOG_PATH = os.path.join(os.path.dirname(__file__), 'debug.log')
def dbg(msg):
    ts = datetime.datetime.now().isoformat()
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f'{ts} | {msg}\n')

sync_timer = timer.SyncTimer()
handlers = []

class DocumentSavingHandler(adsk.core.DocumentEventHandler):
    def notify(self, args):
        dbg('ENTER notify()')
        try:
            app = adsk.core.Application.get()
            doc = app.activeDocument
            original = doc.name
            clean = re.sub(r'\s*v\d+$', '', original)
            dbg(f'Computed clean name: "{clean}" from "{original}"')

            if validator.is_valid(clean):
                dbg(f'Name valid → renaming to "{clean}"')
                doc.name = clean
                logger.log_rename(original, clean, 'autosave')
                dbg('logger.log_rename called')
            else:
                dbg(f'Name INVALID: "{clean}" → showing messageBox')
                app.userInterface.messageBox(f"Invalid name: {clean}")
        except Exception as e:
            err = traceback.format_exc()
            dbg(f'EXCEPTION in notify(): {err}')
            logger.log_error(err)
        finally:
            dbg('EXIT notify()')

def run(context):
    dbg('ENTER run()')
    try:
        app = adsk.core.Application.get()
        handler = DocumentSavingHandler()
        app.documentSaving.add(handler)
        handlers.append(handler)
        dbg('DocumentSavingHandler registered')

        commands.register_commands()
        dbg('commands.register_commands() called')

        sync_timer.start()
        dbg('sync_timer started')
    except Exception as e:
        err = traceback.format_exc()
        dbg(f'EXCEPTION in run(): {err}')
        logger.log_error(err)
    finally:
        dbg('EXIT run()')

def stop(context):
    dbg('ENTER stop()')
    try:
        app = adsk.core.Application.get()
        for h in handlers:
            app.documentSaving.remove(h)
            dbg('Removed one DocumentSavingHandler')
        handlers.clear()
        dbg('handlers list cleared')

        sync_timer.stop()
        dbg('sync_timer stopped')
    except Exception as e:
        err = traceback.format_exc()
        dbg(f'EXCEPTION in stop(): {err}')
        logger.log_error(err)
    finally:
        dbg('EXIT stop()')