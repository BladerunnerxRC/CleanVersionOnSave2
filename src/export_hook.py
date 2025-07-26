import adsk.core, adsk.fusion, re, validator, logger, settings

def on_export(args):
    cfg     = settings.load_settings()
    formats = cfg.get('exportFormats', ['STEP'])
    app     = adsk.core.Application.get()
    doc     = app.activeDocument
    base    = re.sub(r'\s*v\d+$', '', doc.name)

    mgr = doc.exportManager
    for fmt in formats:
        name = f"{base}.{fmt.lower()}"
        options = {
            'STEP': mgr.createSTEPExportOptions,
            'IGES': mgr.createIGESExportOptions,
            'DXF':  mgr.createDXF2DExportOptions
        }[fmt](name, doc.design if fmt != 'DXF' else doc.design.rootComponent)
        mgr.execute(options)
        logger.log_rename(doc.name, name, f'export-{fmt}')
