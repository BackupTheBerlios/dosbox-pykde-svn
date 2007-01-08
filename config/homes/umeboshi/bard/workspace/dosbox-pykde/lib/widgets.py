import os
from qt import SIGNAL, SLOT
from qt import QSplitter
from qt import QGridLayout
from qt import QLabel
from qt import QFrame

from kdecore import KAboutData
from kdecore import KApplication


from kdeui import KAboutDialog
from kdeui import KMainWindow
from kdeui import KListView, KListViewItem
from kdeui import KTextBrowser
from kdeui import KMessageBox
from kdeui import KLineEdit
from kdeui import KDialogBase
from kdeui import KStdAction
from kdeui import KPopupMenu
from kdeui import KTextEdit
from kdeui import KPushButton
from kdeui import KProgressDialog

from kfile import KDirSelectDialog
from kfile import KFileDialog

from khtml import KHTMLPart

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

from infodoc import BaseDocument
from gamedata_widgets import AddNewGameDialog
from gamedata_widgets import EditGameDataDialog

# testing this one
from dcopexport import DCOPExObj

# this is the handler that can be used through dcop
# we will attach this to the app object
# we won't add methods here, because they may not
# be reachable yet.
# we will use the .app objects in the widgets
# then call self.app.dcop.addMethod('Qstring foo(QSomething)', self.say_something)
# in that object.
class DosboxHandler(DCOPExObj):
    def __init__(self, id='dosbox-handler'):
        DCOPExObj.__init__(self, id)
        

# would like to use this class, but don't
# understand how to connect url clicks
class InfoPart(KHTMLPart):
    def __init__(self, parent, name='InfoPart'):
        KHTMLPart.__init__(self, parent, name)
        # setup app pointer
        self.app = KApplication.kApplication()
        self.doc = BaseDocument(self.app)
        self.connect(self, SIGNAL('onURL(QString)'), self.setSource)
        #self.connect(self, SIGNAL('urlSelected(QString)'), self.setSource)
                
    def set_game_info(self, name):
        self.begin()
        self.doc.set_info(name)
        self.write(self.doc.output())
        self.end()

    def setSource(self, *args):
        print 'setSource called', args
    # this is selected when a url is clicked
    def setSourceOK(self, url):
        #action, key, filename = split_url(url)
        action, name = split_url(url)
        print action, name
        filehandler = self.app.game_fileshandler
        if action == 'cleanup':
            filehandler.cleanup_game(name)
        elif action == 'prepare':
            filehandler.prepare_game(name)

        self.set_game_info(name)
        
# text browser for game info
# uses html
# setSource method handles links, but kde-apidocs
# recommend not using this method
class InfoBrowser(KTextBrowser):
    def __init__(self, parent, name='InfoBrowser'):
        KTextBrowser.__init__(self, parent, name)
        self.app = KApplication.kApplication()
        self.setNotifyClick(True)
        self.doc = BaseDocument(self.app)
        # setup dialog pointers
        self.select_title_screenshot_dlg = None
        
    def set_game_info(self, name):
        # the following two lines used to work fine
        # but don't now
        #self.doc.set_info(name)
        #self.setText(self.doc.output())
        # so instead we do this quick hack
        # make a new document
        self.doc = BaseDocument(self.app)
        # display empty document
        self.setText(self.doc.output())
        # continue with what used to work
        self.doc.set_info(name)
        self.setText(self.doc.output())
        
    # this is selected when a url is clicked
    def setSource(self, url):
        #action, key, filename = split_url(url)
        action, name = split_url(url)
        filehandler = self.app.game_fileshandler
        if action == 'cleanup':
            filehandler.cleanup_game(name)
        elif action == 'prepare':
            filehandler.prepare_game(name)
        elif action == 'edit':
            dlg = EditGameDataDialog(self, name)
            dlg.show()
        elif action == 'set_title_screenshot':
            self.select_title_screenshot(name)
        elif action == 'open_weblink':
            # get gamedata from doc object
            # to keep from excessive xml parsing
            gamedata = self.doc.gamedata
            cmd = self.app.config.get('DEFAULT', 'launch_weblink')
            # for these url's, the name is the site
            weblink_url = gamedata['weblinks'][name]
            if '%s' in cmd:
                os.system(cmd % weblink_url)
            else:
                os.system("%s '%s'" % (cmd, weblink_url))
            # now we reset the name variable to reset the page properly
            name = gamedata['name']
        else:
            KMessageBox.error(self, '%s is unimplemented.' % action)
        # refresh the page
        self.set_game_info(name)
        # need to emit signal here for mainwin to pick up
        # this method is ugly
        if action in ['cleanup', 'prepare', 'edit']:
            mainwin = self.parent().parent()
            mainwin.refreshListView()
            
                        
    def select_title_screenshot(self, name):
        if self.select_title_screenshot_dlg is None:
            file_filter = "*.png|PNG Images\n*|All Files"
            path = self.app.dosbox.get_capture_path(name)
            dlg = KFileDialog(path, file_filter, self, 'select_title_screenshot_dlg', True)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.title_screenshot_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.game_name = name
            dlg.show()
            self.select_title_screenshot_dlg = dlg
        else:
            # we shouldn't need this with a modal dialog
            KMessageBox.error(self, opendlg_errormsg)

    def title_screenshot_selected(self):
        print 'screenshot selected'
        dlg = self.select_title_screenshot_dlg
        url = dlg.selectedURL()
        fullpath = str(url.path())
        print 'screenshot at', fullpath
        name = dlg.game_name
        handler = self.app.game_datahandler
        handler.make_title_screenshot(name, fullpath)
        self.destroy_select_title_screenshot_dlg()
        self.set_game_info(name)
        
    def destroy_select_title_screenshot_dlg(self):
        self.select_title_screenshot_dlg = None
        
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
        # place dcop object here
        self.dcop = DosboxHandler()      

    def quit(self):
        KApplication.quit(self)

# main window class
class MainWindow(KMainWindow):
    def __init__(self, parent):
        KMainWindow.__init__(self, parent, 'PyKDE Dosbox Frontend')
        # setup app pointer
        self.app = KApplication.kApplication()
        self.config = self.app.config
        self.resize(*self.config.get_xy('mainwindow', 'mainwindow_size'))
        # initialize game data
        self.initialize_important_game_data()
        self._treedict = {}
        self._show_filter = 'all'
        # setup default view options
        self.flat_tree_view = self.config.get('mainwindow', 'flat_tree_view')
        self.name_title_view = self.config.get('mainwindow', 'name_title_view')
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
        # try to resize splitter
        # this is a kind of ugly hack, but seems to work ok
        x, y = self.config.get_xy('mainwindow', 'mainwindow_size')
        self.splitView.setSizes([int(.1*x), int(.9*x)])
        # setup signals
        self.connect(self.listView,
                     SIGNAL('selectionChanged()'), self.selectionChanged)
        
        # place text browser in splitter
        self.textView = InfoBrowser(self.splitView)
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
        
    def initlistView(self):
        # the -1 is to set the column's WidthMode to Maximum instead of Manual
        self.listView.addColumn('games', -1)
        self.refreshListView()

    def initialize_important_game_data(self):
        self.game_titles = {}
        self.game_paths = {}
        handler = self.app.game_datahandler
        self.game_names = handler.get_game_names()
        for game in self.game_names:
            gamedata = handler.get_game_data(game)
            self.game_titles[game] = gamedata['fullname']
            self.game_paths[game] = gamedata['dosboxpath']

    def update_important_game_data(self, name):
        handler = self.app.game_datahandler
        gamedata = handler.get_game_data(name)
        self.game_titles[name] = gamedata['fullname']
        self.game_paths[name] = gamedata['dosboxpath']
        if name not in self.game_names:
            self.game_names.append(name)
            self.game_names.sort()

    def _appendListItem(self, parent, name):
        if self.name_title_view == 'name':
            item_label = name
        else:
            item_label = self.game_titles[name]
        item = None
        if self._show_filter == 'all':
            item = KListViewItem(parent, item_label)
        else:
            fhandler = self.app.game_fileshandler
            available = fhandler.get_game_status(name)
            if self._show_filter == 'available':
                if available:
                    item = KListViewItem(parent, item_label)
            elif self._show_filter == 'unavailable':
                if not available:
                    item = KListViewItem(parent, item_label)
        if item is not None:
            item.game = name
        
    def refreshListView(self):
        self.listView.clear()
        # the tree view option may get too long
        # with a large number of games.  I have tried
        # to make this fairly quick for a small number of
        # directories, but a lot of directories will almost
        # surely slow it down.
        if self.flat_tree_view == 'tree':
            self._treedict = {}
            self.listView.setRootIsDecorated(True)
            for name in self.game_names:
                path = self.game_paths[name]
                # basename should always equal name
                # we only need the dirname
                dirname, basename = os.path.split(path)
                dirs = dirname.split('/')
                parent = None
                for adir in dirs:
                    if parent is None:
                        if adir not in self._treedict:
                            self._treedict[adir] = KListViewItem(self.listView, adir)
                            self._treedict[adir].dirname = adir
                        parent = self._treedict[adir]
                    else:
                        path = os.path.join(parent.dirname, adir)
                        if path not in self._treedict:
                            self._treedict[path] = KListViewItem(parent, adir)
                            self._treedict[path].dirname = path
                        parent = self._treedict[path]
                self._appendListItem(self._treedict[dirname], basename)            
        else:
            self.listView.setRootIsDecorated(False)
            for game in self.game_names:
                self._appendListItem(self.listView, game)
            
    def selectionChanged(self):
        item = self.listView.currentItem()
        if hasattr(item, 'game'):
            self.selectGame(item.game, called_externally=False)

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
            else:
                # we only change the textView for internal calls
                self.textView.set_game_info(name)
                
    # Should probably start putting these actions into a dict
    def initActions(self):
        collection = self.actionCollection()
        self.quitAction = KStdAction.quit(self.close, collection)
        # new genre probably won't be implemented
        #self.newGenreAction = NewGenre(self.slotNewGenre, collection)
        self.newGameAction = NewGame(self.slotNewGame, collection)
        self.launchDosboxAction = LaunchDosbox(self.slotLaunchDosbox, collection)
        self.flatViewAction = FlatView(self.slotFlatView, collection)
        self.treeViewAction = TreeView(self.slotTreeView, collection)
        self.nameViewAction = NameView(self.slotNameView, collection)
        self.titleViewAction = TitleView(self.slotTitleView, collection)
        self.prepareAllGamesAction = PrepareAllGames(self.slotPrepareAllGames, collection)
        self.cleanAllGamesAction = CleanAllGames(self.slotCleanAllGames, collection)
        self.archiveAllGamesAction = ArchiveAllGames(self.slotArchiveAllGames, collection)
        self.filterAllGamesAction = FilterAllGames(self.slotFilterAllGames, collection)
        self.filterAvailableGamesAction = FilterAvailableGames(self.slotFilterAvailableGames,
                                                                   collection)
        self.filterUnavailableGamesAction = FilterUnavailableGames(self.slotFilterUnavailableGames,
                                                                   collection)
        
        
    def initMenus(self):
        mainmenu = KPopupMenu(self)
        # new genre probably won't be implemented
        #self.newGenreAction.plug(mainmenu)
        self.newGameAction.plug(mainmenu)
        self.launchDosboxAction.plug(mainmenu)
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
            KMessageBox.error(self, opendlg_errormsg)

    def destroy_new_game_dir_dlg(self):
        self.new_game_dir_dialog = None

    def destroy_add_new_game_dlg(self):
        self.add_new_game_dlg = None
        
    # new genre probably won't be implemented
    def slotNewGenre(self):
        KMessageBox.information(self,
                                'create new genre is unimplemented')

    def slotLaunchDosbox(self, game=None):
        if game is None:
            game = self.listView.currentItem().game
        if self.app.game_fileshandler.get_game_status(game):
            self.app.dosbox.run_game(game)
        else:
            title = self.game_titles[game]
            KMessageBox.error(self, '%s is unavailable' % title)
        
    def select_new_game_path(self):
        url = self.new_game_dir_dialog.url()
        fullpath = str(url.path())
        name = os.path.basename(fullpath)
        if name not in self.game_names:
            print name, fullpath
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
            
    def add_new_game(self):
        print 'add_new_game'
        dlg = self.add_new_game_dlg
        gamedata = dlg.get_gamedata_from_entries()
        name = gamedata['name']
        if name not in self.game_names:
            # add game to data handler
            handler = self.app.game_datahandler
            handler.add_new_game(gamedata)
            # archive as fresh install
            filehandler = self.app.game_fileshandler
            filehandler.archive_fresh_install(name)
            # update quick reference dictionaries
            self.update_important_game_data(name)
            # update the list
            self.refreshListView()
            # now we should be done with this dialog
        else:
            KMessageBox.error(self, '%s already exists.' % name)
        self.add_new_game_dlg = None
        
    def slotFlatView(self):
        #KMessageBox.information(self, 'set to flat view')
        self.flat_tree_view = 'flat'
        self.refreshListView()
        
    def slotTreeView(self):
        #KMessageBox.information(self, 'set to tree view')
        self.flat_tree_view = 'tree'
        self.refreshListView()
        
    def slotNameView(self):
        #KMessageBox.information(self, 'set to name view')
        self.name_title_view = 'name'
        self.refreshListView()
        
    def slotTitleView(self):
        #KMessageBox.information(self, 'set to title view')
        self.name_title_view = 'title'
        self.refreshListView()

    def _available_games(self):
        fhandler = self.app.game_fileshandler
        return [g for g in self.game_names if fhandler.game_is_available(g)]

    def _unavailable_games(self):
        fhandler = self.app.game_fileshandler
        return [g for g in self.game_names if not fhandler.game_is_available(g)]
    
    def _prepare_games_orig(self, gamelist):
        fhandler = self.app.game_fileshandler
        for game in gamelist:
            fhandler.prepare_game(game)

    def _clean_games_orig(self, gamelist):
        fhandler = self.app.game_fileshandler
        for game in gamelist:
            fhandler.cleanup_game(game)

    def _clean_games(self, gamelist):
        self._perform_multigame_action(gamelist, 'cleanup_game')
        
    def _prepare_games(self, gamelist):
        self._perform_multigame_action(gamelist, 'prepare_game')
        
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
            
        
    def slotPrepareAllGames(self):
        missing = self._unavailable_games()
        self._prepare_games(missing)

    def slotCleanAllGames(self):
        available = self._available_games()
        self._clean_games(available)

    def slotArchiveAllGames(self):
        available = self._available_games()
        self._clean_games(available)
        self._prepare_games(available)

    def slotFilterAllGames(self):
        self._show_filter = 'all'
        self.refreshListView()
        
    def slotFilterAvailableGames(self):
        self._show_filter = 'available'
        self.refreshListView()

    def slotFilterUnavailableGames(self):
        self._show_filter = 'unavailable'
        self.refreshListView()

class BaseProgressDialog(KProgressDialog):
    def __init__(self, parent, name='BaseProgressDialog'):
        KProgressDialog.__init__(self, parent, name)

# make a progress dialog for operations spanning
# multiple games
class MultiGameProgressDialog(BaseProgressDialog):
    def set_label(self, game):
        message = '%s game <b>%s</b>' % (self.game_action, game)
        self.setLabel(message)
    


if __name__ == '__main__':
    print "testing module"
    
