from qt import QString
from kdecore import KShortcut
from kdeui import KGuiItem, KAction

from common.actions import FilterAvailableGamesData
from common.actions import FilterUnavailableGamesData
from common.actions import FilterAllGamesData
from common.actions import NewGenreData
from common.actions import NewGameData
from common.actions import LaunchDosboxData
from common.actions import FlatViewData
from common.actions import TreeViewData
from common.actions import NameViewData
from common.actions import TitleViewData
from common.actions import PrepareAllGamesData
from common.actions import CleanAllGamesData
from common.actions import ArchiveAllGamesData


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
        
    
