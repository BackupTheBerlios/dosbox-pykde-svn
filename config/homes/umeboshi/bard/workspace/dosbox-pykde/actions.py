from qt import QString
from kdecore import KShortcut
from kdeui import KGuiItem, KAction

class NewGenreItem(KGuiItem):
    def __init__(self):
        text = QString('New genre')
        icon = QString('folder_new')
        ttip = QString('create a new genre (rpg, strategy, etc.)')
        wtf = QString('create a new genre (rpg, strategy, etc.)')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class NewGenre(KAction):
    def __init__(self, slot, parent):
        item = NewGenreItem()
        name = 'NewGenre'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class NewGameItem(KGuiItem):
    def __init__(self):
        text = QString('New game')
        icon = QString('filenew')
        ttip = QString('setup a new game')
        wtf = QString('setup a new game')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class NewGame(KAction):
    def __init__(self, slot, parent):
        item = NewGameItem()
        name = 'NewGame'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)
        
