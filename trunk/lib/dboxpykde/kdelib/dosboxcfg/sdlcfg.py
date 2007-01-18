from qt import SIGNAL, SLOT
from qt import PYSIGNAL
from qt import QWidget

from qt import QGridLayout
from qt import QGroupBox
from qt import QCheckBox
from qt import QLabel

from kdeui import KTabWidget
from kdeui import KComboBox
from kdeui import KIntSpinBox

class BaseDosboxConfigWidget(QWidget):
    def __init__(self, parent, name='BaseDosboxConfigWidget'):
        QWidget.__init__(self, parent, name)
        
class SDLConfigWidget(BaseDosboxConfigWidget):
    def __init__(self, parent, name='SDLConfigWidget'):
        BaseDosboxConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 2
        margin = 0
        space = 1
        self._default_resolutions = ['original', '640x480', '800x600', '1024x768']
        self._default_outputs = ['surface', 'overlay', 'opengl', 'openglnb', 'ddraw']
        self._default_priorities = ['lowest', 'lower', 'normal', 'higher', 'highest']
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'SDLConfigWidgetLayout')
        # fullscreen group
        self.fullscreen_groupbox = QGroupBox(self)
        self.fullscreen_groupbox.setTitle('Fullscreen Options')
        self.fullscreen_groupbox.setOrientation(self.fullscreen_groupbox.Vertical)
        self.fullscreen_groupbox.setColumns(2)
        self.grid.addWidget(self.fullscreen_groupbox, 0, 0)
        self.fullscreen_check = QCheckBox(self.fullscreen_groupbox)
        self.fullscreen_check.setText('fullscreen')
        self.fulldouble_check = QCheckBox(self.fullscreen_groupbox)
        self.fulldouble_check.setText('fulldouble')
        # resolution group
        self.resolution_groupbox = QGroupBox(self)
        self.resolution_groupbox.setTitle('Resolutions')
        self.resolution_groupbox.setOrientation(self.resolution_groupbox.Vertical)
        self.resolution_groupbox.setColumns(4)
        self.grid.addWidget(self.resolution_groupbox, 1, 0)
        self.fullresolution_lbl = QLabel(self.resolution_groupbox)
        self.fullresolution_lbl.setText('fullresolution')
        self.fullresolution_box = KComboBox(self.resolution_groupbox)
        self.fullresolution_box.insertStrList(self._default_resolutions)
        self.windowresolution_lbl = QLabel(self.resolution_groupbox)
        self.windowresolution_lbl.setText('windowresolution')
        self.windowresolution_box = KComboBox(self.resolution_groupbox)
        self.windowresolution_box.insertStrList(self._default_resolutions)
        # output group
        self.output_groupbox = QGroupBox(self)
        self.output_groupbox.setTitle('Output')
        self.output_groupbox.setOrientation(self.output_groupbox.Vertical)
        self.output_groupbox.setColumns(2)
        self.output_lbl = QLabel(self.output_groupbox)
        self.output_lbl.setText('output')
        self.output_box = KComboBox(self.output_groupbox)
        self.output_box.insertStrList(self._default_outputs)
        self.grid.addWidget(self.output_groupbox, 1, 2)
        # mouse group
        self.mouse_groupbox = QGroupBox(self)
        self.mouse_groupbox.setTitle('Mouse Options')
        self.mouse_groupbox.setOrientation(self.mouse_groupbox.Vertical)
        self.mouse_groupbox.setColumns(3)
        self.grid.addWidget(self.mouse_groupbox, 0, 2)
        self.autolock_check = QCheckBox(self.mouse_groupbox)
        self.autolock_check.setText('autolock')
        self.sensitivity_lbl = QLabel(self.mouse_groupbox)
        self.sensitivity_lbl.setText('sensitivity')
        self.sensitivity_box = KIntSpinBox(self.mouse_groupbox)
        self.sensitivity_box.setMinValue(1)
        self.sensitivity_box.setMaxValue(100)
        self.sensitivity_box.setSuffix('%')
        
        
class DosboxConfigTabWidget(KTabWidget):
    def __init__(self, parent, name='DosboxConfigWidget'):
        KTabWidget.__init__(self, parent, name)
        self.sdltab = SDLConfigWidget(self)
        self.insertTab(self.sdltab, 'sdl')
        
        
