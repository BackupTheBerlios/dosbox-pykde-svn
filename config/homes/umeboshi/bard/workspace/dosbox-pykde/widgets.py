import os
from qt import SIGNAL, SLOT
from qt import QSplitter
from qt import qApp
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

from kfile import KDirSelectDialog
from kfile import KFileDialog

from base import split_url
from actions import NewGenre, NewGame, LaunchDosbox
from actions import NameView, TitleView
from actions import FlatView, TreeView

from infodoc import BaseDocument

opendlg_errormsg = 'There is already a dialog box open.  Close it or restart the program'

class AddNewGameLayout(QGridLayout):
    def __init__(self, parent, fullpath, name='AddNewGameLayout'):
        nrows = 2
        ncols = 2
        margin = 0
        space = 1
        QGridLayout.__init__(self, parent, nrows, ncols, margin, space, name)
        self.config = KApplication.kApplication().config
        self.fullpath = fullpath
        shortname = os.path.basename(self.fullpath)
        # setup dialog pointers
        self.select_launch_command_dlg = None

        # Setup widgets
        # setup name widgets
        self.name_lbl = QLabel('<b>Name</b>', parent)
        self.name_entry = KLineEdit(shortname, parent)
        # add name widgets
        self.addWidget(self.name_lbl, 0, 0)
        self.addWidget(self.name_entry, 1, 0)
        # setup fullname widgets
        self.fullname_lbl = QLabel('<b>Full name</b>', parent)
        self.fullname_entry = KLineEdit(shortname.capitalize(), parent)
        # add fullname widgets
        self.addWidget(self.fullname_lbl, 2, 0)
        self.addWidget(self.fullname_entry, 3, 0)
        # setup description widgets
        self.desc_lbl = QLabel('<b>Description</b>', parent)
        self.desc_entry = KTextEdit(parent, 'description_entry')
        # add description widgets
        self.addWidget(self.desc_lbl, 4, 0)
        self.addWidget(self.desc_entry, 5, 0)
        # setup launch command widgets
        self.launch_lbl = QLabel('<b>Launch command</b>', parent)
        self.launch_entry = KLineEdit('%s.exe' % shortname, parent)
        self.launch_dlg_button = KPushButton('...', parent, 'launch_dlg_button')
        self.launch_dlg_button.connect(self.launch_dlg_button, SIGNAL('clicked()'),
                                       self.select_launch_command)
        # add launch command widgets
        self.addWidget(self.launch_lbl, 0, 1)
        self.addWidget(self.launch_entry, 1, 1)
        self.addWidget(self.launch_dlg_button, 1, 2)
        # setup dosboxpath widgets
        self.dosboxpath_lbl = QLabel('<b>dosbox path</b>', parent)
        main_dbox_path = self.config.get('DEFAULT', 'main_dosbox_path')
        if not self.fullpath.startswith(main_dbox_path):
            raise ValueError, '%s is not contained in %s' % (self.fullpath, main_dbox_path)
        dbox_path = self.fullpath.split(main_dbox_path)[1]
        while dbox_path.startswith('/'):
            dbox_path = dbox_path[1:]
        self.dosboxpath_entry = KLineEdit(dbox_path, parent)
        # add dosboxpath widgets
        self.addWidget(self.dosboxpath_lbl, 2, 1)
        self.addWidget(self.dosboxpath_entry, 3, 1)
        
        
    def select_launch_command(self):
        if self.select_launch_command_dlg is None:
            file_filter = "*.exe *.bat *.com|Dos Executables\n*|All Files"
            dlg = KFileDialog(self.fullpath, file_filter,  self.parent(), 'select_launch_command_dlg', True)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.launch_command_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_select_launch_command_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_select_launch_command_dlg)
            dlg.show()
            self.select_launch_command_dlg = dlg
        else:
            # we shouldn't need this with a modal dialog
            KMessageBox.error(self.parent(), opendlg_errormsg)

    def destroy_select_launch_command_dlg(self):
        self.select_launch_command_dlg = None

    def launch_command_selected(self):
        dlg = self.select_launch_command_dlg
        url = dlg.selectedURL()
        fullpath = str(url.path())
        launch_command = os.path.basename(fullpath)
        self.launch_entry.setText(launch_command)
        self.select_launch_command_dlg = None
        
class AddNewGameDialog(KDialogBase):
    def __init__(self, parent, fullpath, name='AddNewGameDialog'):
        KDialogBase.__init__(self, parent, name)
        self.resize(400, 300)
        self.fullpath = fullpath
        self._frame = QFrame(self)
        self.setMainWidget(self._frame)
        self.grid = AddNewGameLayout(self._frame, self.fullpath)
        
# text browser for game info
class InfoBrowser(KTextBrowser):
    def __init__(self, parent):
        KTextBrowser.__init__(self, parent)
        self.app = KApplication.kApplication()
        self.setNotifyClick(True)
        self.doc = BaseDocument(self.app)

    def set_game_info(self, name):
        self.doc.set_info(name)
        self.setText(self.doc.output())
        
    # this is selected when a url is clicked
    def setSource(self, url):
        #action, key, filename = split_url(url)
        action, name = split_url(url)
        print action, name
        filehandler = self.app.game_fileshandler
        if action == 'cleanup':
            filehandler.cleanup_game(name)
        elif action == 'prepare':
            filehandler.prepare_game(name)

        self.set_game_info(name)
        
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
        # setup app pointer
        self.app = KApplication.kApplication()
        self.config = self.app.config
        self.resize(*self.config.get_xy('mainwindow', 'mainwindow_size'))
        # initialize game data
        self.initialize_important_game_data()
        self._treedict = {}
        # setup default view options
        self.flat_tree_view = 'flat'
        self.name_title_view = 'name'
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
        # set main widget
        self.setCentralWidget(self.splitView)

        # setup dialog pointers
        self.new_game_dir_dialog = None
        self.add_new_game_dlg = None
        
    def initlistView(self):
        self.listView.addColumn('genre', -1)
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
            item = KListViewItem(parent, name)
        else:
            fullname = self.game_titles[name]
            item = KListViewItem(parent, fullname)
        item.game = name
        
    def refreshListView(self):
        self.listView.clear()
        #handler = self.app.game_datahandler
        #games = handler.get_game_names()
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
            self.textView.set_game_info(item.game)
        
    def initActions(self):
        collection = self.actionCollection()
        self.quitAction = KStdAction.quit(self.close, collection)
        self.newGenreAction = NewGenre(self.slotNewGenre, collection)
        self.newGameAction = NewGame(self.slotNewGame, collection)
        self.launchDosboxAction = LaunchDosbox(self.slotLaunchDosbox, collection)
        self.flatViewAction = FlatView(self.slotFlatView, collection)
        self.treeViewAction = TreeView(self.slotTreeView, collection)
        self.nameViewAction = NameView(self.slotNameView, collection)
        self.titleViewAction = TitleView(self.slotTitleView, collection)
        
        
    def initMenus(self):
        mainmenu = KPopupMenu(self)
        self.newGenreAction.plug(mainmenu)
        self.newGameAction.plug(mainmenu)
        self.launchDosboxAction.plug(mainmenu)
        self.quitAction.plug(mainmenu)
        optionmenu = KPopupMenu(self)
        self.flatViewAction.plug(optionmenu)
        self.treeViewAction.plug(optionmenu)
        self.nameViewAction.plug(optionmenu)
        self.titleViewAction.plug(optionmenu)
        self.menuBar().insertItem('&Main', mainmenu)
        self.menuBar().insertItem('&Options', optionmenu)
        self.menuBar().insertItem('&Help', self.helpMenu(''))

    def initToolbar(self):
        toolbar = self.toolBar()
        self.newGenreAction.plug(toolbar)
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
        
    def slotNewGenre(self):
        KMessageBox.information(self,
                                'create new genre')

    def slotLaunchDosbox(self):
        game = self.listView.currentItem().game
        self.app.dosbox.run_game(game)
        #KMessageBox.information(self, 'launch %s in dosbox' % game)
        
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
        # setup keys for gamedata
        name = str(dlg.grid.name_entry.text())
        if name not in self.game_names:
            fullname = str(dlg.grid.fullname_entry.text())
            desc = str(dlg.grid.desc_entry.text())
            dosboxpath = str(dlg.grid.dosboxpath_entry.text())
            launchcmd = str(dlg.grid.launch_entry.text())
            # fill gamedata
            gamedata = dict(name=name, fullname=fullname,
                            description=desc, dosboxpath=dosboxpath,
                            launchcmd=launchcmd)
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
    
if __name__ == '__main__':
    print "testing module"
    
