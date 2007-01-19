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
        text = self.currentText()
        rate, hz = text.split()
        if as_string:
            return rate
        else:
            return int(rate)
        
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

        self.new_stuff()
        
    def new_stuff(self):
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
        self.midi_config_lbl = QLabel('MIDI config', self.midi_groupbox)
        self.midi_config_box = KLineEdit(self.midi_groupbox)

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
        
        #self._default_oplmodes = ['auto', 'cms', 'opl2', 'dualopl2', 'opl3']
        #self.sb_oplmode_box = ConfigComboBoxWidget(self.sblaster_groupbox,
        #                                       'OPL mode', self._default_oplmodes)
        #self.sb_oplrate_box = SampleRateOption(self.sblaster_groupbox,
        #                                       'OPL sample rate')

        
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
        self.gus_ultradir_lbl = QLabel('GUS patches directory', self.gus_groupbox)
        self.gus_ultradir_box =  KURLRequester(self.gus_groupbox)
        self.gus_ultradir_box.setMode(KFile.Directory)

        
    def old_stuff(self):
        # mixer group
        self.mixer_groupbox = QGroupBox(self)
        self.mixer_groupbox.setTitle('Mixer Options')
        self.mixer_groupbox.setOrientation(self.mixer_groupbox.Vertical)
        self.mixer_groupbox.setColumns(7)
        self.grid.addWidget(self.mixer_groupbox, 0, 0)
        self.nosound_check = QCheckBox(self.mixer_groupbox)
        self.nosound_check.setText('Disable sound')
        self.sample_rate_lbl = QLabel('Sample rate', self.mixer_groupbox)
        self.sample_rate_box = KIntSpinBox(self.mixer_groupbox)
        self.sample_rate_box.setSuffix('Hz')
        # magic number for maximum sample rate
        self.sample_rate_box.setMaxValue(44100)
        self.blocksize_lbl = QLabel('Mixer block size', self.mixer_groupbox)
        self.blocksize_box = KIntSpinBox(self.mixer_groupbox)
        self.blocksize_box.setSuffix(' bytes')
        # magic number for maximum block size
        self.blocksize_box.setMaxValue(262144)
        self.prebuffer_lbl = QLabel('Prebuffer', self.mixer_groupbox)
        self.prebuffer_box = KIntSpinBox(self.mixer_groupbox)
        self.prebuffer_box.setSuffix(' msec')
        # magic number for maximum prebuffer (10 secs)
        self.prebuffer_box.setMaxValue(10000)

        # midi group
        self.midi_groupbox = QGroupBox(self)
        self.midi_groupbox.setTitle('Midi Options')
        self.midi_groupbox.setOrientation(self.midi_groupbox.Vertical)
        self.midi_groupbox.setColumns(6)
        self.grid.addWidget(self.midi_groupbox, 0, 1)
        self.mpu401_lbl = QLabel('mpu401 type', self.midi_groupbox)
        self.mpu401_box = KComboBox(self.midi_groupbox)
        self.mpu401_box.insertStrList(self._default_mpu401_types)
        self.midi_device_lbl = QLabel('MIDI device', self.midi_groupbox)
        self.midi_device_box = KComboBox(self.midi_groupbox)
        self.midi_device_box.insertStrList(self._default_midi_devices)
        self.midi_config_lbl = QLabel('MIDI config', self.midi_groupbox)
        self.midi_config_box = KLineEdit(self.midi_groupbox)

        # sblaster group
        self.sblaster_groupbox = QGroupBox(self)
        self.sblaster_groupbox.setTitle('SoundBlaster Options')
        
        
