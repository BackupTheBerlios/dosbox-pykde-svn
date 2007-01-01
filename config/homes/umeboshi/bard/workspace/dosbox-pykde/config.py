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
installed_archives_path:	%(__archive_parent_path)s/dosbox-installed
extras_archives_path:	%(__archive_parent_path)s/dosbox-extras
tmp_parent_path:		/tmp/dosbox-area
main_dosbox_path:	         %(__main_path)s/dosbox
overwrite_extras_archives:	False
# the path to the dosbox binary
# if already in the path, the default should be fine
dosbox_binary:              dosbox

[mainwindow]
mainwindow_size:  400, 600
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
    
