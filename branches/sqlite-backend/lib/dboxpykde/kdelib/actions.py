from qt import QString
from kdecore import KShortcut
from kdeui import KGuiItem, KAction

from dboxpykde.common.actions import FilterAvailableGamesData
from dboxpykde.common.actions import FilterUnavailableGamesData
from dboxpykde.common.actions import FilterAllGamesData
from dboxpykde.common.actions import NewGenreData
from dboxpykde.common.actions import NewGameData
from dboxpykde.common.actions import LaunchDosboxData
from dboxpykde.common.actions import FlatViewData
from dboxpykde.common.actions import TreeViewData
from dboxpykde.common.actions import NameViewData
from dboxpykde.common.actions import TitleViewData
from dboxpykde.common.actions import PrepareAllGamesData
from dboxpykde.common.actions import CleanAllGamesData
from dboxpykde.common.actions import ArchiveAllGamesData
from dboxpykde.common.actions import LaunchDosboxPromptData
from dboxpykde.common.actions import LaunchMainDosboxPromptData

class BaseItem(KGuiItem):
    def __init__(self, itemdata):
        text = QString(itemdata['text'])
        icon = QString(itemdata['icon'])
        ttip = QString(itemdata['ttip'])
        whatsit = QString(itemdata['whatsit'])
        KGuiItem.__init__(self, text, icon, ttip, whatsit)
        
# this class will go into useless.kbase.actions later
class BaseAction(KAction):
    def __init__(self, itemdata, name, slot, parent):
        cut = KShortcut()
        item = BaseItem(itemdata)
        KAction.__init__(self, item, cut, slot, parent, name)

class FilterAvailableGames(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, FilterAvailableGamesData, 'FilterAvailableGames',
                            slot, parent)

class FilterUnavailableGames(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, FilterUnavailableGamesData, 'FilterUnavailableGames',
                            slot, parent)

class FilterAllGames(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, FilterAllGamesData, 'FilterAllGames',
                            slot, parent)

class NewGenre(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(NewGenreData)
        name = 'NewGenre'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class NewGame(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(NewGameData)
        name = 'NewGame'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)
        
class LaunchDosbox(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(LaunchDosboxData)
        name = 'LaunchDosbox'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class FlatView(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(FlatViewData)
        name = 'FlatViewItem'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class TreeView(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(TreeViewData)
        name = 'TreeView'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class NameView(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(NameViewData)
        name = 'NameView'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class TitleView(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(TitleViewData)
        name = 'TitleView'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class PrepareAllGames(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(PrepareAllGamesData)
        name = 'PrepareAllGames'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class CleanAllGames(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(CleanAllGamesData)
        name = 'CleanAllGames'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class ArchiveAllGames(KAction):
    def __init__(self, slot, parent):
        item = BaseItem(ArchiveAllGamesData)
        name = 'ArchiveAllGames'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)
        
class LaunchDosboxPrompt(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, LaunchDosboxPromptData, 'LaunchDosboxPrompt',
                            slot, parent)

class LaunchMainDosboxPrompt(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, LaunchMainDosboxPromptData, 'LaunchMainDosboxPrompt',
                            slot, parent)
        
############
# these actions need to go to common area eventually
############

class ManageDosboxProfiles(BaseAction):
    def __init__(self, slot, parent):
        itemdata = {}
        itemdata['text'] = 'Manage dosbox profiles'
        itemdata['icon'] = 'configure'
        itemdata['ttip'] = 'Manage dosbox configurations'
        itemdata['whatsit'] = itemdata['ttip']
        BaseAction.__init__(self, itemdata, 'ManageDosboxProfiles',
                            slot, parent)

class SetCurrentProfile(BaseAction):
    def __init__(self, slot, parent):
        itemdata = {}
        itemdata['text'] = 'Set current profile'
        itemdata['icon'] = 'configure'
        itemdata['ttip'] = 'Set current dosbox configuration profile'
        itemdata['whatsit'] = itemdata['ttip']
        BaseAction.__init__(self, itemdata, 'SetCurrentProfile',
                            slot, parent)
        
class ImportZipFile(BaseAction):
    def __init__(self, slot, parent):
        itemdata = {}
        itemdata['text'] = 'Import zip file'
        itemdata['icon'] = 'tar'
        itemdata['ttip'] = 'Import a zip file into the dosbox area as a new game'
        itemdata['whatsit'] = itemdata['ttip']
        BaseAction.__init__(self, itemdata, 'ImportZipFile',
                            slot, parent)
        
class ConfigureDosboxPyKDE(BaseAction):
    def __init__(self, slot, parent):
        itemdata = {}
        itemdata['text'] = 'Configure dosbox-pykde'
        itemdata['icon'] = 'configure'
        itemdata['ttip'] = 'Configure settings for dosbox-pykde'
        itemdata['whatsit'] = itemdata['ttip']
        BaseAction.__init__(self, itemdata, 'ConfigureDosboxPyKDE',
                            slot, parent)
    
class EditGameData(BaseAction):
    def __init__(self, slot, parent):
        itemdata = {}
        itemdata['text'] = "Edit this game's data"
        itemdata['icon'] = 'edit'
        itemdata['ttip'] = "Edit this game's data"
        itemdata['whatsit'] = itemdata['ttip']
        BaseAction.__init__(self, itemdata, 'EditGameData',
                            slot, parent)
    
    
