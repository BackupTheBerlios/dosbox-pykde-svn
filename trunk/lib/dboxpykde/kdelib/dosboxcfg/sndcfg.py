from qt import QGridLayout
from qt import QGroupBox
from qt import QWidget
from qt import QCheckBox
from qt import QLabel
from qt import QSpacerItem
from qt import QSizePolicy

from kdeui import KComboBox
from kdeui import KIntSpinBox
from kdeui import KLineEdit

from kfile import KFile
from kfile import KURLRequester

from base import BaseDosboxConfigWidget
from base import ConfigComboBoxWidget
from base import ConfigSpinWidget
from base import ConfigLineEditWidget
from base import ConfigKURLSelectWidget
from base import VerticalGroupBox

# these common sample rates taken from
# http://en.wikipedia.org/wiki/Sampling_rate
SAMPLE_RATES = ['%s Hz' % r for r in map(str, [8000, 11025, 16000, 22050, 32000, 44100])]

class SampleRateOption(ConfigComboBoxWidget):
    def __init__(self, parent, labeltext='Sample rate', name='SampleRateOption'):
        ConfigComboBoxWidget.__init__(self, parent, labeltext,
                                      SAMPLE_RATES, name=name)

    # helper method to strip "Hz" suffix
    def get_rate(self, as_string=False):
        text = self.mainwidget.currentText()
        text = str(text)
        rate, hz = text.split()
        if as_string:
            return rate
        else:
            return int(rate)

    def set_rate(self, rate):
        if type(rate) is int:
            rate = str(rate)
        rate = '%s Hz' % rate
        if rate not in self._mainlist:
            raise ValueError, '%s not in list of sample rates' % rate
        index = self._mainlist.index(rate)
        self.mainwidget.setCurrentItem(index)

    def get_config_option(self):
        return self.get_rate()

    def set_config_option(self, option):
        self.set_rate(option)
        
class SoundBlasterHardwareOptions(QWidget):
    def __init__(self, parent, name='SoundBlasterHardwareOptions'):
        QWidget.__init__(self, parent, name)
        numrows = 2
        numcols = 3
        margin = 0
        space = 1
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'SoundBlasterHardwareOptionsLayout')
        self.base_box = ConfigSpinWidget(self, 'I/O address',
                                               max=1000)
        self.grid.addWidget(self.base_box, 0, 0)
        self.irq_box = ConfigSpinWidget(self, 'IRQ', min=3, max=15)
        self.grid.addWidget(self.irq_box, 1, 0)
        self.dma_box = ConfigSpinWidget(self, 'DMA')
        self.grid.addWidget(self.dma_box, 0, 2)
        self.hdma_box = ConfigSpinWidget(self, 'High DMA')
        self.grid.addWidget(self.hdma_box, 1, 2)

    def get_config_options(self):
        opts = {}
        opts['sbbase'] = self.base_box.get_config_option()
        opts['irq'] = self.irq_box.get_config_option()
        opts['dma'] = self.dma_box.get_config_option()
        opts['hdma'] = self.hdma_box.get_config_option()
        return opts

    def set_config_options(self, opts):
        self.base_box.set_config_option(opts['sbbase'])
        self.irq_box.set_config_option(opts['irq'])
        self.dma_box.set_config_option(opts['dma'])
        self.hdma_box.set_config_option(opts['hdma'])
        
class SoundBlasterOPLOptions(QWidget):
    def __init__(self, parent, name='SoundBlasterHardwareOptions'):
        QWidget.__init__(self, parent, name)
        numrows = 2
        numcols = 1
        margin = 0
        space = 1
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'SoundBlasterHardwareOptionsLayout')
        self._default_oplmodes = ['auto', 'cms', 'opl2', 'dualopl2', 'opl3']
        self.oplmode_box = ConfigComboBoxWidget(self,
                                               'OPL mode', self._default_oplmodes)
        self.grid.addWidget(self.oplmode_box, 0, 0)
        self.oplrate_box = SampleRateOption(self, 'OPL sample rate')
        self.grid.addWidget(self.oplrate_box, 1, 0)

    def get_config_options(self):
        opts = {}
        opts['oplmode'] = self.oplmode_box.get_config_option()
        opts['oplrate'] = self.oplrate_box.get_config_option()
        return opts

    def set_config_options(self, opts):
        self.oplmode_box.set_config_option(opts['oplmode'])
        self.oplrate_box.set_config_option(opts['oplrate'])
        
        
class GusHardwareOptions(QWidget):
    def __init__(self, parent, name='GusHardwareOptions'):
        QWidget.__init__(self, parent, name)
        numrows = 2
        numcols = 3
        margin = 0
        space = 1
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'GusHardwareOptionsLayout')
        self.base_box = ConfigSpinWidget(self, 'I/O address',
                                         max=1000)
        self.grid.addWidget(self.base_box, 0, 0)
        self.irq1_box = ConfigSpinWidget(self, 'IRQ 1', min=3, max=15)
        self.grid.addWidget(self.irq1_box, 0, 1)
        self.irq2_box = ConfigSpinWidget(self, 'IRQ 2', min=3, max=15)
        self.grid.addWidget(self.irq2_box, 1, 1)
        self.dma1_box = ConfigSpinWidget(self, 'DMA 1')
        self.grid.addWidget(self.dma1_box, 0, 2)
        self.dma2_box = ConfigSpinWidget(self, 'DMA 2')
        self.grid.addWidget(self.dma2_box, 1, 2)

    def get_config_options(self):
        opts = {}
        opts['gusbase'] = self.base_box.get_config_option()
        opts['irq1'] = self.irq1_box.get_config_option()
        opts['irq2'] = self.irq2_box.get_config_option()
        opts['dma1'] = self.dma1_box.get_config_option()
        opts['dma2'] = self.dma2_box.get_config_option()
        
        return opts

    def set_config_options(self, opts):
        self.base_box.set_config_option(opts['gusbase'])
        self.irq1_box.set_config_option(opts['irq1'])
        self.irq2_box.set_config_option(opts['irq2'])
        self.dma1_box.set_config_option(opts['dma1'])
        self.dma2_box.set_config_option(opts['dma2'])
        
class SoundConfigWidget(BaseDosboxConfigWidget):
    def __init__(self, parent, name='SDLConfigWidget'):
        BaseDosboxConfigWidget.__init__(self, parent, name=name)
        numrows = 4
        numcols = 3
        margin = 10
        space = 7
        self._default_mpu401_types = ['none', 'uart', 'intelligent']
        self._default_midi_devices = ['default', 'none', 'alsa', 'oss', 'coreaudio', 'win32']
        self._default_sbtypes = ['none', 'sb1', 'sb2', 'sbpro1', 'sbpro2', 'sb16']
        self._default_tandyopts = ['auto', 'on', 'off']
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'SDLConfigWidgetLayout')
        for section in ['mixer', 'midi', 'sblaster', 'gus', 'speaker']:
            self.localconfig.add_section(section)
        

        # mixer group
        self.mixer_groupbox = VerticalGroupBox(self, 'Mixer Options')
        self.mixer_groupbox.setColumns(4)
        self.grid.addWidget(self.mixer_groupbox, 0, 0)
        self.nosound_check = QCheckBox(self.mixer_groupbox)
        self.nosound_check.setText('Disable sound')
        self.sample_rate_box = SampleRateOption(self.mixer_groupbox,
                                                'Sample rate')
        # magic number for maximum block size
        self.blocksize_box = ConfigSpinWidget(self.mixer_groupbox,
                                              'Mixer block size', min=0, max=262144,
                                              suffix=' bytes')
        # magic number for maximum prebuffer (10 secs)
        self.prebuffer_box = ConfigSpinWidget(self.mixer_groupbox,
                                              'Prebuffer', min=0, max=10000,
                                              suffix=' msec')
        
        
        # midi group
        self.midi_groupbox = VerticalGroupBox(self, 'MIDI Options')
        self.midi_groupbox.setColumns(4)
        self.grid.addWidget(self.midi_groupbox, 0, 1)
        self.mpu401_box = ConfigComboBoxWidget(self.midi_groupbox,
                                               'mpu401 type', self._default_mpu401_types)
        self.midi_device_box = ConfigComboBoxWidget(self.midi_groupbox,
                                                    'MIDI device', self._default_midi_devices)
        self.midi_config_box = ConfigLineEditWidget(self.midi_groupbox,
                                                    'MIDI config')
        
        # speaker group
        self.speaker_groupbox = VerticalGroupBox(self, 'PC Speaker Options')
        self.speaker_groupbox.setColumns(2)
        self.grid.addMultiCellWidget(self.speaker_groupbox, 1, 1, 0, 0)
        self.enable_speaker_check = QCheckBox(self.speaker_groupbox)
        self.enable_speaker_check.setText('Enable PC speaker emulation')
        self.pc_rate_box = SampleRateOption(self.speaker_groupbox,
                                        'Sample rate of PC speaker')
        self.enable_tandy_box = ConfigComboBoxWidget(self.speaker_groupbox,
                                                     'Enable Tandy Sound System emulation',
                                                     self._default_tandyopts)
        self.tandy_rate_box = SampleRateOption(self.speaker_groupbox,
                                               'Sample rate of Tandy Sound System')
        self.enable_disney_check = QCheckBox(self.speaker_groupbox)
        self.enable_disney_check.setText('Enable Disney Sound Source emulation')
        
        # sblaster group
        self.sblaster_groupbox = VerticalGroupBox(self, 'SoundBlaster Options')
        self.sblaster_groupbox.setColumns(2)
        self.grid.addWidget(self.sblaster_groupbox, 2, 0)
        self.sbtype_box = ConfigComboBoxWidget(self.sblaster_groupbox,
                                               'SoundBlaster type', self._default_sbtypes)
        self.sblaster_hwopt_groupbox = VerticalGroupBox(self.sblaster_groupbox,
                                                        'SoundBlaster Hardware Options')
        self.sblaster_hwopt_groupbox.setColumns(1)
        self.sblaster_hwopt_box = SoundBlasterHardwareOptions(self.sblaster_hwopt_groupbox)
        
        self.sb_mixer_check = QCheckBox(self.sblaster_groupbox)
        self.sb_mixer_check.setText('SoundBlaster modifies dosbox mixer')
        self.sblaster_oplopt_groupbox = VerticalGroupBox(self.sblaster_groupbox,
                                                         'SoundBlaster OPL Options')
        self.sblaster_oplopt_groupbox.setColumns(1)
        self.sblaster_oplopt_box = SoundBlasterOPLOptions(self.sblaster_oplopt_groupbox)
        
        # gus group
        self.gus_groupbox = VerticalGroupBox(self, 'Gravis Ultrasound Options')
        self.gus_groupbox.setColumns(5)
        #self.grid.addWidget(self.gus_groupbox, 2, 1)
        self.grid.addMultiCellWidget(self.gus_groupbox, 1, 2, 1, 1)
        self.enable_gus_check = QCheckBox(self.gus_groupbox)
        self.enable_gus_check.setText('Enable Gravis Ultrasound emulation')
        self.gus_hwopt_groupbox = VerticalGroupBox(self.gus_groupbox,
                                                   'Gravis Ultrasound hardware options')
        self.gus_hwopt_groupbox.setColumns(1)
        self.gus_hwopt_box = GusHardwareOptions(self.gus_hwopt_groupbox)
        self.gus_rate_box = SampleRateOption(self.gus_groupbox)
        self.gus_ultradir_box = ConfigKURLSelectWidget(self.gus_groupbox,
                                                       'GUS patches directory', filetype='dir')
        
        
    def set_config(self, configobj):
        self.mainconfig = configobj
        # some assignments to help with typing
        mixer = 'mixer'
        midi = 'midi'
        sblaster = 'sblaster'
        gus = 'gus'
        speaker = 'speaker'
        cfg = self.mainconfig
        # set the various config widgets
        # mixer section
        nosound = cfg.getboolean(mixer, 'nosound')
        self.nosound_check.setChecked(nosound)
        rate = cfg.getint(mixer, 'rate')
        self.sample_rate_box.set_config_option(rate)
        blocksize = cfg.getint(mixer, 'blocksize')
        self.blocksize_box.set_config_option(blocksize)
        prebuffer = cfg.getint(mixer, 'prebuffer')
        self.prebuffer_box.set_config_option(prebuffer)
        # midi section
        mpu401 = cfg.get(midi, 'mpu401')
        self.mpu401_box.set_config_option(mpu401)
        device = cfg.get(midi, 'device')
        self.midi_device_box.set_config_option(device)
        midi_config = cfg.get(midi, 'config')
        self.midi_config_box.set_config_option(midi_config)
        # sblaster section
        sbtype = cfg.get(sblaster, 'sbtype')
        self.sbtype_box.set_config_option(sbtype)
        opts = {}
        for opt in ['sbbase', 'irq', 'dma', 'hdma']:
            opts[opt] = cfg.getint(sblaster, opt)
        self.sblaster_hwopt_box.set_config_options(opts)
        mixer = cfg.getboolean(sblaster, 'mixer')
        self.sb_mixer_check.setChecked(mixer)
        opts = {}
        opts['oplmode'] = cfg.get(sblaster, 'oplmode')
        opts['oplrate'] = cfg.getint(sblaster, 'oplrate')
        self.sblaster_oplopt_box.set_config_options(opts)
        
        # gus section
        enable_gus = cfg.getboolean(gus, 'gus')
        self.enable_gus_check.setChecked(enable_gus)
        gusrate = cfg.getint(gus, 'gusrate')
        self.gus_rate_box.set_config_option(gusrate)
        opts = {}
        for opt in ['gusbase', 'irq1', 'irq2', 'dma1', 'dma2']:
            opts[opt] = cfg.getint(gus, opt)
        self.gus_hwopt_box.set_config_options(opts)
        ultradir = cfg.get(gus, 'ultradir')
        self.gus_ultradir_box.set_config_option(ultradir)
        # speaker section
        pcspeaker = cfg.getboolean(speaker, 'pcspeaker')
        self.enable_speaker_check.setChecked(pcspeaker)
        pcrate = cfg.getint(speaker, 'pcrate')
        self.pc_rate_box.set_config_option(pcrate)
        tandy = cfg.get(speaker, 'tandy')
        self.enable_tandy_box.set_config_option(tandy)
        tandyrate = cfg.getint(speaker, 'tandyrate')
        self.tandy_rate_box.set_config_option(tandyrate)
        disney = cfg.getboolean(speaker, 'disney')
        self.enable_disney_check.setChecked(disney)
        

    def get_config(self):
        # some assignments to help with typing
        mixer = 'mixer'
        midi = 'midi'
        sblaster = 'sblaster'
        gus = 'gus'
        speaker = 'speaker'
        cfg = self.localconfig
        # get config values from the various widgets
        # mixer section
        nosound = self._get_bool_for_config(self.nosound_check)
        cfg.set(mixer, 'nosound', nosound)
        rate = self.sample_rate_box.get_config_option()
        cfg.set(mixer, 'rate', rate)
        blocksize = self.blocksize_box.get_config_option()
        cfg.set(mixer, 'blocksize', blocksize)
        prebuffer = self.prebuffer_box.get_config_option()
        cfg.set(mixer, 'prebuffer', prebuffer)
        # midi section
        mpu401 = self.mpu401_box.get_config_option()
        cfg.set(midi, 'mpu401', mpu401)
        device = self.midi_device_box.get_config_option()
        cfg.set(midi, 'device', device)
        midi_config = self.midi_config_box.get_config_option()
        cfg.set(midi, 'config', midi_config)
        # sblaster section
        sbtype = self.sbtype_box.get_config_option()
        cfg.set(sblaster, 'sbtype', sbtype)
        opts = self.sblaster_hwopt_box.get_config_options()
        for opt, value in opts.items():
            cfg.set(sblaster, opt, value)
        mixer = self._get_bool_for_config(self.sb_mixer_check)
        cfg.set(sblaster, 'mixer', mixer)
        opts = self.sblaster_oplopt_box.get_config_options()
        for opt, value in opts.items():
            cfg.set(sblaster, opt, value)
        # gus section
        enable_gus = self._get_bool_for_config(self.enable_gus_check)
        cfg.set(gus, 'gus', enable_gus)
        gusrate = self.gus_rate_box.get_config_option()
        cfg.set(gus, 'gusrate', gusrate)
        opts = self.gus_hwopt_box.get_config_options()
        for opt, value in opts.items():
            cfg.set(gus, opt, value)
        ultradir = self.gus_ultradir_box.get_config_option()
        cfg.set(gus, 'ultradir', ultradir)
        # speaker section
        pcspeaker = self._get_bool_for_config(self.enable_speaker_check)
        cfg.set(speaker, 'pcspeaker', pcspeaker)
        pcrate = self.pc_rate_box.get_config_option()
        cfg.set(speaker, 'pcrate', pcrate)
        tandy = self.enable_tandy_box.get_config_option()
        cfg.set(speaker, 'tandy', tandy)
        tandyrate = self.tandy_rate_box.get_config_option()
        cfg.set(speaker, 'tandyrate', tandyrate)
        disney = self._get_bool_for_config(self.enable_disney_check)
        cfg.set(speaker, 'disney', disney)
        # done 
        return self.localconfig
        
