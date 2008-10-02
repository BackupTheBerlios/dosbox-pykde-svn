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

class SerialPortOption(ConfigComboBoxWidget):
    def __init__(self, parent, labeltext, name='SerialPortOption'):
        options = ['disabled', 'dummy', 'modem', 'directserial']
        ConfigComboBoxWidget.__init__(self, parent, labeltext,
                                      options, name=name)
        

class MachineConfigWidget(BaseDosboxConfigWidget):
    def __init__(self, parent, name='SDLConfigWidget'):
        BaseDosboxConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 3
        margin = 10
        space = 7
        self._default_machines = ['vga', 'cga', 'tandy', 'pcjr', 'hercules']
        self._default_scalers = ['none', 'normal2x', 'normal3x', 'advmame2x', 'advmame3x',
                                 'advinterp2x', 'advinterp3x', 'tv2x', 'tv3x',
                                 'rgb2x', 'rgb3x', 'scan2x', 'scan3x']
        self._default_cores = ['simple', 'normal', 'full', 'dynamic', 'auto']
        for section in ['render', 'cpu', 'dosbox', 'dos', 'bios', 'serial', 'ipx']:
            self.localconfig.add_section(section)
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'MachineConfigWidgetLayout')

        # render group
        self.render_groupbox = VerticalGroupBox(self, 'Render Options')
        self.render_groupbox.setColumns(2)
        self.grid.addWidget(self.render_groupbox, 0, 1)
        self.frameskip_box = ConfigSpinWidget(self.render_groupbox,
                                              'Frame skip', suffix=' frames')
        self.tooltips.add(self.frameskip_box, 'How many frames to skip.')
        self.aspect_check = QCheckBox(self.render_groupbox)
        self.aspect_check.setText('Aspect correction')
        self.tooltips.add(self.aspect_check, 'Try to keep aspect ratio.')
        self.scaler_box = ConfigComboBoxWidget(self.render_groupbox,
                                               'Scaler', self._default_scalers)
        self.tooltips.add(self.scaler_box, 'Select size and effect of video')
        # cpu group
        # make a big number for cycles that should never be needed
        cyclemax = int(1e6)
        self.cpu_groupbox = VerticalGroupBox(self, 'CPU Options')
        self.cpu_groupbox.setColumns(2)
        self.grid.addWidget(self.cpu_groupbox, 0, 0)
        self.core_box = ConfigComboBoxWidget(self.cpu_groupbox,
                                             'Core', self._default_cores)
        self.tooltips.add(self.core_box, 'Select type of cpu core')
        self.cycles_box = ConfigSpinWidget(self.cpu_groupbox,
                                           'Cycles', max=cyclemax, suffix=' cycles')
        tt = 'The number of cycles to attempt to perform in a second'
        self.tooltips.add(self.cycles_box, tt)
        self.cycleup_box = ConfigSpinWidget(self.cpu_groupbox,
                                            'Cycle up increment', max=cyclemax,
                                            suffix=' cycles')
        self.cycledown_box = ConfigSpinWidget(self.cpu_groupbox,
                                              'Cycle down increment', max=cyclemax,
                                              suffix=' cycles')
        
        # dosbox group
        self.dosbox_groupbox = VerticalGroupBox(self, 'Dosbox Options')
        self.dosbox_groupbox.setColumns(3)
        # row 1, first two columns
        #self.grid.addMultiCellWidget(self.dosbox_groupbox, 1, 1, 0, 1)
        self.grid.addWidget(self.dosbox_groupbox, 1, 0)
        self.language_entry = ConfigKURLSelectWidget(self.dosbox_groupbox,
                                                     'Language file')
        self.memsize_box = ConfigSpinWidget(self.dosbox_groupbox,
                                            'Memory size', suffix='MB')
        self.captures_entry = ConfigKURLSelectWidget(self.dosbox_groupbox,
                                                     'Captures directory', filetype='dir')
            
        # dos group
        self.dos_groupbox = VerticalGroupBox(self, 'Dos Options')
        self.dos_groupbox.setColumns(3)
        self.grid.addWidget(self.dos_groupbox, 1, 1)
        self.xms_check = QCheckBox(self.dos_groupbox)
        self.xms_check.setText('Enable XMS support')
        self.ems_check = QCheckBox(self.dos_groupbox)
        self.ems_check.setText('Enable EMS support')
        self.umb_check = QCheckBox(self.dos_groupbox)
        self.umb_check.setText('Enable UMB support')

        # peripheral options
        self.peripheral_groupbox = VerticalGroupBox(self, 'Peripheral Options')
        self.peripheral_groupbox.setColumns(1)
        #self.grid.addWidget(self.peripheral_groupbox, 2, 0)
        self.grid.addMultiCellWidget(self.peripheral_groupbox, 2, 2, 0, 2)
        # peripherals in bios section
        self.bios_groupbox = VerticalGroupBox(self.peripheral_groupbox, 'Bios Options')
        self.bios_groupbox.setColumns(1)
        joystick_types = ['none', '2axis', '4axis', 'fcs', 'ch']
        self.joysticktype_box = ConfigComboBoxWidget(self.bios_groupbox,
                                                     'Joystick type', joystick_types)
        # peripherals in serial section
        self.serial_groupbox = VerticalGroupBox(self.peripheral_groupbox, 'Serial Options')
        self.serial_groupbox.setColumns(2)
        self.serial_warning_lbl = QLabel('These options are',
                                         self.serial_groupbox)
        self.serial_warning_lbl2 = QLabel('not fully suported yet.', self.serial_groupbox)
        self.serial1_box = SerialPortOption(self.serial_groupbox, 'Serial 1')
        self.serial2_box = SerialPortOption(self.serial_groupbox, 'Serial 2')
        self.serial3_box = SerialPortOption(self.serial_groupbox, 'Serial 3')
        self.serial4_box = SerialPortOption(self.serial_groupbox, 'Serial 4')

        # ipx options
        self.ipx_groupbox = VerticalGroupBox(self, 'IPX Options')
        self.ipx_groupbox.setColumns(1)
        self.grid.addWidget(self.ipx_groupbox, 1, 2)
        self.ipx_check = QCheckBox(self.ipx_groupbox)
        self.ipx_check.setText('Enable ipx over UDP/IP emulation')
        
    def set_config(self, configobj):
        self.mainconfig = configobj
        # some assignments to help with typing
        render = 'render'
        cpu = 'cpu'
        dosbox = 'dosbox'
        dos = 'dos'
        bios = 'bios'
        serial = 'serial'
        ipx = 'ipx'
        cfg = self.mainconfig
        # set the various config widgets
        # render section
        frameskip = cfg.getint(render, 'frameskip')
        self.frameskip_box.set_config_option(frameskip)
        aspect = cfg.getboolean(render, 'aspect')
        self.aspect_check.setChecked(aspect)
        scaler = cfg.get(render, 'scaler')
        self.scaler_box.set_config_option(scaler)
        # cpu section
        core = cfg.get(cpu, 'core')
        self.core_box.set_config_option(core)
        cycles = cfg.getint(cpu, 'cycles')
        self.cycles_box.set_config_option(cycles)
        cycleup = cfg.getint(cpu, 'cycleup')
        self.cycleup_box.set_config_option(cycleup)
        cycledown = cfg.getint(cpu, 'cycledown')
        self.cycledown_box.set_config_option(cycledown)
        # dosbox section
        language = cfg.get(dosbox, 'language')
        self.language_entry.set_config_option(language)
        memsize = cfg.getint(dosbox, 'memsize')
        self.memsize_box.set_config_option(memsize)
        captures = cfg.get(dosbox, 'captures')
        self.captures_entry.set_config_option(captures)
        # dos section
        xms = cfg.getboolean(dos, 'xms')
        self.xms_check.setChecked(xms)
        ems = cfg.getboolean(dos, 'ems')
        self.ems_check.setChecked(ems)
        umb = cfg.getboolean(dos, 'umb')
        self.umb_check.setChecked(umb)
        # bios section
        joysticktype = cfg.get(bios, 'joysticktype')
        self.joysticktype_box.set_config_option(joysticktype)
        # serial section
        serial1 = cfg.get(serial, 'serial1')
        self.serial1_box.set_config_option(serial1)
        serial2 = cfg.get(serial, 'serial2')
        self.serial2_box.set_config_option(serial2)
        serial3 = cfg.get(serial, 'serial3')
        self.serial3_box.set_config_option(serial3)
        serial4 = cfg.get(serial, 'serial4')
        self.serial4_box.set_config_option(serial4)
        # ipx section
        ipxopt = cfg.getboolean(ipx, ipx)
        self.ipx_check.setChecked(ipxopt)

    def get_config(self):
        # some assignments to help with typing
        render = 'render'
        cpu = 'cpu'
        dosbox = 'dosbox'
        dos = 'dos'
        bios = 'bios'
        serial = 'serial'
        ipx = 'ipx'
        cfg = self.localconfig
        # get config values from the various widgets
        # render section
        frameskip = self.frameskip_box.get_config_option()
        cfg.set(render, 'frameskip', frameskip)
        aspect = self._get_bool_for_config(self.aspect_check)
        cfg.set(render, 'aspect', aspect)
        scaler = self.scaler_box.get_config_option()
        cfg.set(render, 'scaler', scaler)
        # cpu section
        core = self.core_box.get_config_option()
        cfg.set(cpu, 'core', core)
        cycles = self.cycles_box.get_config_option()
        cfg.set(cpu, 'cycles', cycles)
        cycleup = self.cycleup_box.get_config_option()
        cfg.set(cpu, 'cycleup', cycleup)
        cycledown = self.cycledown_box.get_config_option()
        cfg.set(cpu, 'cycledown', cycledown)
        # dosbox section
        language = self.language_entry.get_config_option()
        cfg.set(dosbox, 'language', language)
        memsize = self.memsize_box.get_config_option()
        cfg.set(dosbox, 'memsize', memsize)
        captures = self.captures_entry.get_config_option()
        cfg.set(dosbox, 'captures', captures)
        # dos section
        xms = self._get_bool_for_config(self.xms_check)
        cfg.set(dos, 'xms', xms)
        ems = self._get_bool_for_config(self.ems_check)
        cfg.set(dos, 'ems', ems)
        umb = self._get_bool_for_config(self.umb_check)
        cfg.set(dos, 'umb', umb)
        # bios section
        joysticktype = self.joysticktype_box.get_config_option()
        cfg.set(bios, 'joysticktype', joysticktype)
        # serial section
        serial1 = self.serial1_box.get_config_option()
        cfg.set(serial, 'serial1', serial1)
        serial2 = self.serial2_box.get_config_option()
        cfg.set(serial, 'serial2', serial2)
        serial3 = self.serial3_box.get_config_option()
        cfg.set(serial, 'serial3', serial3)
        serial4 = self.serial4_box.get_config_option()
        cfg.set(serial, 'serial4', serial4)
        # ipx section
        ipxopt = self._get_bool_for_config(self.ipx_check)
        cfg.set(ipx, ipx, ipxopt)
        return self.localconfig
        
