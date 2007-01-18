import traceback
from StringIO import StringIO
from kdeui import KMessageBox

separator = '-' * 80

def excepthook(type, value, tracebackobj):
    tbinfofile = StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    sections = [str(type), str(value), separator, tbinfo, separator]
    msg = '\n'.join(sections)
    KMessageBox.error(None, msg)
    
