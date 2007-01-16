import os
from qt import SIGNAL, SLOT
from qt import qApp

from qt import QApplication
from qt import QMainWindow
from qt import QPopupMenu
from qt import QSplitter
from qt import QListView, QListViewItem
from qt import QMessageBox


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

#from gamedata_widgets import AddNewGameDialog
#from gamedata_widgets import EditGameDataDialog

from infobrowser import InfoBrowser


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
        self._init_common()

        self.splitView = QSplitter(self, 'splitView')
        self.listView = QListView(self.splitView, 'games_view')
        self.initlistView()
        x, y = self.config.get_xy('mainwindow', 'mainwindow_size')
        self.splitView.setSizes([int(.1*x), int(.9*x)])
        self.connect(self.listView,
                     SIGNAL('selectionChanged()'), self.selectionChanged)
        self.textView = InfoBrowser(self.splitView)
        self.setCentralWidget(self.splitView)
        
        
        
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

    # do nothing here, for now
    def initToolbar(self):
        pass
    
    def refreshListView(self):
        self.refreshListView_common(QListViewItem)

    def _appendListItem(self, parent, name):
        self._appendListItem_common(parent, name, QListViewItem)
        
    def selectGame(self, name, called_externally=False):
        self.textView.set_game_info(name)

    def slotLaunchDosbox(self, game=None):
        if game is None:
            game = self.listView.currentItem().game
        if self.app.game_fileshandler.get_game_status(game):
            self.app.dosbox.run_game(game)
        else:
            title = self.game_titles[game]
            box = QMessageBox.information(self, 'UnavailableGame')
            box.setText('%s is unavailable' % title)
        
        
    

if __name__ == '__main__':
    print "testing module"
    
