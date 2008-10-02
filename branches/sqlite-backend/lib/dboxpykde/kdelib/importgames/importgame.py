import os
from qt import SIGNAL, SLOT
from qt import PYSIGNAL
from qt import QFrame, QLabel
from qt import QGridLayout
from qt import QScrollView

from kdeui import KLineEdit

#from kdeui import KMainWindow
#from kdeui import KListView, KListViewItem
from kdeui import KMessageBox
#from kdeui import KStdAction
#from kdeui import KPopupMenu
#from kdeui import KStatusBar
from khtml import KHTMLPart
from khtml import KHTMLView

#from kfile import KDirSelectDialog

#from dboxpykde.base import split_url
#from dboxpykde.base import opendlg_errormsg
#from dboxpykde.base import ExistsError
from dboxpykde.filemanagement.httphandler import AbandonGamesHandler

from dboxpykde.kdelib.base import get_application_pointer
from dboxpykde.kdelib.base import BaseDialogWindow

from infodoc import AbandoniaInfoDocument
from importpart import BaseAbandoniaPart

class AbandoniaInfoWindow(BaseDialogWindow):
    def __init__(self, parent, name='AbandoniaInfoWindow'):
        BaseDialogWindow.__init__(self, parent, name=name)
        self.handler = parent.handler
        margin = 5
        space = 7
        self.box = self.makeVBoxMainWidget()
        self.htmlpart = BaseAbandoniaPart(self.box)
        self.htmlpart.set_game_info(self.handler)
        self.setMainWidget(self.box)
        self.resize(400, 600)
        
        
class ImportGameUrlDialog(BaseDialogWindow):
    def __init__(self, parent, name='ImportGameUrlDialog'):
        BaseDialogWindow.__init__(self, parent, name=name)
        self.frame = QFrame(self)
        margin = 5
        space = 7
        self.grid = QGridLayout(self.frame, 2, 1, margin, space)
        self.url_lbl = QLabel('URL', self.frame)
        self.url_entry = KLineEdit('', self.frame)
        self.grid.addWidget(self.url_lbl, 0, 0)
        self.grid.addWidget(self.url_entry, 1, 0)
        self.setMainWidget(self.frame)
        self.connect(self, SIGNAL('okClicked()'), self.import_game)
        self.handler = AbandonGamesHandler(self.app)

    def _makeinfo(self, base, parser):
        text = 'Title: %s\n' % parser.title
        if parser.smallinfo:
            text += 'Small Information'
            for k,v in parser.smallinfo.items():
                text += '%s: %s\n' % ( k.capitalize(), v)
        #text += str(parser.smallinfo) + '\n'
        dlurl = base + parser.download_link
        text += 'download page: %s\n' % dlurl
        text += 'direct link: %s\n' % parser.real_download_link
        if parser.files:
            text += 'Files:\n'
            text += '======\n'
            for f in parser.files:
                text += '%s%s\n' % (base, f)
        return text
        
    def import_game(self):
        url = str(self.url_entry.text())
        print url
        #KMessageBox.information(self, "import_game is still not implemented")
        
        #self.handler.get_game_data(url)
        self.handler.handle_url(url)
        #self.handler.parser.feed(file('dunetest.html').read())
        win = AbandoniaInfoWindow(self)
        win.show()
        #import pdb
        #pdb.set_trace()
        
        
        
