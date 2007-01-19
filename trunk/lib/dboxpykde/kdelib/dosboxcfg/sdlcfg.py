from qt import SIGNAL, SLOT
from qt import PYSIGNAL

from qt import QGridLayout
#from qt import QHBoxLayout
from qt import QGroupBox

from qt import QCheckBox
from qt import QLabel


from kdeui import KComboBox
from kdeui import KIntSpinBox

from kfile import KURLRequester

from base import BaseDosboxConfigWidget

from base import ConfigComboBoxWidget
from base import ConfigSpinWidget
from base import VerticalGroupBox

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
        self.new_stuff()
    
    def new_stuff(self):
        # fullscreen group
        self.fullscreen_groupbox = VerticalGroupBox(self, 'Fullscreen Options')
        self.fullscreen_groupbox.setColumns(2)
        self.grid.addWidget(self.fullscreen_groupbox, 0, 0)
        self.fullscreen_check = QCheckBox(self.fullscreen_groupbox)
        self.fullscreen_check.setText('fullscreen')
        self.tooltips.add(self.fullscreen_check, "Run dosbox in fullscreen")
        self.fulldouble_check = QCheckBox(self.fullscreen_groupbox)
        self.fulldouble_check.setText('full&double')
        self.tooltips.add(self.fulldouble_check, "Use double buffering in fullscreen")
        
        # resolution group
        self.resolution_groupbox = VerticalGroupBox(self, 'Resolution Options')
        self.resolution_groupbox.setColumns(4)
        self.grid.addWidget(self.resolution_groupbox, 0, 1)
        self.fullresolution_box = ConfigComboBoxWidget(self.resolution_groupbox,
                                                       'fullscreen resolution', self._default_resolutions)
        self.tooltips.add(self.fullresolution_box, "Resolution when running in fullscreen")

        self.windowresolution_box = ConfigComboBoxWidget(self.resolution_groupbox,
                                                         'windowed resolution', self._default_resolutions)
        self.tooltips.add(self.windowresolution_box, "Resolution when running in a window")
        
        # misc group
        self.misc_groupbox = VerticalGroupBox(self, 'Misc. Options')
        self.misc_groupbox.setColumns(3)
        self.grid.addWidget(self.misc_groupbox, 1, 0)
        self.output_box = ConfigComboBoxWidget(self.misc_groupbox,
                                               'Output', self._default_outputs)
        self.waitonerror_check = QCheckBox(self.misc_groupbox)
        self.waitonerror_check.setText('Wait on error')
        self.tooltips.add(self.waitonerror_check,
                          "Wait before closing window if dosbox has an error")
        
        # mouse group
        self.mouse_groupbox = VerticalGroupBox(self, 'Mouse Options')
        self.mouse_groupbox.setColumns(3)
        self.grid.addWidget(self.mouse_groupbox, 1, 1)
        self.autolock_check = QCheckBox(self.mouse_groupbox)
        self.autolock_check.setText('autolock')
        self.tooltips.add(self.autolock_check,
                          "Clicking in the dosbox window automatically locks mouse")
        self.sensitivity_box = ConfigSpinWidget(self.mouse_groupbox,
                                                'Mouse sensitivity', min=1, max=100,
                                                suffix='%')
        self.tooltips.add(self.sensitivity_box, "How sensitive the mouse is")

        # keyboard group
        self.keyboard_groupbox = VerticalGroupBox(self, 'Keyboard Options')
        self.keyboard_groupbox.setColumns(3)
        # add to row 2, first two columns
        self.grid.addMultiCellWidget(self.keyboard_groupbox, 2, 2, 0, 1)
        self.usescancodes_check = QCheckBox(self.keyboard_groupbox)
        self.usescancodes_check.setText('usescancodes')
        self.tooltips.add(self.usescancodes_check,
                          "Avoid use of symkeys")
        self.mapper_lbl = QLabel(self.keyboard_groupbox)
        self.mapper_lbl.setText('mapperfile (File used for key mappings)')
        self.tooltips.add(self.mapper_lbl, "File used for key mappings")
        self.mapper_entry = KURLRequester(self.keyboard_groupbox)

        # priority group
        self.priority_groupbox = QGroupBox(self)
        self.priority_groupbox.setTitle('Priority Options')
        self.priority_groupbox.setColumns(2)
        #self.grid.addWidget(self.priority_groupbox, 3, 0)
        # add to row 3 first two columns
        self.grid.addMultiCellWidget(self.priority_groupbox, 3, 3, 0, 1)
        self.focused_box = ConfigComboBoxWidget(self.priority_groupbox,
                                                'focused', self._default_priorities)
        self.tooltips.add(self.focused_box, "Priority level for dosbox when focused")
        self.unfocused_box = ConfigComboBoxWidget(self.priority_groupbox,
                                                  'unfocused', self._default_priorities)
        self.tooltips.add(self.unfocused_box,
                          "Priority level for dosbox when unfocused or minimized")
        
        
    def old_stuff(self):
        # fullscreen group
        self.fullscreen_groupbox = QGroupBox(self)
        self.fullscreen_groupbox.setTitle('Fullscreen Options')
        self.fullscreen_groupbox.setOrientation(self.fullscreen_groupbox.Vertical)
        self.fullscreen_groupbox.setColumns(2)
        self.grid.addWidget(self.fullscreen_groupbox, 0, 0)
        self.fullscreen_check = QCheckBox(self.fullscreen_groupbox)
        self.fullscreen_check.setText('fullscreen')
        self.tooltips.add(self.fullscreen_check, "Run dosbox in fullscreen")
        self.fulldouble_check = QCheckBox(self.fullscreen_groupbox)
        self.fulldouble_check.setText('full&double')
        self.tooltips.add(self.fulldouble_check, "Use double buffering in fullscreen")
        
        # resolution group
        self.resolution_groupbox = QGroupBox(self)
        self.resolution_groupbox.setTitle('Resolutions')
        self.resolution_groupbox.setOrientation(self.resolution_groupbox.Vertical)
        self.resolution_groupbox.setColumns(4)
        self.grid.addWidget(self.resolution_groupbox, 0, 1)
        self.fullresolution_lbl = QLabel(self.resolution_groupbox)
        self.fullresolution_lbl.setText('fullresolution')
        self.fullresolution_box = KComboBox(self.resolution_groupbox)
        self.fullresolution_box.insertStrList(self._default_resolutions)
        self.tooltips.add(self.fullresolution_box, "Resolution when running in fullscreen")
        self.windowresolution_lbl = QLabel(self.resolution_groupbox)
        self.windowresolution_lbl.setText('windowresolution')
        self.windowresolution_box = KComboBox(self.resolution_groupbox)
        self.windowresolution_box.insertStrList(self._default_resolutions)
        self.tooltips.add(self.windowresolution_box, "Resolution when running in a window")
        
        # misc group
        self.misc_groupbox = QGroupBox(self)
        self.misc_groupbox.setTitle('Misc. Options')
        self.misc_groupbox.setOrientation(self.misc_groupbox.Vertical)
        self.misc_groupbox.setColumns(3)
        self.grid.addWidget(self.misc_groupbox, 1, 0)
        self.output_lbl = QLabel(self.misc_groupbox)
        self.output_lbl.setText('output')
        self.output_box = KComboBox(self.misc_groupbox)
        self.output_box.insertStrList(self._default_outputs)
        self.waitonerror_check = QCheckBox(self.misc_groupbox)
        self.waitonerror_check.setText('Wait on error')
        self.tooltips.add(self.waitonerror_check,
                          "Wait before closing window if dosbox has an error")
        
        # mouse group
        self.mouse_groupbox = QGroupBox(self)
        self.mouse_groupbox.setTitle('Mouse Options')
        self.mouse_groupbox.setOrientation(self.mouse_groupbox.Vertical)
        self.mouse_groupbox.setColumns(3)
        self.grid.addWidget(self.mouse_groupbox, 1, 1)
        self.autolock_check = QCheckBox(self.mouse_groupbox)
        self.autolock_check.setText('autolock')
        self.tooltips.add(self.autolock_check,
                          "Clicking in the dosbox window automatically locks mouse")
        self.sensitivity_lbl = QLabel(self.mouse_groupbox)
        self.sensitivity_lbl.setText('sensitivity')
        self.sensitivity_box = KIntSpinBox(self.mouse_groupbox)
        self.sensitivity_box.setMinValue(1)
        self.sensitivity_box.setMaxValue(100)
        self.sensitivity_box.setSuffix('%')
        self.tooltips.add(self.sensitivity_box, "How sensitive the mouse is")

        # keyboard group
        self.keyboard_groupbox = QGroupBox(self)
        self.keyboard_groupbox.setTitle('Keyboard Options')
        self.keyboard_groupbox.setOrientation(self.keyboard_groupbox.Vertical)
        self.keyboard_groupbox.setColumns(3)
        #self.grid.addWidget(self.keyboard_groupbox, 2, 0)
        # add to row 2, first two columns
        self.grid.addMultiCellWidget(self.keyboard_groupbox, 2, 2, 0, 1)
        self.usescancodes_check = QCheckBox(self.keyboard_groupbox)
        self.usescancodes_check.setText('usescancodes')
        self.tooltips.add(self.usescancodes_check,
                          "Avoid use of symkeys")
        self.mapper_lbl = QLabel(self.keyboard_groupbox)
        self.mapper_lbl.setText('mapperfile (File used for key mappings)')
        self.tooltips.add(self.mapper_lbl, "File used for key mappings")
        self.mapper_entry = KURLRequester(self.keyboard_groupbox)

        # priority group
        self.priority_groupbox = QGroupBox(self)
        self.priority_groupbox.setTitle('Priority Options')
        self.priority_groupbox.setColumns(4)
        #self.grid.addWidget(self.priority_groupbox, 3, 0)
        # add to row 3 first two columns
        self.grid.addMultiCellWidget(self.priority_groupbox, 3, 3, 0, 1)
        self.focused_lbl = QLabel(self.priority_groupbox)
        self.focused_lbl.setText('focused')
        self.focused_box = KComboBox(self.priority_groupbox)
        self.focused_box.insertStrList(self._default_priorities)
        self.tooltips.add(self.focused_box, "Priority level for dosbox when focused")
        self.unfocused_lbl = QLabel(self.priority_groupbox)
        self.unfocused_lbl.setText('unfocused')
        self.unfocused_box = KComboBox(self.priority_groupbox)
        self.unfocused_box.insertStrList(self._default_priorities)
        self.tooltips.add(self.unfocused_box,
                          "Priority level for dosbox when unfocused or minimized")
        
        
