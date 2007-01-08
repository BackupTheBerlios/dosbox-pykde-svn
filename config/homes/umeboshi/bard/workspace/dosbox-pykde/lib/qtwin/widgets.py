import os
from qt import SIGNAL, SLOT
from qt import qApp
#from qt import QSplitter
#from qt import QGridLayout
#from qt import QLabel
#from qt import QFrame

from qt import QApplication
from qt import QMainWindow

#from kdecore import KAboutData
#from kdecore import KApplication


#from kdeui import KAboutDialog
#from kdeui import KMainWindow
#from kdeui import KListView, KListViewItem
#from kdeui import KTextBrowser
#from kdeui import KMessageBox
#from kdeui import KLineEdit
#from kdeui import KDialogBase
#from kdeui import KStdAction
#from kdeui import KPopupMenu
#from kdeui import KTextEdit
#from kdeui import KPushButton
#from kdeui import KProgressDialog

#from kfile import KDirSelectDialog
#from kfile import KFileDialog

#from khtml import KHTMLPart

from base import split_url
from base import opendlg_errormsg

#from actions import NewGenre, NewGame, LaunchDosbox
#from actions import NameView, TitleView
#from actions import FlatView, TreeView
# file management actions
#from actions import PrepareAllGames, CleanAllGames
#from actions import ArchiveAllGames
# filter actions
#from actions import FilterAvailableGames
#from actions import FilterAllGames
#from actions import FilterUnavailableGames

from infodoc import BaseDocument

#from gamedata_widgets import AddNewGameDialog
#from gamedata_widgets import EditGameDataDialog


# stuff to clean up in this file

# fix imports from actions, if possible

# replace KMessageBox

# replace KFileDialog


# classes to convert from kde
# InfoBrowser
# AboutData
# AboutDialog
# MainApplication - done
# MainWindow
# BaseProgressDialog
# MultiGameProgressDialog

        
# main window
class MainWindow(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent, 'PyQt Dosbox Frontend')
        # setup app pointer
        self.app = qApp
        self.config = self.app.config
        self.resize(*self.config.get_xy('mainwindow', 'mainwindow_size'))
        # initialize game data
        pass
    
    

if __name__ == '__main__':
    print "testing module"
    
