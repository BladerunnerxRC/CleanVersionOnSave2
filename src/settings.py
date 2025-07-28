import adsk.core, adsk.fusion, json, os, traceback

# Paths
_addinFolder = os.path.dirname(__file__)
_cfgPath     = os.path.join(_addinFolder, 'data', 'config.json')
_htmlPath    = os.path.join(_addinFolder, 'resources', 'settings.html')

# Default values
featureEnabled     = False
customVersionText  = ''

def load():
    """Read config.json into module globals, creating it if missing."""
    global featureEnabled, customVersionText

    if not os.path.exists(_cfgPath):
        os.makedirs(os.path.dirname(_cfgPath), exist_ok=True)
        with open(_cfgPath, 'w') as f:
            json.dump({
                "featureEnabled": False,
                "customVersionText": ""
            }, f, indent=2)

    with open(_cfgPath, 'r') as f:
        cfg = json.load(f)

    featureEnabled    = bool(cfg.get('featureEnabled', False))
    customVersionText = str(cfg.get('customVersionText', ''))

    return cfg

def save():
    """Persist current globals to config.json."""
    try:
        cfg = {
            "featureEnabled": featureEnabled,
            "customVersionText": customVersionText
        }
        with open(_cfgPath, 'w') as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        adsk.core.Application.get().userInterface.messageBox(
            f"Failed to write settings:\n{traceback.format_exc()}"
        )

# Load on import
load()

# HTML palette and handlers
handlers           = []
palette            = None
htmlLoadedHandler  = None
htmlEventHandler   = None
idleHandler        = None

def run(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        global palette
        palette = ui.palettes.add(
            'MyAddinSettings', 'Settings',
            _htmlPath,
            True, True, True,
            600, 400
        )

        # 1) Push initial config.json on HTML load
        class OnHtmlLoaded(adsk.core.HTMLEventHandler):
            def notify(self, args):
                try:
                    cfg = load()
                    palette.evaluateJavascript(
                        f"loadSettings({json.dumps(cfg)});"
                    )
                except:
                    ui.messageBox('Failed to load settings into HTML.')

        global htmlLoadedHandler
        htmlLoadedHandler = OnHtmlLoaded()
        palette.htmlLoaded.add(htmlLoadedHandler)
        handlers.append(htmlLoadedHandler)

        # 2) Save clicks from JS → update globals & disk
        class OnHtmlEvent(adsk.core.HTMLEventHandler):
            def notify(self, args):
                try:
                    msg = json.loads(args.data)
                    if msg.get('action') == 'save':
                        data = msg['payload']
                        # update module globals
                        globals()['featureEnabled']    = bool(data.get('featureEnabled'))
                        globals()['customVersionText'] = str(data.get('customVersionText'))
                        save()
                        palette.evaluateJavascript("alert('Settings saved!');")
                    # you can handle other actions here
                except:
                    ui.messageBox('Failed to save settings from HTML.')

        global htmlEventHandler
        htmlEventHandler = OnHtmlEvent()
        palette.htmlEventReceived.add(htmlEventHandler)
        handlers.append(htmlEventHandler)

        # 3) Idle: watch for external edits
        class IdleHandler(adsk.core.IdleEventHandler):
            def __init__(self):
                super().__init__()
                self.lastMTime = os.path.getmtime(_cfgPath)

            def notify(self, args):
                try:
                    current = os.path.getmtime(_cfgPath)
                    if current != self.lastMTime:
                        self.lastMTime = current
                        cfg = load()
                        if palette:
                            palette.evaluateJavascript(
                                f"updateSettings({json.dumps(cfg)});"
                            )
                except:
                    pass

        global idleHandler
        idleHandler = IdleHandler()
        app.idle.add(idleHandler)
        handlers.append(idleHandler)

    except:
        ui.messageBox(f"Add-in Start Failed:\n{traceback.format_exc()}")

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        if idleHandler:
            app.idle.remove(idleHandler)
        if palette and htmlLoadedHandler:
            palette.htmlLoaded.remove(htmlLoadedHandler)
        if palette and htmlEventHandler:
            palette.htmlEventReceived.remove(htmlEventHandler)

        if palette:
            palette.deleteMe()

        handlers.clear()

    except:
        ui.messageBox(f"Add-in Stop Failed:\n{traceback.format_exc()}")