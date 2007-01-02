import os, sys
from ConfigParser import ConfigParser

default_config = """
# configuration file for dosbox-pykde
# all options starting with "__" are not used in the code,
# but are here to ease editing this file

[DEFAULT]
__main_path:                %s """ % os.path.expanduser('~/')[:-1]
default_config +="""
__archive_parent_path:      %(__main_path)s/archives
# path to the archives of freshly installed games
installed_archives_path:	%(__archive_parent_path)s/dosbox-installed
# path to the extras archives (backups of savegames and configs)
extras_archives_path:	%(__archive_parent_path)s/dosbox-extras
# the parent path for temporary manipulation
# of extras archives contents
tmp_parent_path:		/tmp/dosbox-area
# the parent path to the installed dosbox games
main_dosbox_path:	         %(__main_path)s/dosbox
# option to keep from overwriting extras archives
# this should normally be set to true, as by default
# all extras archives are rdiff-backup trees
# this option is here in case we don't ever use
# rdiff-backup.  Set this to False to keep all
# backups of the extras archives
overwrite_extras_archives:	True
# the path to the dosbox binary
# if already in the path, the default should be fine
dosbox_binary:              dosbox
# command to launch external weblinks
launch_weblink:   kfmclient newTab %s
#text editor command
text_editor:      kate

[mainwindow]
mainwindow_size:  400, 600
# default view types
flat_tree_view:   flat
name_title_view:  title

[gamedata_dialog]
dialog_size:   400, 300
""" 

main_config_dir = os.path.expanduser('~/.dosbox-pykde')
configfilename = os.path.join(main_config_dir, 'dosbox-pykde.conf')
if not os.path.exists(configfilename):
    configfile = file(configfilename, 'w')
    configfile.write(default_config)
    configfile.close()
    

class MyConfig(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
        self.configfilename = configfilename
        
    def get_xy(self, section, option):
        strvalue = self.get(section, option)
        x, y = [int(v.strip()) for v in strvalue.split(',')]
        return x, y

    def reload_config(self):
        self.read([self.configfilename])
        
# setup ConfigParser
config = MyConfig()
configfiles = [configfilename, './local-dosbox-pykde.conf']
config.read(configfiles)

if __name__ == '__main__':
    print 'testing config module'
    
