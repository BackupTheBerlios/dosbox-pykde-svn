import os, sys
from ConfigParser import ConfigParser

from base import ExistsError

default_config = """
# configuration file for dosbox-pykde
# all options starting with "__" are not used in the code,
# but are here to ease editing this file

[DEFAULT]
__main_path:                %s """ % os.path.expanduser('~/')[:-1]
default_config +="""

# These are the commands used for file management.
[filemanagement]
# Currently rdiff-backup and rsync are required.
use_rdiff_backup:  True
# if use_rdiff_backup is True, we restore to a staging
# area and rsync it into the install path.  This is only needed
# when rdiff-backup is used.
use_rsync:  True

__archive_parent_path:      %(__main_path)s/archives
# path to the archives of freshly installed games
installed_archives_path:	%(__archive_parent_path)s/dosbox-installed
# path to the extras archives (backups of savegames and configs)
extras_archives_path:	%(__archive_parent_path)s/dosbox-extras

# This option determines whether the extra files
# are archived in tarballs, or just left as a
# rdiff-backup tree.
extras_archives_tarballs:  True

# option to keep from overwriting extras archives
# this should normally be set to true, as by default
# all extras archives are rdiff-backup trees
# this option is here in case we don't ever use
# rdiff-backup.  Set this to False to keep all
# backups of the extras archives
overwrite_extras_archives:	True

[dosbox]
# the parent path to the installed dosbox games
main_dosbox_path:	         %(__main_path)s/dosbox
# the path to the dosbox binary
# if already in the path, the default should be fine
dosbox_binary:              dosbox

# whether the main_dosbox_path is mounted as c:
# or the full path to the game is mounted ad c:
# If this is set to True, all intermediate directory
# names need to be <= 8 chars.
cdrive_is_main_dosbox_path:    False

[externalactions]
# command to launch external weblinks
# The default command talks to a running konqueror process
# and exits quickly, leaving konqueror to do the work
# this command is executed with an os.system call, so any
# command here needs to tell a running webbrowser to open a link
# then exit, or this application will freeze waiting for the command
# to finish executing.
launch_weblink:   kfmclient newTab "%s"
#text editor command
text_editor:      kate

[mainwindow]
mainwindow_size:  400, 600
# default view types
flat_tree_view:   flat
name_title_view:  title
use_khtml_part:   False

[gamedata_dialog]
dialog_size:   400, 300

[dosbox_profiles]
default_resolutions:    640x480,800x600,1024x768,1280x768

""" 

default_dbox_config = """
[ipx]
ipx = false

[render]
scaler = normal2x
aspect = false
frameskip = 0

[midi]
device = default
mpu401 = intelligent
config = 

[sblaster]
dma = 1
mixer = true
oplrate = 22050
irq = 7
hdma = 5
sbbase = 220
sbtype = sb16
oplmode = auto

[mixer]
rate = 22050
prebuffer = 10
nosound = false
blocksize = 2048

[gus]
dma2 = 3
gusbase = 240
irq2 = 5
ultradir = C:\ULTRASND
irq1 = 5
gus = true
dma1 = 3
gusrate = 22050

[bios]
joysticktype = 2axis

[speaker]
pcspeaker = true
tandy = auto
tandyrate = 22050
disney = true
pcrate = 22050

[sdl]
usescancodes = true
fullscreen = false
fulldouble = false
mapperfile = mapper.txt
sensitivity = 100
priority = higher,normal
windowresolution = original
waitonerror = true
output = surface
autolock = true
fullresolution = original

[dos]
umb = true
ems = true
xms = true

[serial]
serial3 = disabled
serial1 = dummy
serial4 = disabled
serial2 = dummy

[cpu]
cycles = 3000
cycledown = 20
cycleup = 500
core = normal

[dosbox]
machine = vga
memsize = 16
language = 
captures = capture

"""


class MyConfig(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
        
    def get_xy(self, section, option):
        strvalue = self.get(section, option)
        x, y = [int(v.strip()) for v in strvalue.split(',')]
        return x, y

    def get_list(self, section, option, sep=','):
        value = self.get(section, option)
        return [v.strip() for v in value.split(sep)]
    
    def reload_config(self):
        self.read([self.configfilename])
        
def generate_default_config(path):
    if not os.path.exists(path):
        cfile = file(path, 'w')
        cfile.write(default_config)
        cfile.close()

def generate_default_dosbox_config(path):
    if not os.path.exists(path):
        cfile = file(path, 'w')
        cfile.write(default_dbox_config)
        cfile.close()

if __name__ == '__main__':
    print 'testing config module'
    
