from qt import QWidget
from qt import QLabel
from qt import QGridLayout

from kdeui import KWizard

from dboxpykde.config import generate_default_config_for_wizard

from dboxpykde.kdelib.config import BaseConfigWidget
from dboxpykde.kdelib.config import ConfigKURLSelectWidget
from dboxpykde.kdelib.base import get_application_pointer

intro = """
Welcome,
This wizard will help you configure some important options for
dosbox-pykde.
"""
archive_paths_lbl = """<qt>
Configure the paths for the installed and extras archives.
The default is:<br>
<b>~/archives/dosbox-installed</b> for the installed path and
<b>~/archives/dosbox-extras</b> for the extras path
</qt>
"""
dosbox_path_lbl = """
Configure the path to the main dosbox area.  This is where
all of the dosbox games will be stored and run from.
"""

class IntroPage(BaseConfigWidget):
    def __init__(self, parent, name='IntroPage'):
        BaseConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 1
        margin = 5
        space = 7
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'IntroPageLayout')
        lbl = QLabel(intro, self)
        self.grid.addWidget(lbl, 0, 0)

class ArchivePathsPage(BaseConfigWidget):
    def __init__(self, parent, name='ArchivePathsPage'):
        BaseConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 1
        margin = 5
        space = 7
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'ArchivePathsPageLayout')
        lbl = QLabel(archive_paths_lbl, self)
        lbl.setFrameStyle(lbl.Panel + lbl.Sunken)
        #lbl.setFrameStyle(lbl.Raised)
        self.grid.addWidget(lbl, 0, 0)
        self.installed_entry = ConfigKURLSelectWidget(self, 'Path to "install" archives',
                                                      filetype='dir')
        self.tooltips.add(self.installed_entry,
                          "This is the path to the archives of fresh installs")
        self.grid.addWidget(self.installed_entry, 1, 0)
        self.extras_entry = ConfigKURLSelectWidget(self, 'Path to "extras" archives',
                                                   filetype='dir')
        self.grid.addWidget(self.extras_entry, 2, 0)

    def set_config(self, configobj):
        self.mainconfig = configobj
        # some assignments to help with typing
        fm = 'filemanagement'
        cfg = self.mainconfig
        installed = cfg.get(fm, 'installed_archives_path')
        self.installed_entry.set_config_option(installed)
        extras = cfg.get(fm, 'extras_archives_path')
        self.extras_entry.set_config_option(extras)

    def get_config(self):
        fm = 'filemanagement'
        cfg = self.localconfig
        installed = self.installed_entry.get_config_option()
        cfg.set(fm, 'installed_archives_path', installed)
        extras = self.extras_entry.get_config_option()
        cfg.set(fm, 'extras_archives_path', extras)
        return cfg

class DosboxPathPage(BaseConfigWidget):
    def __init__(self, parent, name='DosboxPathPage'):
        BaseConfigWidget.__init__(self, parent, name=name)
        numrows = 2
        numcols = 1
        margin = 5
        space = 7
        self.grid = QGridLayout(self, numrows, numcols,
                                margin, space, 'DosboxPathPageLayout')
        lbl = QLabel(dosbox_path_lbl, self)
        lbl.setFrameStyle(lbl.Panel + lbl.Sunken)
        #lbl.setFrameStyle(lbl.Raised)
        self.grid.addWidget(lbl, 0, 0)
        self.dosbox_path_entry = ConfigKURLSelectWidget(self, 'Path to main dosbox area',
                                                        filetype='dir')
        self.grid.addWidget(self.dosbox_path_entry, 1, 0)

# make a wizard to help create default configuration
class DboxPykdeWizard(KWizard):
    def __init__(self, parent, name='DboxPykdeWizard'):
        # the last argument is modal
        KWizard.__init__(self, parent, name, True)
        self.app = get_application_pointer()
        print 'hello', self.app
        self.cfg = generate_default_config_for_wizard()
        print self.cfg.sections()
        self.pageone = IntroPage(self)
        self.addPage(self.pageone, 'Introduction')
        self.pagetwo = ArchivePathsPage(self)
        self.addPage(self.pagetwo, 'Archive Paths')
        self.pagethree = DosboxPathPage(self)
        self.addPage(self.pagethree, 'Dosbox Path')
        self.set_config()
        
    def set_config(self):
        self.pagetwo.set_config(self.cfg)
        
