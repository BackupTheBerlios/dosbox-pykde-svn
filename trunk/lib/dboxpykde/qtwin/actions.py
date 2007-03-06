from qt import QAction
from qt import SIGNAL, SLOT

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


# this class will go into useless.kbase.actions later
class BaseAction(QAction):
    def __init__(self, itemdata, name, slot, parent):
        QAction.__init__(self, parent, name)
        self.setMenuText(itemdata['text'])
        self.setToolTip(itemdata['ttip'])
        self.setWhatsThis(itemdata['whatsit'])
        self.connect(self, SIGNAL('activated()'), slot)
        
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

class NewGenre(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, NewGenreData, 'NewGenre',
                            slot, parent)
        
class NewGame(BaseAction):
    def __init__(self, slot, parent):
        item = NewGameData
        name = 'NewGame'
        BaseAction.__init__(self, item, name, slot, parent)
        
class LaunchDosbox(BaseAction):
    def __init__(self, slot, parent):
        item = LaunchDosboxData
        name = 'LaunchDosbox'
        BaseAction.__init__(self, item, name, slot, parent)

class FlatView(BaseAction):
    def __init__(self, slot, parent):
        item = FlatViewData
        name = 'FlatViewItem'
        BaseAction.__init__(self, item, name, slot, parent)

class TreeView(BaseAction):
    def __init__(self, slot, parent):
        item = TreeViewData
        name = 'TreeView'
        BaseAction.__init__(self, item, name, slot, parent)

class NameView(BaseAction):
    def __init__(self, slot, parent):
        item = NameViewData
        name = 'NameView'
        BaseAction.__init__(self, item, name, slot, parent)

class TitleView(BaseAction):
    def __init__(self, slot, parent):
        item = TitleViewData
        name = 'TitleView'
        BaseAction.__init__(self, item, name, slot, parent)

class PrepareAllGames(BaseAction):
    def __init__(self, slot, parent):
        item = PrepareAllGamesData
        name = 'PrepareAllGames'
        BaseAction.__init__(self, item, name, slot, parent)
        
    
class CleanAllGames(BaseAction):
    def __init__(self, slot, parent):
        item = CleanAllGamesData
        name = 'CleanAllGames'
        BaseAction.__init__(self, item, name, slot, parent)
        
class ArchiveAllGames(BaseAction):
    def __init__(self, slot, parent):
        item = ArchiveAllGamesData
        name = 'ArchiveAllGames'
        BaseAction.__init__(self, item, name, slot, parent)
        

# standard actions
class QuitAction(BaseAction):
    def __init__(self, slot, parent):
        name = 'QuitAction'
        item = dict(text='quit',
                    icon='quit',
                    ttip='quit',
                    whatsit='quit')
        BaseAction.__init__(self, item, name, slot, parent)
        
