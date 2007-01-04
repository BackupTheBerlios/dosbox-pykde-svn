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
        # make a couple of lists to point to the weblink entries
        self.weblink_site_entries = []
        self.weblink_url_entries = []
        # I may use dict[site] = (site_entry, url_entry)
        # I haven't decided yet.  It could always be formed by zipping the 2 lists above.
        self.weblink_dict = {}
        # setup app pointer
        self.app = KApplication.kApplication()
        self.config = self.app.config
        # setup dialog pointers
        self.select_launch_command_dlg = None
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
        #self.addWidget(self.desc_entry, 5, 0)
        # add the description as a multirow entity
        # default from 5 to 15
        # this allows for weblinks to be added
        # (about 5)
        # without the dialog looking ugly
        # going to 15 won't force there to be that many rows
        # until more enough widgets are added
        self.addMultiCellWidget(self.desc_entry, 5, 15, 0, 0)
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
        # setup main weblink widgets
        self.weblinks_lbl = QLabel('<b>weblinks</b>', parent)
        self.weblinks_btn = KPushButton('+', parent, 'add_weblink_button')
        self.weblinks_btn.connect(self.weblinks_btn, SIGNAL('clicked()'),
                                  self.add_weblink_entries)
        # add main weblink widgets
        self.addWidget(self.weblinks_lbl, 4, 1)
        self.addWidget(self.weblinks_btn, 4, 2)
        
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

    def destroy_select_launch_command_dlg(self):
        self.select_launch_command_dlg = None

    def launch_command_selected(self):
        dlg = self.select_launch_command_dlg
        url = dlg.selectedURL()
        fullpath = str(url.path())
        launch_command = os.path.basename(fullpath)
        self.launch_entry.setText(launch_command)
        self.select_launch_command_dlg = None

    def add_weblink_entries(self, site='', url=''):
        #we start at row #5 column 1 for lbl column 2 for entry
        parent = self.parent()
        num_entries = len(self.weblink_url_entries)
        # we need to add 1 on lbl_num because the entries can be appended
        # until instantiated
        lbl_num = num_entries + 1
        site_lbl = QLabel('<b>site %d</b>' % lbl_num, parent)
        site_entry = KLineEdit(site, parent)
        self.weblink_site_entries.append(site_entry)
        url_lbl = QLabel('<b>url %d</b>' % lbl_num, parent)
        url_entry = KLineEdit(url, parent)
        self.weblink_url_entries.append(url_entry)
        if len(self.weblink_site_entries) != len(self.weblink_url_entries):
            KMessageBox.error('entries mismatch, something really bad happened.')
            import sys
            sys.exit(1)
        # we need a little math here to figure out the rows
        # for the widgets
        # num_entries should now be 1 greater than above
        num_entries = len(self.weblink_url_entries)
        site_row = 2*num_entries + 3
        url_row = 2*num_entries + 4
        # add weblink widgets
        top = self.AlignTop
        self.addWidget(site_entry, site_row, 1)
        self.addWidget(site_lbl, site_row, 2)
        self.addWidget(url_entry, url_row, 1)
        self.addWidget(url_lbl, url_row, 2)
        # we have to call .show() explicitly on the widgets
        # as the rest of the widgets are already visible
        # when show was called on the dialog
        # show() automatically calls show() on all children
        for widget in [site_lbl, site_entry, url_lbl, url_entry]:
            widget.show()
        
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
        # remember the weblinks
        sites = gamedata['weblinks'].keys()
        sites.sort()
        for site in sites:
            self.grid.add_weblink_entries(site, gamedata['weblinks'][site])
            
    def get_gamedata_from_entries(self):
        # setup keys for gamedata
        name = str(self.grid.name_entry.text())
        fullname = str(self.grid.fullname_entry.text())
        desc = str(self.grid.desc_entry.text())
        dosboxpath = str(self.grid.dosboxpath_entry.text())
        launchcmd = str(self.grid.launch_entry.text())
        _site_entries = self.grid.weblink_site_entries
        _url_entries = self.grid.weblink_url_entries
        weblink_entries = zip(_site_entries, _url_entries)
        weblinks = {}
        for site, url in weblink_entries:
            weblinks[str(site.text())] = str(url.text())
        # fill gamedata
        gamedata = dict(name=name, fullname=fullname,
                        description=desc, dosboxpath=dosboxpath,
                        launchcmd=launchcmd, weblinks=weblinks)
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
        # this dialog is currently only called from the InfoBrowser
        parent = self.parent()
        if parent.name() == 'InfoBrowser':
            # this refreshes the document in the InfoBrowser
            parent.set_game_info(gamedata['name'])
            
        
    

        
        

if __name__ == '__main__':
    print "testing gamedata_widgets module"
    
