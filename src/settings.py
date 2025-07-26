import adsk.core, adsk.fusion, json, os, traceback

# Keep references so Fusion doesn’t GC them
handlers = []
palette = None
htmlLoadedHandler = None
htmlEventHandler = None
idleHandler = None

def run(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Paths
        addinFolder = os.path.dirname(__file__)
        cfgPath     = os.path.join(addinFolder, 'data', 'config.json')
        htmlPath    = os.path.join(addinFolder, 'resources', 'settings.html')

        # Create the HTML palette
        global palette
        palette = ui.palettes.add(
            'MyAddinSettings', 'Settings',
            htmlPath,
            True,  # isVisible
            True,  # showInPaletteList
            True,  # initialStateDockable
            600,   # width
            400    # height
        )

        # 1) Push initial config.json on HTML load
        class OnHtmlLoaded(adsk.core.HTMLEventHandler):
            def notify(self, args):
                try:
                    with open(cfgPath, 'r') as f:
                        cfg = json.load(f)
                    # call JS loadSettings(cfg)
                    palette.evaluateJavascript(f'loadSettings({json.dumps(cfg)});')
                except:
                    ui.messageBox('Failed to load settings from disk.')

        global htmlLoadedHandler
        htmlLoadedHandler = OnHtmlLoaded()
        palette.htmlLoaded.add(htmlLoadedHandler)
        handlers.append(htmlLoadedHandler)

        # 2) Listen for Save clicks from JS, write back to disk
        class OnHtmlEvent(adsk.core.HTMLEventHandler):
            def notify(self, args):
                try:
                    msg = json.loads(args.data)
                    if msg.get('action') == 'save':
                        with open(cfgPath, 'w') as f:
                            json.dump(msg['payload'], f, indent=2)
                        palette.evaluateJavascript("alert('Settings saved!');")
                except:
                    ui.messageBox('Failed to save settings.')

        global htmlEventHandler
        htmlEventHandler = OnHtmlEvent()
        palette.htmlEventReceived.add(htmlEventHandler)
        handlers.append(htmlEventHandler)

        # 3) Idle handler: watch config.json for external edits
        class IdleHandler(adsk.core.IdleEventHandler):
            def __init__(self):
                super().__init__()
                self.configPath = cfgPath
                self.lastMTime  = os.path.getmtime(self.configPath)
            def notify(self, args):
                try:
                    current = os.path.getmtime(self.configPath)
                    if current != self.lastMTime:
                        self.lastMTime = current
                        with open(self.configPath, 'r') as f:
                            cfg = json.load(f)
                        # call JS updateSettings(cfg)
                        if palette is not None:
                            palette.evaluateJavascript(f'updateSettings({json.dumps(cfg)});')
                except:
                    pass

        global idleHandler
        idleHandler = IdleHandler()
        app.idle.add(idleHandler)
        handlers.append(idleHandler)

    except:
        ui.messageBox('Add-in Start Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Remove handlers
        if idleHandler:
            app.idle.remove(idleHandler)
        if palette and htmlLoadedHandler:
            palette.htmlLoaded.remove(htmlLoadedHandler)
        if palette and htmlEventHandler:
            palette.htmlEventReceived.remove(htmlEventHandler)

        # Delete the palette
        if palette:
            palette.deleteMe()

        handlers.clear()

    except:
        ui.messageBox('Add-in Stop Failed:\n{}'.format(traceback.format_exc()))
