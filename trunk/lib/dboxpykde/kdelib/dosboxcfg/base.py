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
from dboxpykde.kdelib.config import BaseConfigWidget
# these imports to replace removed classes
from dboxpykde.kdelib.config import BaseConfigOptionWidget
from dboxpykde.kdelib.config import ConfigComboBoxWidget
from dboxpykde.kdelib.config import ConfigLineEditWidget
from dboxpykde.kdelib.config import ConfigSpinWidget
from dboxpykde.kdelib.config import ConfigKURLSelectWidget
from dboxpykde.kdelib.config import VerticalGroupBox
# the above modules should be reimported correctly in other intrapackage modules

class BaseDosboxConfigWidget(BaseConfigWidget):
    def __init__(self, parent, name='BaseDosboxConfigWidget'):
        BaseConfigWidget.__init__(self, parent, name=name)

