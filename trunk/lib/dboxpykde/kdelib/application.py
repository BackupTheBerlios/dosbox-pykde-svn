import os
from qt import SIGNAL, SLOT

from kdecore import KAboutData
from kdecore import KApplication
from kdecore import KStandardDirs

from kdeui import KAboutDialog

# testing this one
from dcopexport import DCOPExObj

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
        KAboutData.__init__(self,
                            'dosbox-pykde',
                            'dosbox-pykde',
                            '0.1',
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
        self._std_dirs = KStandardDirs()
        self.tmpdir_parent = str(self._std_dirs.findResourceDir('tmp', '/'))
        self.datadir_parent = str(self._std_dirs.findResourceDir('data', '/'))
        self.tmpdir = os.path.join(self.tmpdir_parent, 'dosbox-pykde')
        self.datadir = os.path.join(self.datadir_parent, 'dosbox-pykde')
        if not os.path.exists(self.datadir):
            os.mkdir(self.datadir)
        self._generate_data_directories()
        
    def _generate_data_directories(self):
        directories = {}.fromkeys(['games', 'configs', 'screenshots', 'capture', 'profiles'])
        for dir_key in directories:
            path = os.path.join(self.datadir, dir_key)
            directories[dir_key] = path
            if not os.path.exists(path):
                os.mkdir(path)
        self.data_directories = directories
        

    def quit(self):
        KApplication.quit(self)


if __name__ == '__main__':
    print "testing module"
    
