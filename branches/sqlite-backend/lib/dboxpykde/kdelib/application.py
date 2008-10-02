import os
from StringIO import StringIO

from qt import SIGNAL, SLOT

from kdecore import KAboutData
from kdecore import KApplication
from kdecore import KStandardDirs

from kdeui import KAboutDialog

from dcopexport import DCOPExObj

from dboxpykde import VERSION
from dboxpykde import get_version
from dboxpykde.base import makepaths
from dboxpykde.path import path
from dboxpykde.config import generate_default_config
from dboxpykde.config import generate_default_dosbox_config
from dboxpykde.config import MyConfig
from dboxpykde.gamesdata import GameDataHandlerCompat
from dboxpykde.dblite.main import Connection, GameDataBaseCompat
from dboxpykde.filemanagement.main import GameFilesHandler
from dboxpykde.dosbox import Dosbox


# this is the handler that can be used through dcop
# we will attach this to the app object
# we won't add methods here, because they may not
# be reachable yet.
# we will use the .app objects in the widgets
# then call self.app.dcop.addMethod('Qstring foo(QSomething)', self.say_something)
# in that object.
class DosboxHandler(DCOPExObj):
    def __init__(self, id='dosbox-handler'):
        DCOPExObj.__init__(self, id)
        

# about this program
class AboutData(KAboutData):
    def __init__(self):
        version = get_version()
        KAboutData.__init__(self,
                            'dosbox-pykde',
                            'dosbox-pykde',
                            version,
                            "Another dosbox frontend")
        self.addAuthor('Joseph Rawson', 'author',
                       'umeboshi@gregscomputerservice.com')
        self.setCopyrightStatement('public domain')

class AboutDialog(KAboutDialog):
    def __init__(self):
        KAboutDialog.__init__(self, parent, *args)
        self.setTitle('PyKDE Dosbox Frontend')
        self.setAuthor('Joseph Rawson')
        
# main application class
class MainApplication(KApplication):
    def __init__(self):
        KApplication.__init__(self)
        # in case something needs done before quitting
        self.connect(self, SIGNAL('aboutToQuit()'), self.quit)
        # place dcop object here
        self.dcop = DosboxHandler()
        self._setup_standard_directories()
        self._generate_data_directories()
        self.mainconfigfilename = os.path.join(self.datadir, 'dosbox-pykde.conf')
        if os.path.isfile(self.mainconfigfilename):
            self.generate_default_config()
            self.generate_main_objects()
            

    def setMainWidget(self, win):
        self.mainwindow = win
        KApplication.setMainWidget(self, win)
        
    def generate_default_config(self):
        default_dbox_cfilename = os.path.join(self.datadir, 'dosbox.conf.default')
        # generate default config files if not already present
        # this would be a good time to use a wizard to setup config options
        generate_default_config(self.mainconfigfilename)
        generate_default_dosbox_config(default_dbox_cfilename)
        self.load_main_config()

    def generate_main_objects(self):
        # setup objects
        self.upgrade_to_db_required = False
        self._dbfile = self.datadir / 'main.db'
        if not self._dbfile.exists():
            print "no database file exists."
            # test for xml files
            gdh = GameDataHandlerCompat(self)
            games = gdh.get_game_names()
            if games:
                self.upgrade_to_db_required = True
        self.conn = Connection(self._dbfile)
        #self.game_datahandler = self.make_new_datahandler()
        self.game_datahandler = GameDataBaseCompat(self.conn)
        self.game_datahandler.set_screenshots_path(self.data_directories['screenshots'])
        self.game_fileshandler = self.make_new_fileshandler()
        self.dosbox = self.make_new_dosbox_object()

    def convert_all_xml_to_db(self):
        gdh = GameDataHandlerCompat(self)
        games = gdh.get_game_names()
        for game in games:
            print 'converting', game
            gamedata = gdh.get_game_data(game)
            installed = gdh.get_installed_files(game)
            self.game_datahandler.add_new_game(gamedata, installed)
            
    # we call self._generate_data_directories() in this method
    # because changes to the config may affect these options
    # and the corresponding application attributes
    def load_main_config(self):
        self.myconfig = MyConfig()
        self.myconfig.read([self.mainconfigfilename])
        self._generate_archive_directories()
        
    def update_main_config(self, configobj):
        cfile = StringIO()
        configobj.write(cfile)
        cfile.seek(0)
        self.myconfig.readfp(cfile)
        self.save_main_config(self.mainconfigfilename)
        self.load_main_config()

    def save_main_config(self, filename=None):
        if filename is None:
            filename = self.mainconfigfilename
        cfile = file(filename, 'w')
        self.myconfig.write(cfile)
        cfile.close()
        
    def make_new_datahandler(self):
        return GameDataHandler(self)

    def make_new_fileshandler(self):
        return GameFilesHandler(self)

    def make_new_dosbox_object(self):
        return Dosbox(self)

    
    # this method sets up the directories used by the application
    # with respect to the KDE environment
    # currently the main config file is placed in self.datadir
    # changes in the file dialogs used in the application will
    # be stored in the config file in its proper location
    # when I am ready to deal with changes to that config file
    # that my code doesn't use, I will probably move the main
    # config file to the regular config location
    def _setup_standard_directories(self):
        self._std_dirs = KStandardDirs()
        self.tmpdir_parent = path(str(self._std_dirs.findResourceDir('tmp', '/')))
        self.datadir_parent = path(str(self._std_dirs.findResourceDir('data', '/')))
        self.tmpdir = self.tmpdir_parent / 'dosbox-pykde'
        self.datadir = self.datadir_parent / 'dosbox-pykde'
        # we need this in dosbox object (for now)
        self.main_config_dir = self.datadir
        if not self.datadir.exists():
            self.datadir.mkdir()
        
    def _generate_data_directories(self):
        directories = {}.fromkeys(['games', 'configs', 'screenshots', 'capture', 'profiles',
                                   'cache'])
        for dir_key in directories:
            newdir = self.datadir / dir_key
            directories[dir_key]  = newdir
            if not newdir.exists():
                try:
                    newdir.mkdir()
                except OSError, inst:
                    #print inst, dir(inst), inst.errno
                    if inst.errno != 17:
                        raise OSError(inst)
        self.data_directories = directories

    # this method sets attributes for the main directories
    # used in the application.
    # it also creates the directories if they aren't already there
    # except for the main_dosbox_path
    # I should probably use a yes/no dialog before actually creating the
    # directories.
    def _generate_archive_directories(self):
        cfg = self.myconfig
        installed_archives_path = cfg.getpath('filemanagement', 'installed_archives_path')
        extras_archives_path = cfg.getpath('filemanagement', 'extras_archives_path')
        makepaths(installed_archives_path, extras_archives_path)
        self.installed_archives_path = installed_archives_path
        self.extras_archives_path = extras_archives_path
        self.main_dosbox_path = cfg.getpath('dosbox', 'main_dosbox_path')

    # This method is currently useless, but may be useful later
    # if some house cleaning needs doing before quitting
    def quit(self):
        # house cleaning chores go here
        KApplication.quit(self)


if __name__ == '__main__':
    print "testing module"
    
