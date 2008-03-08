import traceback
from StringIO import StringIO

from qt import QGridLayout
from qt import QLabel
from qt import QFrame

from kdecore import KApplication

from kdeui import KMainWindow
from kdeui import KMessageBox
from kdeui import KDialogBase
from kdeui import KLineEdit


separator = '-' * 80

def excepthook(type, value, tracebackobj):
    tbinfofile = StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: %s' % (str(type), str(value))
    sections = [separator, errmsg, separator]
    msg = '\n'.join(sections)
    KMessageBox.detailedError(None, msg, tbinfo)

def get_application_pointer():
    return KApplication.kApplication()

class BaseEntryDialog(KDialogBase):
    def __init__(self, parent, name='BaseEntryDialog'):
        KDialogBase.__init__(self, parent, name)
        self.frame = QFrame(self)
        self.setMainWidget(self.frame)
        self.frame.grid = QGridLayout(self.frame, 1, 2, 5, 7)
        self.label = QLabel(self.frame)
        self.entry = KLineEdit(self.frame)
        self.frame.grid.addWidget(self.label, 0, 0)
        self.frame.grid.addWidget(self.entry, 1, 0)
        
class BaseDialogWindow(KDialogBase):
    def __init__(self, parent, name='BaseDialogWindow'):
        KDialogBase.__init__(self, parent, name)
        self.app = get_application_pointer()
        self.myconfig = self.app.myconfig
        
class BaseMainWindow(KMainWindow):
    def __init__(self, parent, name='BaseMainWindow'):
        KMainWindow.__init__(self, parent, name)
        self.app = get_application_pointer()
        self.myconfig = self.app.myconfig
