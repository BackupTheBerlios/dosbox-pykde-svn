from ConfigParser import ConfigParser

from qt import QWidget

from qt import QToolTip

from qt import QGridLayout
from qt import QGroupBox
from qt import QLabel


from kdeui import KComboBox
from kdeui import KIntSpinBox
from kdeui import KLineEdit

# imports for the main settings widget
from kdeui import KTabWidget
from dboxpykde.kdelib.base import BaseDialogWindow
from qt import QCheckBox

from kfile import KFile
from kfile import KURLRequester

from dboxpykde.kdelib.base import get_application_pointer

class BaseConfigWidget(QWidget):
    def __init__(self, parent, name='BaseConfigWidget'):
        QWidget.__init__(self, parent, name)
        self.app = get_application_pointer()
        self.tooltips = QToolTip
        self.mainconfig = None
        self.localconfig = ConfigParser()
        
    def set_config(self, configobj):
        raise NotImplementedError, 'set_config needs to be defined in subclass'

    def get_config(self):
        raise NotImplementedError, 'get_config needs to be defined in subclass'

    # helper method for checkboxes
    def _get_bool_for_config(self, checkbox):
        value = checkbox.isChecked()
        return str(value).lower()
    

            
class BaseConfigOptionWidget(BaseConfigWidget):
    def __init__(self, parent, labeltext, optclass,
                 name='BaseConfigOptionWidget'):
        BaseConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 2
        margin = 0
        space = 1
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'BaseConfigOptionWidgetLayout')
        self.label = QLabel(labeltext, self)
        self.grid.addWidget(self.label, 0, 0)
        self.mainwidget = optclass(self)
        self.grid.addWidget(self.mainwidget, 1, 0)

    def get_config_option(self):
        raise NotImplementedError, 'get_config_option needs to be defined in subclass'

    def set_config_option(self, option):
        raise NotImplementedError, 'set_config_option needs to be defined in subclass'
    
class ConfigComboBoxWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, defaults,
                 name='ConfigComboBoxWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KComboBox, name=name)
        self.mainwidget.insertStrList(defaults)
        self._mainlist = defaults

    def get_config_option(self):
        opt = self.mainwidget.currentText()
        return str(opt)

    def set_config_option(self, option):
        if option not in self._mainlist:
            raise ValueError, '%s not in list of options' % option
        index = self._mainlist.index(option)
        self.mainwidget.setCurrentItem(index)
        
class ConfigLineEditWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext,
                 name='ConfigLineEditWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KLineEdit, name=name)
        
    def get_config_option(self):
        opt = self.mainwidget.text()
        return str(opt)

    def set_config_option(self, option):
        self.mainwidget.setText(option)
        

class ConfigSpinWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, min=0, max=100, suffix='',
                 name='BaseConfigOptionSpinWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KIntSpinBox, name=name)
        self.mainwidget.setMinValue(min)
        self.mainwidget.setMaxValue(max)
        if suffix:
            self.mainwidget.setSuffix(suffix)

    def get_config_option(self):
        return self.mainwidget.value()

    # option needs to be an integer here
    def set_config_option(self, option):
        self.mainwidget.setValue(option)

class ConfigKURLSelectWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, filetype='file',
                 name='ConfigKURLSelectWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext, KURLRequester,
                                        name=name)
        if filetype in ['dir', 'directory']:
            self.mainwidget.setMode(KFile.Directory)

    def get_config_option(self):
        lineEdit = self.mainwidget.lineEdit()
        return str(lineEdit.text())

    def set_config_option(self, option):
        lineEdit = self.mainwidget.lineEdit()
        lineEdit.setText(option)

# I should look for a Q or K class that already does
# something similar
class WinSizeEntryWidget(QWidget):
    def __init__(self, parent, name='WinSizeEntryWidget'):
        QWidget.__init__(self, parent, name)
        numrows = 2
        numcols = 2
        margin = 0
        space = 1
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'WinSizeEntryWidgetLayout')
        self.w_label = QLabel('width', self)
        self.grid.addWidget(self.w_label, 0, 0)
        # should be using KIntSpinBox instead of text entry
        self.w_entry = KLineEdit(self)
        self.grid.addWidget(self.w_entry, 1, 0)
        self.h_label = QLabel('height', self)
        self.grid.addWidget(self.h_label, 0, 1)
        # should be using KIntSpinBox instead of text entry
        self.h_entry = KLineEdit(self)
        self.grid.addWidget(self.h_entry, 1, 1)

# this needs to be redone to handle integers
# instead of strings
class ConfigWinSizeWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, name='ConfigWinSizeWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext, WinSizeEntryWidget,
                                        name=name)

    def get_config_option(self):
        width = str(self.mainwidget.w_entry.text())
        height = str(self.mainwidget.h_entry.text())
        return ', '.join([width, height])

    def set_config_option(self, option):
        width, height = [x.strip() for x in option.split(',')]
        self.mainwidget.w_entry.setText(width)
        self.mainwidget.h_entry.setText(height)
        
class VerticalGroupBox(QGroupBox):
    def __init__(self, parent, title):
        QGroupBox.__init__(self, parent)
        self.setTitle(title)
        self.setOrientation(self.Vertical)
        
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
from kdeui import KTextBrowser
from kdeui import KPushButton
from qt import SIGNAL
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

############
# more testing stuff

# testing stuff here
from kdecore import KConfigSkeleton
from kdecore import KConfigSkeletonItem
import qt
class TestItem(KConfigSkeletonItem):
    def __init__(self, section, option):
        KConfigSkeletonItem.__init__(self, section, option)
        
class MyConfigSkeleton(KConfigSkeleton):
    def __init__(self):
        KConfigSkeleton.__init__(self, 'configskeletontest')
        self.app = get_application_pointer()
        print self.config()
        self.readConfig()
        print dir(self)
        #self.addItemString('testOption', 'testValue', 'testValue')
        print self.currentGroup()
        self.setCurrentGroup('main')
        #print self.currentGroup()
        #self.addItemBool('testbool', True)
        #self.addItemString('testOption', 'testValue', 'testValue', 'testOption')
        self.password = ''
        self.user = ''
        self.addItemString("user",self.user,"nobody")
        self.addItemString("password",self.password,"p")

    def getPassword(self):
        return self.password
    def getUser(self):
        return self.user
    def savePref(user, password, minutes):
        self.user = user
        self.password =password
        self.minutes = minutes
        #print self.items()
        #self.addItemString('testOption2', 'testValue2', 'testValue2', 'testOption2')
        #item = TestItem('main', 'testOption')
        #self.addItem(item, 'testOption')
        #self.writeConfig()
        #self.usrWriteConfig()

#####################
        
