from qt import SIGNAL
from qt import QSplitter

from kdeui import KMainWindow
from kdeui import KListView, KListViewItem

from dboxpykde.filemanagement.httphandler import AbandonGamesHandler
from dboxpykde.kdelib.base import BaseMainWindow

from importpart import MainAbandoniaPart

class ImportsMainWindow(BaseMainWindow):
    def __init__(self, parent, name='ImportsMainWindow'):
        BaseMainWindow.__init__(self, parent, name=name)
        self.handler = AbandonGamesHandler(self.app)
        self.splitView = QSplitter(self)
        self.listView = KListView(self.splitView)
        self.connect(self.listView,
                     SIGNAL('selectionChanged()'), self.selectionChanged)
        
        self.initlistView()
        self.textView = MainAbandoniaPart(self.splitView)
        self.setCentralWidget(self.splitView)
        
        
    def initlistView(self):
        self.listView.addColumn('games', -1)
        self.refreshListView()
        
    def refreshListView(self):
        self.listView.clear()
        gameids = self.handler.get_all_html_ids()
        print 'in initlistView', gameids
        for gameid in gameids:
            #item = KListViewItem(self.listView, str(gameid))
            #item.gameid = gameid
            self.handler.get_game_data(gameid)
            item = KListViewItem(self.listView, self.handler.parser.title)
            item.gameid = gameid
            
    def selectionChanged(self):
        item = self.listView.currentItem()
        self.handler.get_game_data(item.gameid)
        print 'in selectionChanged', self.handler.parser.gameid
        self.textView.set_game_info(self.handler)
        
