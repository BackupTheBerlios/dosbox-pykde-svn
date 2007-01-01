import os, sys
from ConfigParser import ConfigParser

default_config = """
# configuration file for dosbox-pykde
# all options starting with "__" are not used in the code,
# but are here to ease editing this file

[DEFAULT]
__main_path:                /mirrors/share
__archive_parent_path:      %(__main_path)s/archives
installed_archives_path:	%(__archive_parent_path)s/dosbox-installed
extras_archives_path:	%(__archive_parent_path)s/dosbox-extras
tmp_parent_path:		/tmp/dosbox-area
main_dosbox_path:	         %(__main_path)s/dosbox
overwrite_extras_archives:	False
"""

main_config_dir = os.path.expanduser('~/.dosbox-pykde')
configfilename = os.path.join(main_config_dir, 'dosbox-pykde.conf')
if not os.path.exists(configfilename):
    configfile = file(configfilename, 'w')
    configfile.write(default_config)
    configfile.close()
    


# setup ConfigParser
config = ConfigParser()
configfiles = [configfilename, './local-dosbox-pykde.conf']
config.read(configfiles)

if __name__ == '__main__':
    print 'testing config module'
    
