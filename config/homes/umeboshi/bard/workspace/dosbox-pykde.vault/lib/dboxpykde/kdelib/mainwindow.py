import os
from qt import SIGNAL, SLOT
from qt import PYSIGNAL
from qt import QSplitter

from kdecore import KApplication


from kdeui import KMainWindow
from kdeui import KListView, KListViewItem
from kdeui import KMessageBox
from kdeui import KStdAction
from kdeui import KPopupMenu

from kfile import KDirSelectDialog

from dboxpykde.base import split_url
from dboxpykde.base import opendlg_errormsg
from dboxpykde.base import ExistsError


# import actions
from actions import NewGenre, NewGame, LaunchDosbox
from actions import LaunchDosboxPrompt
# view actions
from actions import NameView, TitleView
from actions import FlatView, TreeView
# file management actions
from actions import PrepareAllGames, CleanAllGames
from actions import ArchiveAllGames
# filter actions
from actions import FilterAvailableGames
from actions import FilterAllGames
from actions import FilterUnavailableGames

# import game data dialogs
from gamedata_widgets import AddNewGameDialog
from gamedata_widgets import EditGameDataDialog

from infobrowser import InfoBrowser
from progress_dialogs import MultiGameProgressDialog
# using BaseProgressDialog until a better class is made
from progress_dialogs import BaseProgressDialog

from dboxpykde.common.mainwindow import MainWindowCommon

# main window class
class MainWindow(MainWindowCommon, KMainWindow):
    def __init__(self, parent):
        KMainWindow.__init__(self, parent, 'PyKDE Dosbox Frontend')
        # setup app pointer
        self.app = KApplication.kApplication()
        self._init_common()

        # from here to the splitView should be in _init_common
        #self.config = self.app.config
        #self.resize(*self.config.get_xy('mainwindow', 'mainwindow_size'))
        # initialize game data
        #self.initialize_important_game_data()
        #self._treedict = {}
        #self._show_filter = 'all'
        # setup default view options
        #self.flat_tree_view = self.config.get('mainwindow', 'flat_tree_view')
        #self.name_title_view = self.config.get('mainwindow', 'name_title_view')
        #self.resize(500, 450)
        #self.initActions()
        #self.initMenus()
        #self.initToolbar()

        
        # place a splitter in the window
        self.splitView = QSplitter(self, 'splitView')
        # place a listview in the splitter (on the left)
        self.listView = KListView(self.splitView, 'games_view')
        # fill listview
        self.initlistView()
        # try to resize splitter
        # this is a kind of ugly hack, but seems to work ok
        x, y = self.config.get_xy('mainwindow', 'mainwindow_size')
        self.splitView.setSizes([int(.1*x), int(.9*x)])
        # setup signals
        self.connect(self.listView,
                     SIGNAL('selectionChanged()'), self.selectionChanged)
        
        # place text browser in splitter
        self.textView = InfoBrowser(self.splitView)
        self.connect(self.textView, PYSIGNAL('GameInfoSet'), self.selectGame)
        # i may eventually use the KHTMLPart instead
        # of the KTextBrowser
        #self.textView = InfoPart(self.splitView)
        # set main widget
        self.setCentralWidget(self.splitView)

        # setup dialog pointers
        self.new_game_dir_dialog = None
        self.add_new_game_dlg = None

        # here we add some methods to the dcop object
        self.app.dcop.addMethod('void selectGame (QString)',  self.selectGame)
        self.app.dcop.addMethod('void launchSelectedGame()', self.slotLaunchDosbox)
        
    
    # Should probably start putting these actions into a dict
    def initActions(self):
        collection = self.actionCollection()
        self.quitAction = KStdAction.quit(self.close, collection)
        # new genre probably won't be implemented
        #self.newGenreAction = NewGenre(self.slotNewGenre, collection)
        self.newGameAction = NewGame(self.slotNewGame, collection)
        self.launchDosboxAction = \
                                LaunchDosbox(self.slotLaunchDosbox, collection)
        self.launchDosboxPromptAction = \
                                      LaunchDosboxPrompt(self.slotLaunchDosboxPrompt,
                                                         collection)
        self.flatViewAction = FlatView(self.slotFlatView, collection)
        self.treeViewAction = TreeView(self.slotTreeView, collection)
        self.nameViewAction = NameView(self.slotNameView, collection)
        self.titleViewAction = TitleView(self.slotTitleView, collection)
        self.prepareAllGamesAction = \
                                   PrepareAllGames(self.slotPrepareAllGames, collection)
        self.cleanAllGamesAction = \
                                 CleanAllGames(self.slotCleanAllGames, collection)
        self.archiveAllGamesAction = \
                                   ArchiveAllGames(self.slotArchiveAllGames, collection)
        self.filterAllGamesAction = \
                                  FilterAllGames(self.slotFilterAllGames, collection)
        self.filterAvailableGamesAction = \
                                        FilterAvailableGames(self.slotFilterAvailableGames,
                                                             collection)
        self.filterUnavailableGamesAction = \
                                          FilterUnavailableGames(self.slotFilterUnavailableGames,
                                                                 collection)
        
        
    def initMenus(self):
        mainmenu = KPopupMenu(self)
        # new genre probably won't be implemented
        #self.newGenreAction.plug(mainmenu)
        self.newGameAction.plug(mainmenu)
        self.launchDosboxAction.plug(mainmenu)
        self.launchDosboxPromptAction.plug(mainmenu)
        mainmenu.insertSeparator()
        self.prepareAllGamesAction.plug(mainmenu)
        self.cleanAllGamesAction.plug(mainmenu)
        self.archiveAllGamesAction.plug(mainmenu)
        self.quitAction.plug(mainmenu)
        optionmenu = KPopupMenu(self)
        self.flatViewAction.plug(optionmenu)
        self.treeViewAction.plug(optionmenu)
        self.nameViewAction.plug(optionmenu)
        self.titleViewAction.plug(optionmenu)
        optionmenu.insertSeparator()
        self.filterAllGamesAction.plug(optionmenu)
        self.filterAvailableGamesAction.plug(optionmenu)
        self.filterUnavailableGamesAction.plug(optionmenu)
        self.menuBar().insertItem('&Main', mainmenu)
        self.menuBar().insertItem('&Options', optionmenu)
        self.menuBar().insertItem('&Help', self.helpMenu(''))

    def initToolbar(self):
        toolbar = self.toolBar()
        # new genre probably won't be implemented
        #self.newGenreAction.plug(toolbar)
        self.newGameAction.plug(toolbar)
        self.launchDosboxAction.plug(toolbar)
        self.launchDosboxPromptAction.plug(toolbar)
        self.quitAction.plug(toolbar)
        
    def refreshListView(self):
        self.refreshListView_common(KListViewItem)

    def _appendListItem(self, parent, name):
        self._appendListItem_common(parent, name, KListViewItem)
        
    # if this method is called externally, i.e. through dcop
    # we need to select the KListViewItem that matches also
    # if this method is not called externally, it means that the
    # listitem has already been selected
    def selectGame(self, name, called_externally=True):
            if called_externally:
                # if this method is called from dcop, name will be
                # a QString, so we make it python string
                name = str(name)
                if name not in self.game_names:
                    KMessageBox.error(self, '%s is not a valid game name.' % name)
                else:
                    if self.name_title_view is 'name':
                        # this is the easy part
                        # the 0 in the second arg means column
                        item = self.listView.findItem(name, 0)
                    else:
                        # we're using titles, so we have to get it
                        title = self.game_titles[name]
                        item = self.listView.findItem(title, 0)
                        # here True means select, False means unselect
                        self.listView.setSelected(item, True)
                        # calling setSelected will emit the selection changed signal
                        # which will result in this method being called again, although
                        # internally this time.

                        # here we make the selected item visible on the list
                        # if it's not currently visible
                        pos = item.itemPos()

                        item_pos = item.itemPos()
                        contentsY = self.listView.contentsY()
                        contentsHeight = self.listView.contentsHeight()
                        visibleHeight = self.listView.visibleHeight()
                        #print 'item pos', item_pos
                        #print 'contentsY', contentsY
                        #print 'contentsHeight', contentsHeight
                        #print 'visibleHeight', visibleHeight
                        # visible range = contentsY + visibleHeight
                        visible_range = range(contentsY, contentsY + visibleHeight)
                        if item_pos not in visible_range:
                            self.listView.setContentsPos(0, 0)
                            self.listView.scrollBy(0, pos)
            else:
                # we only change the textView for internal calls
                self.textView.set_game_info(name)
                
    def slotNewGame(self):
        if self.new_game_dir_dialog is None:
            dlg = KDirSelectDialog(self.config.get('DEFAULT', 'main_dosbox_path'), 0, self)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.select_new_game_path)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_new_game_dir_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_new_game_dir_dlg)
            dlg.show()
            self.new_game_dir_dialog = dlg
        else:
            KMessageBox.error(self, opendlg_errormsg)

    # new genre probably won't be implemented
    def slotNewGenre(self):
        KMessageBox.information(self,
                                'create new genre is unimplemented')

    def slotLaunchDosbox(self, game=None):
        self._launchdosbox_common(game, launch_game=True)

    def slotLaunchDosboxPrompt(self, game=None):
        self._launchdosbox_common(game, launch_game=False)

    def _launchdosbox_common(self, game, launch_game=True):
        if game is None:
            game = self.listView.currentItem().game
        if self.app.game_fileshandler.get_game_status(game):
            if launch_game:
                self.app.dosbox.run_game(game)
            else:
                self.app.dosbox.launch_dosbox_prompt(game)
        else:
            title = self.game_titles[game]
            KMessageBox.error(self, '%s is unavailable' % title)

            
    def select_new_game_path(self):
        url = self.new_game_dir_dialog.url()
        fullpath = str(url.path())
        name = os.path.basename(fullpath)
        if name not in self.game_names:
            print name, fullpath, self.game_names
            if self.add_new_game_dlg is None:
                dlg = AddNewGameDialog(self, fullpath)
                dlg.connect(dlg, SIGNAL('okClicked()'), self.add_new_game)
                dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_add_new_game_dlg)
                dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_add_new_game_dlg)
                dlg.show()
                self.add_new_game_dlg = dlg
        else:
            KMessageBox.error(self, '%s already exists.' % name)
        self.new_game_dir_dialog = None

    def _report_add_to_installed_archive(self, filename, count, total):
        dlg = self._add_to_installed_archive_progress
        progress = dlg.progressBar()
        if dlg.total is None:
            dlg.total = total
            progress.setTotalSteps(total)
        dlg.setLabel('Adding %s to archive.' % filename)
        progress.setProgress(count)
        self.app.processEvents()
        
    def add_new_game(self):
        dlg = self.add_new_game_dlg
        gamedata = dlg.get_gamedata_from_entries()
        name = gamedata['name']
        fullpath = dlg.fullpath
        dlg.close()
        ### ugly section -- testing now -- cleanup later
        filehandler = self.app.game_fileshandler
        filehandler._report_add_to_installed_archive = self._report_add_to_installed_archive
        self._add_to_installed_archive_progress = BaseProgressDialog(self)
        dlg = self._add_to_installed_archive_progress
        dlg.resize(400, 200)
        dlg.total = None
        dlg.show()
        ##### end of ugly section
        try:
            self.add_new_game_common(gamedata, fullpath)
        except ExistsError, inst:
            print 'here we are', inst
            KMessageBox.error(self, '%s already exists' % inst.args)
        dlg.close()
        
    # here action is either 'cleanup_game'
    # or 'prepare_game'
    def _perform_multigame_action(self, gamelist, action):
        fhandler = self.app.game_fileshandler
        if not hasattr(fhandler, action):
            raise StandardError, 'no %s attribute for game_fileshandler' % action
        num_games = len(gamelist)
        real_action = getattr(fhandler, action)
        dlg = MultiGameProgressDialog(self)
        dlg.resize(400, 200)
        if action == 'prepare_game':
            dlg.game_action = 'Prepare'
        elif action == 'cleanup_game':
            dlg.game_action = 'Clean up'
            
        progress = dlg.progressBar()
        progress.setTotalSteps(num_games)
        dlg.show()
        index = 1
        for game in gamelist:
            print "PERFORM %s on %s, index %d" % (action, game, index)
            progress.setProgress(index)
            title = self.game_titles[game]
            dlg.set_label(title)
            self.app.processEvents()
            real_action(game)
            index += 1
        dlg.close()
        
        
if __name__ == '__main__':
    print "testing module"
    
