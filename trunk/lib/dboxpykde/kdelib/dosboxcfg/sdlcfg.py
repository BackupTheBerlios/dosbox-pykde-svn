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
from base import ConfigKURLSelectWidget
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
        self.localconfig.add_section('sdl')
        
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
        self.mapper_entry = ConfigKURLSelectWidget(self.keyboard_groupbox,
                                                   'mapperfile (File used for key mappings)')
        self.tooltips.add(self.mapper_entry, "File used for key mappings")


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
        
    def set_config(self, configobj):
        self.mainconfig = configobj
        # some assignments to help with typing
        sdl = 'sdl'
        cfg = self.mainconfig
        # set the various config widgets
        fullscreen = cfg.getboolean(sdl, 'fullscreen')
        self.fullscreen_check.setChecked(fullscreen)
        fulldouble = cfg.getboolean(sdl, 'fulldouble')
        self.fulldouble_check.setChecked(fulldouble)
        fullresolution = cfg.get(sdl, 'fullresolution')
        self.fullresolution_box.set_config_option(fullresolution)
        windowresolution = cfg.get(sdl, 'windowresolution')
        self.windowresolution_box.set_config_option(windowresolution)
        output = cfg.get(sdl, 'output')
        self.output_box.set_config_option(output)
        waitonerror = cfg.getboolean(sdl, 'waitonerror')
        self.waitonerror_check.setChecked(waitonerror)
        autolock = cfg.getboolean(sdl, 'autolock')
        self.autolock_check.setChecked(autolock)
        sensitivity = cfg.getint(sdl, 'sensitivity')
        self.sensitivity_box.set_config_option(sensitivity)
        usescancodes = cfg.getboolean(sdl, 'usescancodes')
        self.usescancodes_check.setChecked(usescancodes)
        mapperfile = cfg.get(sdl, 'mapperfile')
        self.mapper_entry.set_config_option(mapperfile)
        priorities = cfg.get(sdl, 'priority')
        focused, unfocused = [p.strip() for p in priorities.split(',')]
        self.focused_box.set_config_option(focused)
        self.unfocused_box.set_config_option(unfocused)

    def get_config(self):
        # some assignments to help with typing
        sdl = 'sdl'
        cfg = self.localconfig
        # get config values from the various widgets
        fullscreen = self._get_bool_for_config(self.fullscreen_check)
        cfg.set(sdl, 'fullscreen', fullscreen)
        fulldouble = self._get_bool_for_config(self.fulldouble_check)
        cfg.set(sdl, 'fulldouble', fulldouble)
        fullresolution = self.fullresolution_box.get_config_option()
        cfg.set(sdl, 'fullresolution', fullresolution)
        windowresolution = self.windowresolution_box.get_config_option()
        cfg.set(sdl, 'windowresolution', windowresolution)
        output = self.output_box.get_config_option()
        cfg.set(sdl, 'output', output)
        waitonerror = self._get_bool_for_config(self.waitonerror_check)
        cfg.set(sdl, 'waitonerror', waitonerror)
        autolock = self._get_bool_for_config(self.autolock_check)
        cfg.set(sdl, 'autolock', autolock)
        sensitivity = self.sensitivity_box.get_config_option()
        cfg.set(sdl, 'sensitivity', sensitivity)
        usescancodes = self._get_bool_for_config(self.usescancodes_check)
        cfg.set(sdl, 'usescancodes', usescancodes)
        mapperfile = self.mapper_entry.get_config_option()
        cfg.set(sdl, 'mapperfile', mapperfile)
        # priorities part
        focused = self.focused_box.get_config_option()
        unfocused = self.unfocused_box.get_config_option()
        priority = ','.join([focused, unfocused])
        cfg.set(sdl, 'priority', priority)
        return self.localconfig
