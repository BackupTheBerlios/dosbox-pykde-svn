import os
from qt import SIGNAL, SLOT
from qt import qApp
#from qt import QSplitter
#from qt import QGridLayout
#from qt import QLabel
#from qt import QFrame

from qt import QApplication
from qt import QMainWindow
from qt import QPopupMenu

from base import split_url
from base import opendlg_errormsg

from actions import NewGenre, NewGame, LaunchDosbox
from actions import NameView, TitleView
from actions import FlatView, TreeView
# file management actions
from actions import PrepareAllGames, CleanAllGames
from actions import ArchiveAllGames
# filter actions
from actions import FilterAvailableGames
from actions import FilterAllGames
from actions import FilterUnavailableGames
# standard actions
from actions import QuitAction

from common.mainwindow import MainWindowCommon
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
class MainWindow(MainWindowCommon, QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent, 'PyQt Dosbox Frontend')
        # setup app pointer
        self.app = qApp
        self.config = self.app.config
        self.resize(*self.config.get_xy('mainwindow', 'mainwindow_size'))
        # initialize game data

        self.initActions()
        self.initMenus()
        
    def initActions(self):
        self.quitAction = QuitAction(self.close, self)
        self.newGameAction = NewGame(self.slotNewGame, self)
        self.launchDosboxAction = LaunchDosbox(self.slotLaunchDosbox, self)
        self.flatViewAction = FlatView(self.slotFlatView, self)
        self.treeViewAction = TreeView(self.slotTreeView, self)
        self.nameViewAction = NameView(self.slotNameView, self)
        self.titleViewAction = TitleView(self.slotTitleView, self)
        self.prepareAllGamesAction = PrepareAllGames(self.slotPrepareAllGames, self)
        self.cleanAllGamesAction = CleanAllGames(self.slotCleanAllGames, self)
        self.archiveAllGamesAction = ArchiveAllGames(self.slotArchiveAllGames, self)
        self.filterAllGamesAction = FilterAllGames(self.slotFilterAllGames, self)
        self.filterAvailableGamesAction = \
                                        FilterAvailableGames(self.slotFilterAvailableGames,
                                                             self)
        self.filterUnavailableGamesAction = \
                                          FilterUnavailableGames(self.slotFilterUnavailableGames,
                                                                 self)

    def initMenus(self):
        mainmenu = QPopupMenu(self)
        self.newGameAction.addTo(mainmenu)
        self.launchDosboxAction.addTo(mainmenu)
        mainmenu.insertSeparator()
        self.prepareAllGamesAction.addTo(mainmenu)
        self.cleanAllGamesAction.addTo(mainmenu)
        self.archiveAllGamesAction.addTo(mainmenu)
        self.quitAction.addTo(mainmenu)
        optionmenu = QPopupMenu(self)
        self.flatViewAction.addTo(optionmenu)
        self.treeViewAction.addTo(optionmenu)
        self.nameViewAction.addTo(optionmenu)
        self.titleViewAction.addTo(optionmenu)
        optionmenu.insertSeparator()
        self.filterAllGamesAction.addTo(optionmenu)
        self.filterAvailableGamesAction.addTo(optionmenu)
        self.filterUnavailableGamesAction.addTo(optionmenu)
        menubar = self.menuBar()
        menubar.insertItem('&Main', mainmenu)
        menubar.insertItem('&Options', optionmenu)
        
        
        
        
    

if __name__ == '__main__':
    print "testing module"
    
