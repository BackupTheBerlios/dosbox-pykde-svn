from qt import QCheckBox
from qt import QGridLayout

from dboxpykde.kdelib.base import BaseDialogWindow

from dboxpykde.kdelib.config import BaseConfigWidget
from dboxpykde.kdelib.config import VerticalGroupBox
from dboxpykde.kdelib.config import ConfigKURLSelectWidget
from dboxpykde.kdelib.config import ConfigLineEditWidget
from dboxpykde.kdelib.config import ConfigComboBoxWidget
from dboxpykde.kdelib.config import ConfigWinSizeWidget

class SettingsWidget(BaseConfigWidget):
    def __init__(self, parent, name='SettingsWidget'):
        BaseConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 2
        margin = 7
        space = 10
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'SettingsWidgetLayout')
        self.myconfig = self.app.myconfig
        for section in ['filemanagement', 'dosbox', 'externalactions', 'mainwindow']:
            self.localconfig.add_section(section)
            
        # filemanagement area
        self.filemanagement_groupbox = VerticalGroupBox(self, 'File Management')
        self.filemanagement_groupbox.setColumns(4)
        #self.grid.addWidget(self.filemanagement_groupbox, 0, 0)
        self.grid.addMultiCellWidget(self.filemanagement_groupbox, 0, 0, 0, 1)
        self.use_rdiff_backup_check = QCheckBox(self.filemanagement_groupbox)
        self.use_rdiff_backup_check.setText('Use rdiff-backup')
        self.use_rsync_check = QCheckBox(self.filemanagement_groupbox)
        self.use_rsync_check.setText('Use rsync')
        self.overwrite_extras_archives_check = QCheckBox(self.filemanagement_groupbox)
        self.overwrite_extras_archives_check.setText('Overwrite extras archives')
        self.archives_groupbox = VerticalGroupBox(self.filemanagement_groupbox,
                                                  'Archive Paths')
        self.archives_groupbox.setColumns(2)
        #self.grid.addWidget(self.archives_groupbox, 0, 1)
        self.installed_archives_entry = ConfigKURLSelectWidget(self.archives_groupbox,
                                                               'Path to the "install" archives',
                                                               filetype='dir')
        self.extras_archives_entry = ConfigKURLSelectWidget(self.archives_groupbox,
                                                            'Path to the "extras" archives',
                                                            filetype='dir')
        # dosbox area
        self.dosbox_groupbox = VerticalGroupBox(self, 'Dosbox Options')
        self.dosbox_groupbox.setColumns(3)
        #self.grid.addWidget(self.dosbox_groupbox, 1, 0)
        self.grid.addMultiCellWidget(self.dosbox_groupbox, 1, 1, 0, 1)
        self.main_dosbox_path_entry = ConfigKURLSelectWidget(self.dosbox_groupbox,
                                                             'Path to dosbox area',
                                                             filetype='dir')
        self.dosbox_binary_entry = ConfigLineEditWidget(self.dosbox_groupbox,
                                                        'Dosbox executable')
        self.cdrive_is_main_check = QCheckBox(self.dosbox_groupbox)
        self.cdrive_is_main_check.setText('C: Drive is main dosbox path')
        # externalactions area
        self.externalactions_groupbox = VerticalGroupBox(self, 'External Actions')
        self.externalactions_groupbox.setColumns(2)
        self.grid.addWidget(self.externalactions_groupbox, 2, 0)
        self.launch_weblinks_entry = ConfigLineEditWidget(self.externalactions_groupbox,
                                                          'Command to handle weblink clicks')
        self.text_editor_entry = ConfigLineEditWidget(self.externalactions_groupbox,
                                                      'Text editor command')
        # mainwindow area
        self.mainwindow_groupbox = VerticalGroupBox(self, 'Main Window Options')
        self.mainwindow_groupbox.setColumns(3)
        self.grid.addWidget(self.mainwindow_groupbox, 2, 1)
        self.mainwindow_size_box = ConfigWinSizeWidget(self.mainwindow_groupbox,
                                                       'Size of main window')
        self.flat_tree_box = ConfigComboBoxWidget(self.mainwindow_groupbox,
                                                  'Game list style', ['flat', 'tree'])
        self.name_title_box = ConfigComboBoxWidget(self.mainwindow_groupbox,
                                                   'Game list entries', ['name', 'title'])

    def set_config(self, configobj):
        self.mainconfig = configobj
        # some assignments to help with typing
        filemanagement = 'filemanagement'
        dosbox = 'dosbox'
        externalactions = 'externalactions'
        mainwindow = 'mainwindow'
        cfg = self.mainconfig
        # set the various config widgets
        # filemanagement section
        use_rdiff_backup = cfg.getboolean(filemanagement, 'use_rdiff_backup')
        self.use_rdiff_backup_check.setChecked(use_rdiff_backup)
        use_rsync = cfg.getboolean(filemanagement, 'use_rsync')
        self.use_rsync_check.setChecked(use_rsync)
        overwrite_extras_archives = cfg.getboolean(filemanagement, 'overwrite_extras_archives')
        self.overwrite_extras_archives_check.setChecked(overwrite_extras_archives)
        installed_archives_path = cfg.get(filemanagement, 'installed_archives_path')
        self.installed_archives_entry.set_config_option(installed_archives_path)
        extras_archives_path = cfg.get(filemanagement, 'extras_archives_path')
        self.extras_archives_entry.set_config_option(extras_archives_path)
        # dosbox section
        dosbox_binary = cfg.get(dosbox, 'dosbox_binary')
        self.dosbox_binary_entry.set_config_option(dosbox_binary)
        main_dosbox_path = cfg.get(dosbox, 'main_dosbox_path')
        self.main_dosbox_path_entry.set_config_option(main_dosbox_path)
        cdrive_is_main = cfg.getboolean(dosbox, 'cdrive_is_main_dosbox_path')
        self.cdrive_is_main_check.setChecked(cdrive_is_main)
        # externalactions section
        launch_weblink = cfg.get(externalactions, 'launch_weblink')
        self.launch_weblinks_entry.set_config_option(launch_weblink)
        text_editor = cfg.get(externalactions, 'text_editor')
        self.text_editor_entry.set_config_option(text_editor)
        # mainwindow section
        mainwindow_size = cfg.get(mainwindow, 'mainwindow_size')
        self.mainwindow_size_box.set_config_option(mainwindow_size)
        flat_tree_view = cfg.get(mainwindow, 'flat_tree_view')
        self.flat_tree_box.set_config_option(flat_tree_view)
        name_title_view = cfg.get(mainwindow, 'name_title_view')
        self.name_title_box.set_config_option(name_title_view)

    def get_config(self):
        # some assignments to help with typing
        filemanagement = 'filemanagement'
        dosbox = 'dosbox'
        externalactions = 'externalactions'
        mainwindow = 'mainwindow'
        cfg = self.localconfig
        # get config values from the various widgets
        # filemanagement section
        use_rdiff_backup = self._get_bool_for_config(self.use_rdiff_backup_check)
        cfg.set(filemanagement, 'use_rdiff_backup', use_rdiff_backup)
        use_rsync = self._get_bool_for_config(self.use_rsync_check)
        cfg.set(filemanagement, 'use_rsync', use_rsync)
        overwrite_extras = self._get_bool_for_config(self.overwrite_extras_archives_check)
        cfg.set(filemanagement, 'overwrite_extras_archives', overwrite_extras)
        installed_archives_path = self.installed_archives_entry.get_config_option()
        cfg.set(filemanagement, 'installed_archives_path', installed_archives_path)
        extras_archives_path = self.extras_archives_entry.get_config_option()
        cfg.set(filemanagement, 'extras_archives_path', extras_archives_path)
        # dosbox section
        dosbox_binary = self.dosbox_binary_entry.get_config_option()
        cfg.set(dosbox, 'dosbox_binary', dosbox_binary)
        main_dosbox_path = self.main_dosbox_path_entry.get_config_option()
        cfg.set(dosbox, 'main_dosbox_path', main_dosbox_path)
        cdrive_is_main = self._get_bool_for_config(self.cdrive_is_main_check)
        cfg.set(dosbox, 'cdrive_is_main_dosbox_path', cdrive_is_main)
        # externalactions section
        launch_weblink = self.launch_weblinks_entry.get_config_option()
        cfg.set(externalactions, 'launch_weblink', launch_weblink)
        text_editor = self.text_editor_entry.get_config_option()
        cfg.set(externalactions, 'text_editor', text_editor)
        # mainwindow section
        mainwindow_size = self.mainwindow_size_box.get_config_option()
        cfg.set(mainwindow, 'mainwindow_size_', mainwindow_size)
        flat_tree_view = self.flat_tree_box.get_config_option()
        cfg.set(mainwindow, 'flat_tree_view', flat_tree_view)
        name_title_view = self.name_title_box.get_config_option()
        cfg.set(mainwindow, 'name_title_view', name_title_view)
        return cfg
    
########################
# testing stuff here
# class for testing config widgets
from qt import SIGNAL
from qt import QWidget
from kdeui import KTabWidget
from kdeui import KTextBrowser
from kdeui import KPushButton
from StringIO import StringIO
class TestConfigTab(QWidget):
    def __init__(self, parent, name='TestConfigTab'):
        QWidget.__init__(self, parent, name)
        self.grid = QGridLayout(self, 2, 1, 0, 1, 'TestConfigTabLayout')
        self.textbrowser = KTextBrowser(self)
        self.grid.addWidget(self.textbrowser, 0, 0)
        self.button = KPushButton(self)
        self.button.setText('test get_config')
        self.grid.addWidget(self.button, 1, 0)
        
    def set_config(self, cfg):
        tfile = StringIO()
        cfg.write(tfile)
        tfile.seek(0)
        text = tfile.read()
        self.textbrowser.setText(text)
        
        
class SettingsTabWidget(KTabWidget):
    def __init__(self, parent, name='SettingsTabWidget'):
        KTabWidget.__init__(self, parent, name)
        self.settingstab = SettingsWidget(self)
        self.insertTab(self.settingstab, 'settings')
        # testing stuff
        self.testtab = TestConfigTab(self)
        self.insertTab(self.testtab, 'test me')
        self.connect(self.testtab.button, SIGNAL('clicked()'), self.get_config)
        
    def get_config(self):
        cfg = self.settingstab.get_config()
        self.testtab.set_config(cfg)

    def set_config(self, configobj):
        self.settingstab.set_config(configobj)
        
# end of testing stuff
#######################
        

class SettingsWidgetDialog(BaseDialogWindow):
    def __init__(self, parent, name='SettingsWidgetDialog'):
        BaseDialogWindow.__init__(self, parent, name=name)
        #self.frame = SettingsWidget(self)
        self.frame = SettingsTabWidget(self)
        self.setMainWidget(self.frame)
        self.frame.set_config(self.app.myconfig)

    def update_config(self):
        newcfg = self.frame.get_config()

