from kdeui import KTabWidget

from sdlcfg import SDLConfigWidget
from machinecfg import MachineConfigWidget
from sndcfg import SoundConfigWidget

        
class DosboxConfigTabWidget(KTabWidget):
    def __init__(self, parent, name='DosboxConfigWidget'):
        KTabWidget.__init__(self, parent, name)
        self.sdltab = SDLConfigWidget(self)
        self.insertTab(self.sdltab, 'sdl')
        self.machinetab = MachineConfigWidget(self)
        self.insertTab(self.machinetab, 'machine')
        self.soundtab = SoundConfigWidget(self)
        self.insertTab(self.soundtab, 'sound')
        
