import os
import urlparse

from qt import SIGNAL, SLOT
from qt import PYSIGNAL
from qt import QFrame, QLabel
from qt import QGridLayout
from qt import QScrollView

from kdecore import KURL
from kdeui import KLineEdit

#from kdeui import KMainWindow
#from kdeui import KListView, KListViewItem
from kdeui import KMessageBox
#from kdeui import KStdAction
#from kdeui import KPopupMenu
#from kdeui import KStatusBar
from khtml import KHTMLPart
from kio import KIO

#from kfile import KDirSelectDialog

#from dboxpykde.base import split_url
#from dboxpykde.base import opendlg_errormsg
#from dboxpykde.base import ExistsError
from dboxpykde.filemanagement.httphandler import AbandonGamesHandler

from dboxpykde.kdelib.base import get_application_pointer
#rom base import BaseDialogWindow
from infodoc import AbandoniaInfoDocument

class BaseAbandoniaPart(KHTMLPart):
    def __init__(self, parent, name='AbandonPart'):
        KHTMLPart.__init__(self, parent, name)
        self.app = get_application_pointer()
        self.doc  = AbandoniaInfoDocument(self.app)
        self.handler = AbandonGamesHandler(self.app)
        self.begin()
        self.write('')
        self.end()
        
    def set_game_info(self, handler):
        self.gameid = handler.parser.gameid
        self.begin()
        self.write('')
        self.end()
        self.app.processEvents()
        self.begin()
        self.doc.set_info(handler)
        self.write(self.doc.output())
        self.end()
        print 'in set_game_info', self.gameid

class MainAbandoniaPart(BaseAbandoniaPart):
    def urlSelected(self, url, button, state, target, args):
        url = str(url)
        if url == 'download':
            self.handler.get_game_data(self.gameid)
            self.handler.get_dl_link()
            urlp = urlparse.urlparse(self.handler.real_download_link)
            fname = os.path.basename(urlp[2])
            dlpath = ''
            if not self.handler.does_download_exist(fname):
                dlpath = self.handler.game_download_path(fname).dirname()
                dlpath = 'file://%s' % dlpath
            if dlpath:
                kl = KURL.List()
                kl.append(KURL(self.handler.real_download_link))
                job = KIO.copy(kl, KURL(dlpath))
                job.gameid = self.gameid
                job.setName('game-%d' % self.gameid)
                self.connect(job, SIGNAL('result(KIO::Job *)'),
                             self._handle_job)
        elif url.startswith('extras/'):
            fname = url.split('/')[-1]
            if not self.handler.is_extra_downloaded(fname):
                url = url[7:]
                kl = KURL.List()
                kl.append(KURL(url))
                dlpath = 'file://%s' % self.handler.extras_path(fname)
                job = KIO.copy(kl, KURL(dlpath))
                job.setName('extras-%s' % dlpath)

    def _handle_job(self, job):
        #import pdb
        #pdb.set_trace()
        gameid = int(str(job.name()[5:]))
        self.handler.set_game_downloaded(gameid)
            
            
        
