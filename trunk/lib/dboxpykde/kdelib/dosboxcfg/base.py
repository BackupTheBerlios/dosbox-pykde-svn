from ConfigParser import ConfigParser

from qt import QWidget

from qt import QToolTip

from qt import QGridLayout
from qt import QGroupBox
from qt import QLabel


from kdeui import KComboBox
from kdeui import KIntSpinBox
from kdeui import KLineEdit

from kfile import KFile
from kfile import KURLRequester

from dboxpykde.kdelib.base import get_application_pointer

class BaseDosboxConfigWidget(QWidget):
    def __init__(self, parent, name='BaseDosboxConfigWidget'):
        QWidget.__init__(self, parent, name)
        self.app = get_application_pointer()
        self.tooltips = QToolTip
        self.mainconfig = None
        self.localconfig = ConfigParser()
        
    def set_config(self, configobj):
        raise NotImplementedError, 'set_config needs to be defined in subclass'

    def get_config(self):
        raise NotImplementedError, 'get_config needs to be defined in subclass'

    # helper method for checkboxes
    def _get_bool_for_config(self, checkbox):
        value = checkbox.isChecked()
        return str(value).lower()
    

            
class BaseConfigOptionWidget(BaseDosboxConfigWidget):
    def __init__(self, parent, labeltext, optclass,
                 name='BaseConfigOptionWidget'):
        BaseDosboxConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 2
        margin = 0
        space = 1
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'BaseConfigOptionWidgetLayout')
        self.label = QLabel(labeltext, self)
        self.grid.addWidget(self.label, 0, 0)
        self.mainwidget = optclass(self)
        self.grid.addWidget(self.mainwidget, 1, 0)

    def get_config_option(self):
        raise NotImplementedError, 'get_config_option needs to be defined in subclass'

    def set_config_option(self, option):
        raise NotImplementedError, 'set_config_option needs to be defined in subclass'
    
class ConfigComboBoxWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, defaults,
                 name='ConfigComboBoxWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KComboBox, name=name)
        self.mainwidget.insertStrList(defaults)
        self._mainlist = defaults

    def get_config_option(self):
        opt = self.mainwidget.currentText()
        return str(opt)

    def set_config_option(self, option):
        if option not in self._mainlist:
            raise ValueError, '%s not in list of options' % option
        index = self._mainlist.index(option)
        self.mainwidget.setCurrentItem(index)
        
class ConfigLineEditWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext,
                 name='ConfigLineEditWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KLineEdit, name=name)
        
    def get_config_option(self):
        opt = self.mainwidget.text()
        return str(opt)

    def set_config_option(self, option):
        self.mainwidget.setText(option)
        

class ConfigSpinWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, min=0, max=100, suffix='',
                 name='BaseConfigOptionSpinWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KIntSpinBox, name=name)
        self.mainwidget.setMinValue(min)
        self.mainwidget.setMaxValue(max)
        if suffix:
            self.mainwidget.setSuffix(suffix)

    def get_config_option(self):
        return self.mainwidget.value()

    # option needs to be an integer here
    def set_config_option(self, option):
        self.mainwidget.setValue(option)

class ConfigKURLSelectWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, filetype='file',
                 name='ConfigKURLSelectWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext, KURLRequester,
                                        name=name)
        if filetype in ['dir', 'directory']:
            self.mainwidget.setMode(KFile.Directory)

    def get_config_option(self):
        lineEdit = self.mainwidget.lineEdit()
        return str(lineEdit.text())

    def set_config_option(self, option):
        lineEdit = self.mainwidget.lineEdit()
        lineEdit.setText(option)

class VerticalGroupBox(QGroupBox):
    def __init__(self, parent, title):
        QGroupBox.__init__(self, parent)
        self.setTitle(title)
        self.setOrientation(self.Vertical)
        
class BaseConfigOptionWidgetScrapped(QWidget):
    def __init__(self, parent, labeltext, optclass,
                 layout='vertical', name='BaseConfigOptionWidget'):
        QWidget.__init__(self, parent, name)
        self._layout_type = layout
        if self._layout_type == 'vertical':
            self._layout = QVBoxLayout(self)
        elif self._layout_type == 'horizontal':
            self._layout = QHBoxLayout(self)
        self.label = QLabel(labeltext, self)
        
