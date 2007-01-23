import os
from qt import SIGNAL, SLOT
from qt import PYSIGNAL
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

from dboxpykde.kdelib.base import BaseDialogWindow

opendlg_errormsg = 'There is already a dialog box open.  Close it or restart the program'

class BaseGameDataFrame(QFrame):
    def __init__(self, parent, name='BaseGameDataFrame'):
        QFrame.__init__(self, parent, name)
        # there will be more than two rows, but we'll start with two
        numrows = 2
        # there should onlty be two columns
        numcols = 2
        margin = 0
        space = 1
        # add a grid layout to the frame
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'BaseGameDataLayout')
        # make a couple of lists to point to the weblink entries
        # order is important in these lists
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
        self.name_lbl = QLabel('<b>Name</b>', self)
        self.name_entry = KLineEdit('', self)
        # add name widgets to grid
        self.grid.addWidget(self.name_lbl, 0, 0)
        self.grid.addWidget(self.name_entry, 1, 0)
        # setup fullname widgets
        self.fullname_lbl = QLabel('<b>Full name</b>', self)
        self.fullname_entry = KLineEdit('', self)
        # add fullname widgets
        self.grid.addWidget(self.fullname_lbl, 2, 0)
        self.grid.addWidget(self.fullname_entry, 3, 0)
        # setup description widgets
        self.desc_lbl = QLabel('<b>Description</b>', self)
        self.desc_entry = KTextEdit(self, 'description_entry')
        # set plain text format for description entry
        # we do this in case there are html tags in the entry
        self.desc_entry.setTextFormat(self.PlainText)
        # add description widgets
        self.grid.addWidget(self.desc_lbl, 4, 0)
        #self.addWidget(self.desc_entry, 5, 0)
        # add the description as a multirow entity
        # default from 5 to 15
        # this allows for weblinks to be added
        # (about 5)
        # without the dialog looking ugly
        # going to 15 won't force there to be that many rows
        # until more enough widgets are added
        self.grid.addMultiCellWidget(self.desc_entry, 5, 15, 0, 0)
        # setup launch command widgets
        self.launch_lbl = QLabel('<b>Launch command</b>', self)
        self.launch_entry = KLineEdit('', self)
        self.launch_dlg_button = KPushButton('...', self, 'launch_dlg_button')
        self.launch_dlg_button.connect(self.launch_dlg_button, SIGNAL('clicked()'),
                                       self.select_launch_command)
        # add launch command widgets
        self.grid.addWidget(self.launch_lbl, 0, 1)
        self.grid.addWidget(self.launch_entry, 1, 1)
        self.grid.addWidget(self.launch_dlg_button, 1, 2)
        # setup dosboxpath widgets
        self.dosboxpath_lbl = QLabel('<b>dosbox path</b>', self)
        self.dosboxpath_entry = KLineEdit('', self)
        # add dosboxpath widgets
        self.grid.addWidget(self.dosboxpath_lbl, 2, 1)
        self.grid.addWidget(self.dosboxpath_entry, 3, 1)
        # setup main weblink widgets
        self.weblinks_lbl = QLabel('<b>weblinks</b>', self)
        self.weblinks_btn = KPushButton('+', self, 'add_weblink_button')
        self.weblinks_btn.connect(self.weblinks_btn, SIGNAL('clicked()'),
                                  self.add_weblink_entries)
        # add main weblink widgets
        self.grid.addWidget(self.weblinks_lbl, 4, 1)
        self.grid.addWidget(self.weblinks_btn, 4, 2)
        
    def select_launch_command(self):
        if self.select_launch_command_dlg is None:
            file_filter = "*.exe *.bat *.com|Dos Executables\n*|All Files"
            dlg = KFileDialog(self.fullpath, file_filter,  self, 'select_launch_command_dlg', True)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.launch_command_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_select_launch_command_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_select_launch_command_dlg)
            dlg.show()
            self.select_launch_command_dlg = dlg
        else:
            # we shouldn't need this with a modal dialog
            KMessageBox.error(self, opendlg_errormsg)

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
        num_entries = len(self.weblink_url_entries)
        # we need to add 1 on lbl_num because the entries can be appended
        # until instantiated
        lbl_num = num_entries + 1
        site_lbl = QLabel('<b>site %d</b>' % lbl_num, self)
        site_entry = KLineEdit(site, self)
        self.weblink_site_entries.append(site_entry)
        url_lbl = QLabel('<b>url %d</b>' % lbl_num, self)
        url_entry = KLineEdit(url, self)
        self.weblink_url_entries.append(url_entry)
        if len(self.weblink_site_entries) != len(self.weblink_url_entries):
            KMessageBox.error(self, 'entries mismatch, something really bad happened.')
            import sys
            sys.exit(1)
        # we need a little math here to figure out the rows
        # for the widgets
        # num_entries should now be 1 greater than above
        num_entries = len(self.weblink_url_entries)
        site_row = 2*num_entries + 3
        url_row = 2*num_entries + 4
        # add weblink widgets to the grid
        top = self.grid.AlignTop
        self.grid.addWidget(site_entry, site_row, 1)
        self.grid.addWidget(site_lbl, site_row, 2)
        self.grid.addWidget(url_entry, url_row, 1)
        self.grid.addWidget(url_lbl, url_row, 2)
        # we have to call .show() explicitly on the widgets
        # as the rest of the widgets are already visible
        # when show was called on the dialog
        # show() automatically calls show() on all children
        for widget in [site_lbl, site_entry, url_lbl, url_entry]:
            widget.show()
        

        

class BaseGameDataDialog(BaseDialogWindow):
    def __init__(self, parent, name='BaseGameDataDialog'):
        BaseDialogWindow.__init__(self, parent, name=name)
        # we need a frame for the layout widget
        # the layout widget won't work with a window as parent
        self.frame = BaseGameDataFrame(self)
        # set frame as main widget
        self.setMainWidget(self.frame)
        self.resize(*self.config.get_xy('gamedata_dialog', 'dialog_size'))


    def _fill_layout(self, gamedata):
        self.frame.name_entry.setText(gamedata['name'])
        self.frame.fullname_entry.setText(gamedata['fullname'])
        self.frame.desc_entry.setText(gamedata['description'])
        self.frame.launch_entry.setText(gamedata['launchcmd'])
        self.frame.dosboxpath_entry.setText(gamedata['dosboxpath'])
        # remember the weblinks
        sites = gamedata['weblinks'].keys()
        sites.sort()
        for site in sites:
            self.frame.add_weblink_entries(site, gamedata['weblinks'][site])
            
    def get_gamedata_from_entries(self):
        # setup keys for gamedata
        name = str(self.frame.name_entry.text())
        fullname = str(self.frame.fullname_entry.text())
        desc = str(self.frame.desc_entry.text())
        dosboxpath = str(self.frame.dosboxpath_entry.text())
        launchcmd = str(self.frame.launch_entry.text())
        _site_entries = self.frame.weblink_site_entries
        _url_entries = self.frame.weblink_url_entries
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
        self.frame.fullpath = fullpath
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
                        dosboxpath=dosboxpath, weblinks={})
        self._fill_layout(gamedata)
        
            
class EditGameDataDialog(BaseGameDataDialog):
    def __init__(self, parent, game, name='EditGameDataDialog'):
        BaseGameDataDialog.__init__(self, parent, name)
        self.handler = self.app.game_datahandler
        gamedata = self.handler.get_game_data(game)
        self.frame.fullpath = os.path.join(self.app.main_dosbox_path, gamedata['dosboxpath'])
        self._fill_layout(gamedata)
        self.connect(self, SIGNAL('okClicked()'), self.update_gamedata)
        self.connect(self, SIGNAL('applyClicked()'), self.update_gamedata)
        
    def update_gamedata(self):
        gamedata = self.get_gamedata_from_entries()
        self.handler.update_game_data(gamedata)
        KMessageBox.information(self, 'Data updated for %s' % gamedata['fullname'])
        # we emit a GameDataUpdated signal passing the name of the game
        # as a parameter so the infobrowser will update the display
        self.emit(PYSIGNAL('GameDataUpdated'), (gamedata['name'], ))
                    
        #self.app.processEvents()
        
    

        
        

if __name__ == '__main__':
    print "testing gamedata_widgets module"
    
