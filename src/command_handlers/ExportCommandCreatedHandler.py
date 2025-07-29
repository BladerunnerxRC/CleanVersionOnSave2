import adsk.core, adsk.fusion, traceback
from ..export_hook import ExportCommandCreatedEventHandler

# If you already have the export logic in export_hook.py,
# simply wrap or re-export it here:
class ExportCommandCreatedHandler(ExportCommandCreatedEventHandler):
    pass