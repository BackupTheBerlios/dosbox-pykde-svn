import os
from qt import SIGNAL, SLOT
from qt import QWidget

from kdecore import KConfig
from kdecore import KSimpleConfig

class MyKConfigBase(KConfig):
    def __init__(self, filename='', ReadOnly=False, UseKDEGlobals=True,
                 resType="config"):
        KConfig.__init__(self, 'dosbox-pykderc', ReadOnly, UseKDEGlobals, resType)
        
class MyKConfig(KSimpleConfig):
    def __init__(self, filename='dosbox-pykderc', ReadOnly=False):
        KSimpleConfig.__init__(self, filename, ReadOnly)
        sections = self.sections()
        if 'main' not in sections:
            self.setGroup('main')
            if not self.hasKey('installed_archives_path'):
                self.writeEntry('installed_archives_path', '$HOME/archives/dosbox-installed')
            if not self.hasKey('extras_archives_path'):
                self.writeEntry('extras_archives_path', '$HOME/archives/dosbox-extras')
            if not self.hasKey('main_dosbox_path'):
                self.writeEntry('main_dosbox_path', '$HOME/dosbox')
            if not self.hasKey('dosbox_binary'):
                self.writeEntry('dosbox_binary', 'dosbox')
            if not self.hasKey('tmp_parent_path'):
                self.writeEntry('tmp_parent_path', '/tmp/dosbox-area')
            if not self.hasKey('launch_weblink'):
                self.writeEntry('launch_weblink', 'kfmclient newTab "%s"')
            if not self.hasKey('text_editor'):
                self.writeEntry('text_editor', 'kate')
            if not self.hasKey('cdrive_is_main_dosbox_path'):
                self.writeEntry('cdrive_is_main_dosbox_path', False)
            self.sync()
        if 'filemanagement' not in sections:
            self.setGroup('filemanagement')
            if not self.hasKey('overwrite_extras_archives'):
                self.writeEntry('overwrite_extras_archives', True)
            if not self.hasKey('use_rdiff_backup'):
                self.writeEntry('use_rdiff_backup', True)
            if not self.hasKey('use_rsync'):
                self.writeEntry('use_rsync', True)
            self.sync()
        if 'mainwindow' not in sections:
            self.setGroup('mainwindow')
            if not self.hasKey('mainwindow_size'):
                self.writeEntry('mainwindow_size', '400, 600')
            if not self.hasKey('flat_tree_view'):
                self.writeEntry('flat_tree_view', 'flat')
            if not self.hasKey('name_title_view'):
                self.writeEntry('name_title_view', 'title')
            self.sync()
              
        for section in self.sections():
            print section, self.options(section)
        #print self.get('mainwindow', 'flat_tree_view')
        #print self.get('filemanagement', 'use_rsync')
        #print self.get('dosbox', 'main_dosbox_path')
  
    def sections(self):
        return [str(section) for section in self.groupList()]

    def options(self, section):
        emap = self.entryMap(section)
        return [str(key) for key in dict(emap).keys()]

    def get(self, section, option):
        curr_group = self.group()
        self.setGroup(section)
        value = self.readEntry(option)
        self.setGroup(curr_group)
        return value
    
    def set(self, section, option, value):
        curr_group = self.group()
        self.setGroup(section)
        self.writeEntry(option, value)
        self.setGroup(curr_group)


class SettingsWidget(QWidget):
    def __init__(self, parent, name='SettingsWidget'):
        QWidget.__init__(self, parent, name)
        
    
if __name__ == '__main__':
    print "testing module"
    
