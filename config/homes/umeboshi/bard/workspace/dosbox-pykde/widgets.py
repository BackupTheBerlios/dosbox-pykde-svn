import os
from qt import SIGNAL, SLOT
from qt import QSplitter
from qt import qApp
#from qt import QGridLayout
#from qt import QLabel
#from qt import QFrame

from kdecore import KAboutData
#from kdecore import KCmdLineArgs
from kdecore import KApplication
#from kdecore import KEntryKey, KEntry

from kdeui import KAboutDialog
from kdeui import KMainWindow
from kdeui import KListView, KListViewItem
from kdeui import KTextBrowser
from kdeui import KMessageBox
#from kdeui import KLineEdit
#from kdeui import KDialogBase
from kdeui import KStdAction
from kdeui import KPopupMenu

from kfile import KDirSelectDialog

from actions import NewGenre, NewGame
from infodoc import BaseDocument

# text browser for game info
class InfoBrowser(KTextBrowser):
    def __init__(self, parent):
        KTextBrowser.__init__(self, parent)
        self.setNotifyClick(True)
        self.doc = BaseDocument()

    def set_game_info(self, name):
        self.doc.set_info(name)
        self.setText(self.doc.output())
        
    # this is selected when a url is clicked
    def setSource(self, url):
        action, key, filename = split_url(url)
        if action == 'new':
            dlg = XattrDialog(self, filename)
            dlg.connect(dlg, SIGNAL('okClicked()'), dlg.update_xattr)
            dlg.show()
        elif action == 'edit':
            value = xattr(filename).get(key)
            dlg = XattrDialog(self, filename, key, value)
            dlg.connect(dlg, SIGNAL('okClicked()'), dlg.update_xattr)
            dlg.show()
        elif action == 'delete':
            dlg = XattrDialog(self, filename, key, action='delete')
            dlg.connect(dlg, SIGNAL('okClicked()'), dlg.delete_xattr)
            dlg.show()


# about this program
class AboutData(KAboutData):
    def __init__(self):
        KAboutData.__init__(self,
                            'dosbox-pykde',
                            'dosbox-pykde',
                            '0.1',
                            "Another dosbox frontend")
        self.addAuthor('Joseph Rawson', 'author',
                       'umeboshi@gregscomputerservice.com')
        self.setCopyrightStatement('public domain')

class AboutDialog(KAboutDialog):
    def __init__(self):
        KAboutDialog.__init__(self, parent, *args)
        self.setTitle('PyKDE Dosbox Frontend')
        self.setAuthor('Joseph Rawson')
        
# main application class
class MainApplication(KApplication):
    def __init__(self):
        KApplication.__init__(self)
        # in case something needs done before quitting
        self.connect(self, SIGNAL('aboutToQuit()'), self.quit)
        
    def quit(self):
        KApplication.quit(self)

# main window class
class MainWindow(KMainWindow):
    def __init__(self, parent):
        KMainWindow.__init__(self, parent, 'PyKDE Dosbox Frontend')
        #self.resize(500, 450)
        self.initActions()
        self.initMenus()
        self.initToolbar()
        # place a splitter in the window
        self.splitView = QSplitter(self, 'splitView')
        # place a listview in the splitter (on the left)
        self.listView = KListView(self.splitView, 'games_view')
        # fill listview
        self.initlistView()
        # setup signals
        self.connect(self.listView,
                     SIGNAL('selectionChanged()'), self.selectionChanged)
        
        # place text browser in splitter
        self.textView = InfoBrowser(self.splitView)
        
        self.setCentralWidget(self.splitView)
        self.config = KApplication.kApplication().config

        # setup dialog pointers
        self.new_game_dir_dialog = None
        self.new_game_dialog = None
        self.new_genre_dialog = None
        
    def initlistView(self):
        self.listView.addColumn('genre', -1)

    def selectionChanged(self):
        item = self.listView.currentItem()
        self.textView.setFileName(item.filename)   
        
    def initActions(self):
        collection = self.actionCollection()
        self.quitAction = KStdAction.quit(self.close, collection)
        self.newGenreAction = NewGenre(self.slotNewGenre, collection)
        self.newGameAction = NewGame(self.slotNewGame, collection)

    def initMenus(self):
        mainmenu = KPopupMenu(self)
        self.newGenreAction.plug(mainmenu)
        self.newGameAction.plug(mainmenu)
        self.quitAction.plug(mainmenu)
        self.menuBar().insertItem('&Main', mainmenu)
        self.menuBar().insertItem('&Help', self.helpMenu(''))

    def initToolbar(self):
        toolbar = self.toolBar()
        self.newGenreAction.plug(toolbar)
        self.newGameAction.plug(toolbar)
        self.quitAction.plug(toolbar)
        
    def slotNewGame(self):
        if self.new_game_dir_dialog is None:
            dlg = KDirSelectDialog(self.config.get('DEFAULT', 'main_dosbox_path'), 0, self)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.select_new_game_path)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_new_game_dir_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_new_game_dir_dlg)
            dlg.show()
            self.new_game_dir_dialog = dlg
        else:
            KMessageBox.error(self,
                             'There is already a dialog box open.  Close it or restart the program')

    def destroy_new_game_dir_dlg(self, *args):
        print 'args', args
        self.new_game_dir_dialog = None
        
    def slotNewGenre(self):
        KMessageBox.information(self,
                                'create new genre')

    def select_new_game_path(self):
        url = self.new_game_dir_dialog.url()
        fullpath = str(url.path())
        name = os.path.basename(fullpath)
        print name, fullpath
        self.new_game_dir_dialog = None

    
if __name__ == '__main__':
    print "testing module"
    
