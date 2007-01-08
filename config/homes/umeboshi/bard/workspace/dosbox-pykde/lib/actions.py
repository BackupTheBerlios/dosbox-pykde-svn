from qt import QString
from kdecore import KShortcut
from kdeui import KGuiItem, KAction

# this class taken from useless.kbase.actions
# This is a quick way to make KGuiItem's
class BaseItem(KGuiItem):
    def __init__(self, text, icon, ttip, whatsit):
        KGuiItem.__init__(self, QString(text), QString(icon), QString(ttip),
                          QString(whatsit))
        
# this class will go into useless.kbase.actions later
class BaseAction(KAction):
    def __init__(self, item, name, slot, parent):
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class FilterAvailableGamesItem(BaseItem):
    def __init__(self):
        txt = 'Show available games'
        BaseItem.__init__(self, txt, 'filter', txt, txt)

class FilterAvailableGames(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, FilterAvailableGamesItem(), 'FilterAvailableGames',
                            slot, parent)



class FilterUnavailableGamesItem(BaseItem):
    def __init__(self):
        txt = 'Show unavailable games'
        BaseItem.__init__(self, txt, 'filter', txt, txt)

class FilterUnavailableGames(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, FilterUnavailableGamesItem(), 'FilterUnavailableGames',
                            slot, parent)



class FilterAllGamesItem(BaseItem):
    def __init__(self):
        txt = 'Show all games'
        BaseItem.__init__(self, txt, 'filter', txt, txt)

class FilterAllGames(BaseAction):
    def __init__(self, slot, parent):
        BaseAction.__init__(self, FilterAllGamesItem(), 'FilterAllGames',
                            slot, parent)



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
        
class LaunchDosboxItem(KGuiItem):
    def __init__(self):
        text = QString('Launch dosbox')
        icon = QString('launch')
        ttip = QString('play this game in dosbox')
        wtf = QString('play this game in dosbox')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class LaunchDosbox(KAction):
    def __init__(self, slot, parent):
        item = LaunchDosboxItem()
        name = 'LaunchDosbox'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class FlatViewItem(KGuiItem):
    def __init__(self):
        text = QString('Flat game list')
        icon = QString('view_icon')
        ttip = QString('view games in a flat list')
        wtf = QString('view games in a flat list')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class FlatView(KAction):
    def __init__(self, slot, parent):
        item = FlatViewItem()
        name = 'FlatViewItem'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class TreeViewItem(KGuiItem):
    def __init__(self):
        text = QString('Tree game list')
        icon = QString('view_tree')
        ttip = QString('view games in a tree list')
        wtf = QString('view games in a tree list')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class TreeView(KAction):
    def __init__(self, slot, parent):
        item = TreeViewItem()
        name = 'TreeView'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class NameViewItem(KGuiItem):
    def __init__(self):
        text = QString('Short game names')
        icon = QString('view_text')
        ttip = QString('view games by short name')
        wtf = QString('view games by short name')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class NameView(KAction):
    def __init__(self, slot, parent):
        item = NameViewItem()
        name = 'NameView'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class TitleViewItem(KGuiItem):
    def __init__(self):
        text = QString('Titled game names')
        icon = QString('view_detailed')
        ttip = QString('view games by title')
        wtf = QString('view games by title')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class TitleView(KAction):
    def __init__(self, slot, parent):
        item = TitleViewItem()
        name = 'TitleView'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)

class PrepareAllGamesItem(KGuiItem):
    def __init__(self):
        text = QString('Prepare all missing games')
        icon = QString('fill')
        ttip = QString('Prepare all the missing games')
        wtf = QString('Prepare all the missing games')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class PrepareAllGames(KAction):
    def __init__(self, slot, parent):
        item = PrepareAllGamesItem()
        name = 'PrepareAllGames'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)
        
    
class CleanAllGamesItem(KGuiItem):
    def __init__(self):
        text = QString('Cleanup all available games')
        icon = QString('save_all')
        ttip = QString('Backup and cleanup all available games')
        wtf = QString('Backup and cleanup all available games')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class CleanAllGames(KAction):
    def __init__(self, slot, parent):
        item = CleanAllGamesItem()
        name = 'CleanAllGames'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)
        
    
class ArchiveAllGamesItem(KGuiItem):
    def __init__(self):
        text = QString('Archive/Prepare all available games')
        icon = QString('stamp')
        ttip = QString('Archive/Prepare all available games')
        wtf = QString('Archive/Prepare all available games')
        KGuiItem.__init__(self, text, icon, ttip, wtf)

class ArchiveAllGames(KAction):
    def __init__(self, slot, parent):
        item = ArchiveAllGamesItem()
        name = 'ArchiveAllGames'
        cut = KShortcut()
        KAction.__init__(self, item, cut, slot, parent, name)
        
    
