import os
from qt import SIGNAL, SLOT
from qt import PYSIGNAL
from qt import QSplitter
from qt import QTextDrag
from qt import QUriDrag
from qt import QStringList

from kdeui import KMainWindow
from kdeui import KListView, KListViewItem
from kdeui import KMessageBox
from kdeui import KStdAction
from kdeui import KPopupMenu
from kdeui import KStatusBar

from kfile import KDirSelectDialog

from dboxpykde.base import split_url
from dboxpykde.base import opendlg_errormsg
from dboxpykde.base import ExistsError


# import actions
from actions import NewGame
from actions import ImportZipFile

# launch dosbox actions
from actions import LaunchDosbox
from actions import LaunchDosboxPrompt
from actions import LaunchMainDosboxPrompt
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
# profile actions
from actions import ManageDosboxProfiles
from actions import SetCurrentProfile
# settings actions
from actions import ConfigureDosboxPyKDE


# import game data dialogs
from gamedata_widgets import AddNewGameDialog
from gamedata_widgets import EditGameDataDialog

# test import
#from gamedata_widgets import ImportGameDialog
from importgames import ImportGameUrlDialog
from importgames import ImportsMainWindow
from infobrowser import InfoBrowser
from infobrowser import InfoPart

# import settings widget
from settings import SettingsWidgetDialog

from progress_dialogs import MultiGameProgressDialog
# using BaseProgressDialog until a better class is made
from progress_dialogs import BaseProgressDialog

from dboxpykde.common.mainwindow import MainWindowCommon

from dosboxcfg.profile import ManageDosboxProfilesWindow
from dosboxcfg.profile import ProfileSelectorDialog

from base import get_application_pointer

# main window class
class MainWindow(MainWindowCommon, KMainWindow):
    def __init__(self, parent):
        KMainWindow.__init__(self, parent, 'PyKDE Dosbox Frontend')
        # setup app pointer
        self.app = get_application_pointer()
        self._init_common()
        self.setAcceptDrops(True)
        
        # place a splitter in the window
        self.splitView = QSplitter(self, 'splitView')
        # place a listview in the splitter (on the left)
        self.listView = KListView(self.splitView, 'games_view')
        # fill listview
        self.initlistView()
        # try to resize splitter
        # this is a kind of ugly hack, but seems to work ok
        x, y = self.myconfig.get_xy('mainwindow', 'mainwindow_size')
        self.splitView.setSizes([int(.1*x), int(.9*x)])
        # setup signals
        self.connect(self.listView,
                     SIGNAL('selectionChanged()'), self.selectionChanged)
        
        # place text browser in splitter
        #self.textView = InfoBrowser(self.splitView)
        # i may eventually use the KHTMLPart instead
        # of the KTextBrowser
        if self.app.myconfig.getboolean('mainwindow', 'use_khtml_part'):
            self.textView = InfoPart(self.splitView)
        else:
            self.textView = InfoBrowser(self.splitView)
        self.connect(self.textView, PYSIGNAL('GameInfoSet'), self.selectGame)

        self.statusbar = KStatusBar(self)
        self._set_current_profile(self.app.dosbox.current_profile)
        # set main widget
        self.setCentralWidget(self.splitView)

        # setup dialog pointers
        # it would be nice if I knew a better way to get
        # information from dialogs
        self.new_game_dir_dialog = None
        self.add_new_game_dlg = None
        self.set_profile_dlg = None
        
        # here we add some methods to the dcop object
        self.app.dcop.addMethod('void selectGame (QString)',  self.selectGame)
        self.app.dcop.addMethod('void launchSelectedGame()', self.slotLaunchDosbox)
        
    
    # Should probably start putting these actions into a dict
    def initActions(self):
        collection = self.actionCollection()
        self.quitAction = KStdAction.quit(self.close, collection)
        self.newGameAction = NewGame(self.slotNewGame, collection)
        self.importZipFileAction = ImportZipFile(self.slotImportZipFile, collection)
        self.launchDosboxAction = \
                                LaunchDosbox(self.slotLaunchDosbox, collection)
        self.launchDosboxPromptAction = \
                                      LaunchDosboxPrompt(self.slotLaunchDosboxPrompt,
                                                         collection)
        self.launchMainDosboxPromptAction = \
                                          LaunchMainDosboxPrompt(self.slotLaunchMainDosboxPrompt,
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
        self.manageDosboxProfilesAction = \
                                        ManageDosboxProfiles(self.slotManageDosboxProfiles,
                                                             collection)
        
        self.setCurrentProfileAction = \
                                     SetCurrentProfile(self.slotSetCurrentProfile,
                                                       collection)
        self.configureDosboxPyKDEAction = \
                                        ConfigureDosboxPyKDE(self.slotConfigureDosboxPyKDE,
                                                             collection)
        
    def initMenus(self):
        # make a new menu
        mainmenu = KPopupMenu(self)
        # plug import new game actions into the menu
        self.newGameAction.plug(mainmenu)
        self.importZipFileAction.plug(mainmenu)
        # insert a little line separating menu items
        mainmenu.insertSeparator()
        # plug launch dosbox actions into the menu
        self.launchDosboxAction.plug(mainmenu)
        self.launchDosboxPromptAction.plug(mainmenu)
        self.launchMainDosboxPromptAction.plug(mainmenu)
        # insert a little line separating menu items
        mainmenu.insertSeparator()
        # plug the rest of the main menu actions
        self.prepareAllGamesAction.plug(mainmenu)
        self.cleanAllGamesAction.plug(mainmenu)
        self.archiveAllGamesAction.plug(mainmenu)
        self.quitAction.plug(mainmenu)
        # make a profiles menu
        profilemenu = KPopupMenu(self)
        self.manageDosboxProfilesAction.plug(profilemenu)
        self.setCurrentProfileAction.plug(profilemenu)
        # make another menu for options
        viewmenu = KPopupMenu(self)
        self.flatViewAction.plug(viewmenu)
        self.treeViewAction.plug(viewmenu)
        self.nameViewAction.plug(viewmenu)
        self.titleViewAction.plug(viewmenu)
        viewmenu.insertSeparator()
        self.filterAllGamesAction.plug(viewmenu)
        self.filterAvailableGamesAction.plug(viewmenu)
        self.filterUnavailableGamesAction.plug(viewmenu)
        # make a settings menu
        settingsmenu = KPopupMenu(self)
        self.configureDosboxPyKDEAction.plug(settingsmenu)
        # get a pointer to the menubar in the main window
        # this method will create a menubar if one is not already
        # available
        menubar = self.menuBar()
        # place the menus on the menu bar (in order)
        menubar.insertItem('&Main', mainmenu)
        menubar.insertItem('&Profiles', profilemenu)
        menubar.insertItem('&View', viewmenu)
        menubar.insertItem('&Settings', settingsmenu)
        menubar.insertItem('&Help', self.helpMenu(''))

    def initToolbar(self):
        # get a pointer to the main toolbar in the main window
        # this method will create a toolbar if one is not already there.
        toolbar = self.toolBar()
        # add some actions to the toolbar
        self.newGameAction.plug(toolbar)
        self.importZipFileAction.plug(toolbar)
        self.launchMainDosboxPromptAction.plug(toolbar)
        self.launchDosboxAction.plug(toolbar)
        self.launchDosboxPromptAction.plug(toolbar)
        self.manageDosboxProfilesAction.plug(toolbar)
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
                    self._make_listitem_visible(item)
                    
        
            else:
                # we only change the textView for internal calls
                self.textView.set_game_info(name)
                
    # here we make the selected item visible on the list
    # if it's not currently visible
    def _make_listitem_visible(self, item):
        item_pos = item.itemPos()
        # contentsY is the position in the contents that
        # is at the top of the visible area
        contentsY = self.listView.contentsY()
        # contentsHeight is the height of the full list
        contentsHeight = self.listView.contentsHeight()
        # visibleHeight is the height of the visible part of the list
        visibleHeight = self.listView.visibleHeight()
        # visible_range is the interval defining the contents positions
        # that are visible
        visible_range = range(contentsY, contentsY + visibleHeight)
        # here we test whether the item position is in the range of
        # visible positions, and if not, we scroll the listview to make it so.
        if item_pos not in visible_range:
            self.listView.setContentsPos(0, 0)
            self.listView.scrollBy(0, item_pos)
            
    def slotNewGame(self):
        if self.new_game_dir_dialog is None:
            main_dosbox_path = self.myconfig.get('dosbox', 'main_dosbox_path')
            dlg = KDirSelectDialog(main_dosbox_path, 0, self)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.new_game_path_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_new_game_dir_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_new_game_dir_dlg)
            dlg.show()
            self.new_game_dir_dialog = dlg
        else:
            KMessageBox.error(self, opendlg_errormsg)

    def slotLaunchDosbox(self, game=None):
        self._launchdosbox_common(game, launch_game=True)

    def slotLaunchDosboxPrompt(self, game=None):
        self._launchdosbox_common(game, launch_game=False)

    def slotLaunchMainDosboxPrompt(self):
        KMessageBox.information(self, 'Not implemented')
        
    def slotManageDosboxProfiles(self):
        #from dosboxcfg.profile import ProfileDialogWindow
        #win = ProfileDialogWindow(self)
        win = ManageDosboxProfilesWindow(self)
        win.show()

    def slotSetCurrentProfile(self):
        dlg = ProfileSelectorDialog(self)
        self.connect(dlg, SIGNAL('okClicked()'), self._current_profile_selected)
        self.set_profile_dlg = dlg
        dlg.show()

    def slotImportZipFile(self):
        #KMessageBox.information(self, 'Import a new game, not yet implemented.')
        #dlg = ImportGameUrlDialog(self)
        
        #dlg.show()
        win = ImportsMainWindow(self)
        win.show()
        
    def slotConfigureDosboxPyKDE(self):
        #KMessageBox.information(self, 'ConfigureDosboxPyKDE')
        dlg = SettingsWidgetDialog(self)
        dlg.show()
        
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

    def _current_profile_selected(self):
        dlg = self.set_profile_dlg
        if dlg is not None:
            profile = dlg.get_selected_profile()
            self._set_current_profile(profile)
            self.set_profile_dlg = None
            
    def _set_current_profile(self, profile):
        dosbox = self.app.dosbox
        dosbox.set_current_profile(profile)
        msg = 'Current Profile:  %s' % dosbox.current_profile
        self.statusbar.message(msg)        
            
    def new_game_path_selected(self):
        # url is a KURL
        url = self.new_game_dir_dialog.url()
        # since the url should be file://path/to/game
        # we only want the /path/to/game
        fullpath = str(url.path())
        # here we set the name of the game to the base
        # directory of the path.  This is probably not a good
        # idea in the long run, and I'll change this behaviour one day.
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

    def _report_extract_from_installed_archive(self, filename, count, total):
        dlg = self.extract_from_installed_archive_progress
        progress = dlg.progressBar()
        if dlg.total is None:
            dlg.total = total
            progress.setTotalSteps(total)
        dlg.setLabel('Extracting %s from archive.' % filename)
        progress.setProgress(count)
        self.app.processEvents()
        
    def add_new_game(self):
        dlg = self.add_new_game_dlg
        gamedata = dlg.get_gamedata_from_entries()
        name = gamedata['name']
        fullpath = dlg.fullpath
        dlg.close()
        ### ugly section -- testing now -- cleanup later
        self.app.processEvents()
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
        if gamelist:
            dlg = MultiGameProgressDialog(self, action)
            dlg.resize(400, 200)
            dlg.show()
            dlg.perform_action(gamelist, self.game_titles)
            dlg.close()
        
    def dropEvent(self, event):
        #print 'in dropEvent', event
        qlist = QStringList()
        if QUriDrag.decodeToUnicodeUris(event, qlist):
            if len(qlist) == 1:
                url = qlist[0]
                dlg = ImportGameUrlDialog(self)
                dlg.url_entry.setText(url)
                dlg.show()
                
                
                
    def dragEnterEvent(self, event):
        #print 'in dragEnterEvent', event
        event.accept(QUriDrag.canDecode(event))
        
if __name__ == '__main__':
    print "testing module"
    
