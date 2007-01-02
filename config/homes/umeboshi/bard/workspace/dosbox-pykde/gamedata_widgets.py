import os
from qt import SIGNAL, SLOT
from qt import QGridLayout
from qt import QLabel
from qt import QFrame

from kdecore import KApplication


from kdeui import KMessageBox
from kdeui import KLineEdit
from kdeui import KTextEdit
from kdeui import KPushButton
from kdeui import KDialogBase

from kfile import KFileDialog

opendlg_errormsg = 'There is already a dialog box open.  Close it or restart the program'

class GameDataLayout(QGridLayout):
    def __init__(self, parent, name='AddNewGameLayout'):
        nrows = 2
        ncols = 2
        margin = 0
        space = 1
        QGridLayout.__init__(self, parent, nrows, ncols, margin, space, name)
        # setup app pointer
        self.app = KApplication.kApplication()
        self.config = self.app.config
        # setup dialog pointers
        self.select_launch_command_dlg = None
        self.select_title_screenshot_dlg = None
        # Setup widgets
        # setup name widgets
        self.name_lbl = QLabel('<b>Name</b>', parent)
        self.name_entry = KLineEdit('', parent)
        # add name widgets
        self.addWidget(self.name_lbl, 0, 0)
        self.addWidget(self.name_entry, 1, 0)
        # setup fullname widgets
        self.fullname_lbl = QLabel('<b>Full name</b>', parent)
        self.fullname_entry = KLineEdit('', parent)
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
        self.launch_entry = KLineEdit('', parent)
        self.launch_dlg_button = KPushButton('...', parent, 'launch_dlg_button')
        self.launch_dlg_button.connect(self.launch_dlg_button, SIGNAL('clicked()'),
                                       self.select_launch_command)
        # add launch command widgets
        self.addWidget(self.launch_lbl, 0, 1)
        self.addWidget(self.launch_entry, 1, 1)
        self.addWidget(self.launch_dlg_button, 1, 2)
        # setup dosboxpath widgets
        self.dosboxpath_lbl = QLabel('<b>dosbox path</b>', parent)
        self.dosboxpath_entry = KLineEdit('', parent)
        # add dosboxpath widgets
        self.addWidget(self.dosboxpath_lbl, 2, 1)
        self.addWidget(self.dosboxpath_entry, 3, 1)
        # setup title_screenshot widgets
        # I don't really know if I want these here yet.
        self.title_screenshot_lbl = QLabel('<b>Title Screenshot</b>', parent)
        self.title_screenshot_entry = KLineEdit('', parent)
        self.title_screenshot_dlg_button = KPushButton('...', parent,
                                                       'title_screenshot_dlg_button')
        self.title_screenshot_dlg_button.connect(self.title_screenshot_dlg_button,
                                                 SIGNAL('clicked()'),
                                                 self.select_title_screenshot)
        # add title_screenshot widgets
        self.addWidget(self.title_screenshot_lbl, 4, 1)
        self.addWidget(self.title_screenshot_entry, 5, 1)
        self.addWidget(self.title_screenshot_dlg_button, 5, 2)
        
    
    def select_launch_command(self):
        if self.select_launch_command_dlg is None:
            file_filter = "*.exe *.bat *.com|Dos Executables\n*|All Files"
            parent = self.parent()
            dlg = KFileDialog(self.fullpath, file_filter,  parent, 'select_launch_command_dlg', True)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.launch_command_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_select_launch_command_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_select_launch_command_dlg)
            dlg.show()
            self.select_launch_command_dlg = dlg
        else:
            # we shouldn't need this with a modal dialog
            KMessageBox.error(self.parent(), opendlg_errormsg)

    def select_title_screenshot(self):
        if self.select_title_screenshot_dlg is None:
            file_filter = "*.png|PNG Images\n*|All Files"
            # setting the name like this is sort of ugly
            name = str(self.name_entry.text())
            parent = self.parent()
            path = self.app.dosbox.get_capture_path(name)
            dlg = KFileDialog(path, file_filter, parent, 'select_title_screenshot_dlg', True)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.title_screenshot_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.show()
            self.select_title_screenshot_dlg = dlg
        else:
            # we shouldn't need this with a modal dialog
            KMessageBox.error(self.parent(), opendlg_errormsg)
            
    def destroy_select_launch_command_dlg(self):
        self.select_launch_command_dlg = None

    def destroy_select_title_screenshot_dlg(self):
        self.select_title_screenshot_dlg = None
        
    def title_screenshot_selected(self):
        dlg = self.select_title_screenshot_dlg
        url = dlg.selectedURL()
        fullpath = str(url.path())
        # setting the name like this is sort of ugly
        name = str(self.name_entry.text())
        handler = self.app.game_datahandler
        handler.make_title_screenshot(name, fullpath)
        
        
    def launch_command_selected(self):
        dlg = self.select_launch_command_dlg
        url = dlg.selectedURL()
        fullpath = str(url.path())
        launch_command = os.path.basename(fullpath)
        self.launch_entry.setText(launch_command)
        self.select_launch_command_dlg = None

class BaseGameDataDialog(KDialogBase):
    def __init__(self, parent, name='BaseGameDataDialog'):
        KDialogBase.__init__(self, parent, name)
        # setup app pointer
        self.app = KApplication.kApplication()
        self.config = self.app.config
        self.resize(*self.config.get_xy('gamedata_dialog', 'dialog_size'))
        # we need a frame for the layout widget
        # the layout widget won't work with a window as parent
        self._frame = QFrame(self)
        # set frame as main widget
        self.setMainWidget(self._frame)
        # now place layout with frame as parent
        self.grid = GameDataLayout(self._frame)

    def _fill_layout(self, gamedata):
        self.grid.name_entry.setText(gamedata['name'])
        self.grid.fullname_entry.setText(gamedata['fullname'])
        self.grid.desc_entry.setText(gamedata['description'])
        self.grid.launch_entry.setText(gamedata['launchcmd'])
        self.grid.dosboxpath_entry.setText(gamedata['dosboxpath'])

    def get_gamedata_from_entries(self):
        # setup keys for gamedata
        name = str(self.grid.name_entry.text())
        fullname = str(self.grid.fullname_entry.text())
        desc = str(self.grid.desc_entry.text())
        dosboxpath = str(self.grid.dosboxpath_entry.text())
        launchcmd = str(self.grid.launch_entry.text())
        # fill gamedata
        gamedata = dict(name=name, fullname=fullname,
                        description=desc, dosboxpath=dosboxpath,
                        launchcmd=launchcmd)
        return gamedata
    
class AddNewGameDialog(BaseGameDataDialog):
    def __init__(self, parent, fullpath, name='AddNewGameDialog'):
        BaseGameDataDialog.__init__(self, parent, name)
        self.fullpath = fullpath
        self.grid.fullpath = fullpath
        self._prefill_game_data()
        
    def _prefill_game_data(self):
        # setup some simple default values
        shortname = os.path.basename(self.fullpath)
        fullname = shortname.capitalize()
        launchcmd = '%s.exe' % shortname
        description = ''
        main_dosboxpath = self.config.get('DEFAULT', 'main_dosbox_path')
        if not self.fullpath.startswith(main_dosboxpath):
            raise ValueError, '%s is not contained in %s' % (self.fullpath, main_dosboxpath)
        dosboxpath = self.fullpath.split(main_dosboxpath)[1]
        while dosboxpath.startswith('/'):
            dosboxpath = dosboxpath[1:]
        gamedata = dict(name=shortname, fullname=fullname,
                        launchcmd=launchcmd, description=description,
                        dosboxpath=dosboxpath)
        self._fill_layout(gamedata)
        
            
class EditGameDataDialog(BaseGameDataDialog):
    def __init__(self, parent, game, name='EditGameDataDialog'):
        BaseGameDataDialog.__init__(self, parent, name)
        self.handler = self.app.game_datahandler
        gamedata = self.handler.get_game_data(game)
        self.grid.fullpath = os.path.join(self.app.main_dosbox_path, gamedata['dosboxpath'])
        self._fill_layout(gamedata)
        self.connect(self, SIGNAL('okClicked()'), self.update_gamedata)

    def update_gamedata(self):
        gamedata = self.get_gamedata_from_entries()
        self.handler.update_game_data(gamedata)
        KMessageBox.information(self, 'Data updated for %s' % gamedata['fullname'])
        
    

        
        

if __name__ == '__main__':
    print "testing gamedata_widgets module"
    
