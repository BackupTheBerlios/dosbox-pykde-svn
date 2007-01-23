from qt import SIGNAL
from qt import QSplitter
from kdeui import KListView, KListViewItem
from kdeui import KStdAction
from kdeui import KPopupMenu
from kdeui import KMessageBox

from dboxpykde.kdelib.base import BaseDialogWindow
from dboxpykde.kdelib.base import BaseMainWindow
from dboxpykde.kdelib.base import BaseEntryDialog
from dboxpykde.kdelib.base import get_application_pointer
from dboxpykde.dosbox import Dosbox

from cfgmain import DosboxConfigTabWidget

class NameProfileDialog(BaseEntryDialog):
    def __init__(self, parent, name='NameProfileDialog'):
        BaseEntryDialog.__init__(self, parent, name=name)
        caption = 'Name Profile'
        msg = 'Please name the profile.'
        self.setCaption(caption)
        self.label.setText(msg)

class ProfileSelectorDialog(BaseDialogWindow):
    def __init__(self, parent, name='ProfileSelectorDialog'):
        BaseDialogWindow.__init__(self, parent, name=name)
        self.dbox = Dosbox(self.app)
        profiles = self.dbox.get_profile_list()
        self.listView = KListView(self)
        self.listView.addColumn('profile')
        self.setMainWidget(self.listView)
        for profile in profiles:
            item = KListViewItem(self.listView, profile)
            item.profile = profile

    def get_selected_profile(self):
        item = self.listView.currentItem()
        return item.profile
    
class ProfileManagerWidget(QSplitter):
    def __init__(self, parent, name='ProfileManagerWidget'):
        QSplitter.__init__(self, parent, name)
        self.app = get_application_pointer()
        #self.listView = KListView(self)
        self.cfgView = DosboxConfigTabWidget(self)
        self.dbox = Dosbox(self.app)

        #self.initlistView()
        cfg = self.dbox.get_default_config()
        self.cfgView.set_config(cfg)
        #self.connect(self.listView,
        #             SIGNAL('selectionChanged()'), self.selectionChanged)
        
    def initlistView(self):
        self.listView.addColumn('profile')
        self.refreshListView()
        
    def refreshListView(self):
        self.listView.clear()
        for profile in self.dbox.get_profile_list():
            item = KListViewItem(self.listView, profile)
            item.profile = profile

    def save_profile(self, profile):
        configobj = self.cfgView.get_config()
        self.dbox.save_profile(profile, configobj)

    def selectionChanged(self):
        item = self.listView.currentItem()
        profile = item.profile
        self.select_profile(profile)

    def select_profile(self, profile):
        cfg = self.dbox.load_profile(profile)
        self.cfgView.set_config(cfg)
        
class ManageDosboxProfilesWindow(BaseMainWindow):
    def __init__(self, parent, name='ManageDosboxProfilesWindow'):
        BaseMainWindow.__init__(self, parent, name)
        self.mainView = ProfileManagerWidget(self)
        self.initActions()
        self.initMenus()
        self.initToolbar()
        self.setCentralWidget(self.mainView)
        self.setCaption('Manage Dosbox Profiles')
        self.statusbar = self.statusBar()
        self.statusbar.message('No Profile loaded')
        self.dbox = Dosbox(self.app)
        # pointers
        self.current_profile = None
        self._name_profile_dialog = None
        self._save_profile_dialog = None
        self._open_profile_dialog = None

        current_profile = self.app.dosbox.current_profile
        if current_profile is not None:
            self.set_current_profile(current_profile)
        
    def initActions(self):
        collection = self.actionCollection()
        self.quitAction = KStdAction.quit(self.close, collection)
        self.openNewAction = KStdAction.openNew(self.slotOpenNew, collection)
        self.openAction = KStdAction.open(self.slotOpen, collection)
        self.saveAction = KStdAction.save(self.slotSave, collection)
        self.saveAsAction = KStdAction.saveAs(self.slotSaveAs, collection)
        
    def initMenus(self):
        mainmenu = KPopupMenu(self)
        for action in [self.openNewAction, self.openAction, self.saveAction,
                       self.saveAsAction]:
            action.plug(mainmenu)
        self.quitAction.plug(mainmenu)
        menubar = self.menuBar()
        menubar.insertItem('&Main', mainmenu)
        
    def initToolbar(self):
        toolbar = self.toolBar()
        for action in [self.openNewAction, self.openAction, self.saveAction,
                       self.saveAsAction]:
            action.plug(toolbar)
        self.quitAction.plug(toolbar)

    def slotSave(self):
        profile = self.current_profile
        msg = 'Save profile %s?' % profile
        ans = KMessageBox.questionYesNo(self, msg, 'Save Profile')
        if ans == KMessageBox.Yes:
            self.mainView.save_profile(profile)
        elif ans == KMessageBox.No:
            print KMessageBox.information(self,
                                          'Declined to save profile %s' % profile)
        else:
            print ans
        

    def slotSaveAs(self):
        dlg = NameProfileDialog(self)
        self.connect(dlg, SIGNAL('okClicked()'), self._saveas_profile_name_selected)
        dlg.show()
        self._name_profile_dialog = dlg
        print 'slotSaveAs called'
        
    def slotOpenNew(self):
        self.slotSaveAs()

    def slotOpen(self):
        print 'slotOpen called'
        dlg = ProfileSelectorDialog(self)
        self.connect(dlg, SIGNAL('okClicked()'), self._open_profile_name_selected)
        dlg.show()
        self._open_profile_dialog = dlg

    def set_current_profile(self, profile):
        self.dbox.set_current_profile(profile)
        self.current_profile = self.dbox.current_profile
        self.mainView.select_profile(self.current_profile)
        self.statusbar.message('Profile %s loaded.' % self.current_profile)
        
        
    def _saveas_profile_name_selected(self):
        dlg = self._name_profile_dialog
        if dlg is not None:
            profile = str(dlg.entry.text())
            print 'new profile is', profile
            self.mainView.save_profile(profile)
            self._name_profile_dialog = None
            self.set_current_profile(profile)
            
    def _save_profile_ok(self):
        dlg = self._save_profile_dialog
        if dlg is not None:
            profile = dlg.profile
            self.mainView.save_profile(profile)
            self._save_profile_dialog = None
            self.set_current_profile(profile)
            
    def _open_profile_name_selected(self):
        dlg = self._open_profile_dialog
        if dlg is not None:
            profile = dlg.get_selected_profile()
            self.set_current_profile(profile)
            
            
            
            
class ProfileDialogWindow(BaseDialogWindow):
    def __init__(self, parent, name='ProfileDialogWindow'):
        BaseDialogWindow.__init__(self, parent, name=name)
        self.mainView = ProfileManagerWidget(self)
        
        self.setMainWidget(self.mainView)

class Profile:
    pass
