#from qt import SIGNAL, SLOT
#from qt import PYSIGNAL

from qt import QGridLayout
#from qt import QHBoxLayout
from qt import QGroupBox

from qt import QCheckBox
from qt import QLabel


from kdeui import KComboBox
from kdeui import KIntSpinBox

from kfile import KFile
from kfile import KURLRequester

from base import BaseDosboxConfigWidget
from base import ConfigComboBoxWidget
from base import ConfigSpinWidget
from base import ConfigKURLSelectWidget
from base import VerticalGroupBox

class MachineConfigWidget(BaseDosboxConfigWidget):
    def __init__(self, parent, name='SDLConfigWidget'):
        BaseDosboxConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 2
        margin = 0
        space = 1
        self._default_machines = ['vga', 'cga', 'tandy', 'pcjr', 'hercules']
        self._default_scalers = ['none', 'normal2x', 'normal3x', 'advmame2x', 'advmame3x',
                                 'advinterp2x', 'advinterp3x', 'tv2x', 'tv3x',
                                 'rgb2x', 'rgb3x', 'scan2x', 'scan3x']
        self._default_cores = ['simple', 'normal', 'full', 'dynamic']
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'MachineConfigWidgetLayout')
        self.new_stuff()
        
    def new_stuff(self):
        # dosbox group
        self.dosbox_groupbox = VerticalGroupBox(self, 'Dosbox Options')
        self.dosbox_groupbox.setColumns(3)
        # row 1, first two columns
        self.grid.addMultiCellWidget(self.dosbox_groupbox, 1, 1, 0, 1)
        self.language_entry = ConfigKURLSelectWidget(self.dosbox_groupbox,
                                                     'Language file')
        self.memsize_box = ConfigSpinWidget(self.dosbox_groupbox,
                                            'Memory size', suffix='MB')
        self.captures_entry = ConfigKURLSelectWidget(self.dosbox_groupbox,
                                                     'Captures directory', filetype='dir')
            
        # render group
        self.render_groupbox = VerticalGroupBox(self, 'Render Options')
        self.render_groupbox.setColumns(2)
        self.grid.addWidget(self.render_groupbox, 0, 1)
        self.frameskip_box = ConfigSpinWidget(self.render_groupbox,
                                              'Frame skip', suffix=' frames')
        self.aspect_check = QCheckBox(self.render_groupbox)
        self.aspect_check.setText('Aspect correction')
        self.scaler_box = ConfigComboBoxWidget(self.render_groupbox,
                                               'Scaler', self._default_scalers)

        # cpu group
        # make a big number for cycles that should never be needed
        cyclemax = int(1e6)
        self.cpu_groupbox = VerticalGroupBox(self, 'CPU Options')
        self.cpu_groupbox.setColumns(2)
        self.grid.addWidget(self.cpu_groupbox, 0, 0)
        self.core_box = ConfigComboBoxWidget(self.cpu_groupbox,
                                             'Core', self._default_cores)
        self.cycles_box = ConfigSpinWidget(self.cpu_groupbox,
                                           'Cycles', max=cyclemax, suffix=' cycles')
        self.cycleup_box = ConfigSpinWidget(self.cpu_groupbox,
                                            'Cycle up increment', max=cyclemax,
                                            suffix=' cycles')
        self.cycledown_box = ConfigSpinWidget(self.cpu_groupbox,
                                              'Cycle down increment', max=cyclemax,
                                              suffix=' cycles')
        
        
    def old_stuff(self):
        # dosbox group
        self.dosbox_groupbox = QGroupBox(self)
        self.dosbox_groupbox.setTitle('Dosbox Options')
        self.dosbox_groupbox.setOrientation(self.dosbox_groupbox.Vertical)
        self.dosbox_groupbox.setColumns(6)
        # row 1, first two columns
        self.grid.addMultiCellWidget(self.dosbox_groupbox, 1, 1, 0, 1)
        self.language_lbl = QLabel(self.dosbox_groupbox)
        self.language_lbl.setText('Language file')
        self.language_entry = KURLRequester(self.dosbox_groupbox)
        self.memsize_lbl = QLabel(self.dosbox_groupbox)
        self.memsize_lbl.setText('Memory size')
        self.memsize_box = KIntSpinBox(self.dosbox_groupbox)
        self.memsize_box.setMinValue(0)
        self.memsize_box.setSuffix('MB')
        self.captures_lbl = QLabel(self.dosbox_groupbox)
        self.captures_lbl.setText('Captures directory')
        self.captures_entry = KURLRequester(self.dosbox_groupbox)
        self.captures_entry.setMode(KFile.Directory)
        
        # render group
        self.render_groupbox = QGroupBox(self)
        self.render_groupbox.setTitle('Render Options')
        self.render_groupbox.setOrientation(self.render_groupbox.Vertical)
        self.render_groupbox.setColumns(5)
        self.grid.addWidget(self.render_groupbox, 0, 1)
        self.frameskip_lbl = QLabel(self.render_groupbox)
        self.frameskip_lbl.setText('Frame skip')
        self.frameskip_box = KIntSpinBox(self.render_groupbox)
        self.frameskip_box.setMinValue(0)
        self.frameskip_box.setSuffix(' frames')
        self.aspect_check = QCheckBox(self.render_groupbox)
        self.aspect_check.setText('Aspect correction')
        self.scaler_lbl = QLabel(self.render_groupbox)
        self.scaler_lbl.setText('Scaler')
        self.scaler_box = KComboBox(self.render_groupbox)
        self.scaler_box.insertStrList(self._default_scalers)

        # cpu group
        self.cpu_groupbox = QGroupBox(self)
        self.cpu_groupbox.setTitle('Cpu Options')
        self.cpu_groupbox.setOrientation(self.cpu_groupbox.Vertical)
        self.cpu_groupbox.setColumns(8)
        self.grid.addWidget(self.cpu_groupbox, 0, 0)
        self.core_lbl = QLabel(self.cpu_groupbox)
        self.core_lbl.setText('Core')
        self.core_box = KComboBox(self.cpu_groupbox)
        self.core_box.insertStrList(self._default_cores)
        self.cycles_lbl = QLabel(self.cpu_groupbox)
        self.cycles_lbl.setText('Cycles')
        self.cycles_box = KIntSpinBox(self.cpu_groupbox)
        self.cycles_box.setSuffix(' cycles')
        # magic number for maximum cycles (I hope 1 million is good enough)
        self.cycles_box.setMaxValue(1000000)
        self.cycleup_lbl = QLabel('Cycle up increment', self.cpu_groupbox)
        self.cycleup_box = KIntSpinBox(self.cpu_groupbox)
        self.cycleup_box.setSuffix(' cycles')
        # magic number for maximum cycle up increment
        self.cycleup_box.setMaxValue(1000000)
        self.cycledown_lbl = QLabel('Cycle down increment', self.cpu_groupbox)
        self.cycledown_box = KIntSpinBox(self.cpu_groupbox)
        self.cycledown_box.setSuffix(' cycles')
        # magic number for maximum cycle down increment
        self.cycledown_box.setMaxValue(1000000)
        
        
