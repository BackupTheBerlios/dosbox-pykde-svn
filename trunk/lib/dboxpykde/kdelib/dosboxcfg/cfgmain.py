from StringIO import StringIO
from ConfigParser import ConfigParser

from kdeui import KTabWidget

from sdlcfg import SDLConfigWidget
from machinecfg import MachineConfigWidget
from sndcfg import SoundConfigWidget

# testing imports
from kdeui import KPushButton
from qt import SIGNAL
from qt import QWidget
from qt import QGridLayout
from kdeui import KTextBrowser
from StringIO import StringIO
# end testing imports

# class for testing config widgets
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
        
class DosboxConfigTabWidget(KTabWidget):
    def __init__(self, parent, name='DosboxConfigWidget'):
        KTabWidget.__init__(self, parent, name)
        self.sdltab = SDLConfigWidget(self)
        self.insertTab(self.sdltab, 'sdl')
        self.machinetab = MachineConfigWidget(self)
        self.insertTab(self.machinetab, 'machine')
        self.soundtab = SoundConfigWidget(self)
        self.insertTab(self.soundtab, 'sound')
        # testing stuff
        self.testtab = TestConfigTab(self)
        self.insertTab(self.testtab, 'test me')
        self.connect(self.testtab.button, SIGNAL('clicked()'), self.get_config)        

    def get_config(self):
        sdlcfg = self.sdltab.get_config()
        machinecfg = self.machinetab.get_config()
        soundcfg = self.soundtab.get_config()
        mainconfig = ConfigParser()
        self._import_new_config(mainconfig, sdlcfg)
        self._import_new_config(mainconfig, machinecfg)
        self._import_new_config(mainconfig, soundcfg)
        # testing stuff
        self.testtab.set_config(mainconfig)
        return mainconfig
    
        
    def _import_new_config(self, mainconfig, localconfig):
        cfile = StringIO()
        localconfig.write(cfile)
        cfile.seek(0)
        mainconfig.readfp(cfile)
        cfile.close()
        
    def set_config(self, configobj):
        self.sdltab.set_config(configobj)
        self.machinetab.set_config(configobj)
        self.soundtab.set_config(configobj)
        
