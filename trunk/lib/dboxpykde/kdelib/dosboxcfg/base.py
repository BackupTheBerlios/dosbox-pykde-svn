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

class BaseDosboxConfigWidget(QWidget):
    def __init__(self, parent, name='BaseDosboxConfigWidget'):
        QWidget.__init__(self, parent, name)
        self.tooltips = QToolTip

class BaseConfigOptionWidget(QWidget):
    def __init__(self, parent, labeltext, optclass,
                 name='BaseConfigOptionWidget'):
        QWidget.__init__(self, parent, name)
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

class ConfigComboBoxWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, defaults,
                 name='ConfigComboBoxWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KComboBox, name=name)
        self.mainwidget.insertStrList(defaults)

class ConfigLineEditWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext,
                 name='ConfigLineEditWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KLineEdit, name=name)
        

class ConfigSpinWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, min=0, max=100, suffix='',
                 name='BaseConfigOptionSpinWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext,
                                        KIntSpinBox, name=name)
        self.mainwidget.setMinValue(min)
        self.mainwidget.setMaxValue(max)
        if suffix:
            self.mainwidget.setSuffix(suffix)

class ConfigKURLSelectWidget(BaseConfigOptionWidget):
    def __init__(self, parent, labeltext, filetype='file',
                 name='ConfigKURLSelectWidget'):
        BaseConfigOptionWidget.__init__(self, parent, labeltext, KURLRequester,
                                        name=name)
        if filetype in ['dir', 'directory']:
            self.mainwidget.setMode(KFile.Directory)
            
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
        
