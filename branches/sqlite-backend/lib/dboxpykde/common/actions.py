class CommonItem(object):
    def __init__(self):
        pass


_show_avail = 'Show available games'
FilterAvailableGamesData = dict(text=_show_avail,
                                icon='filter',
                                ttip=_show_avail,
                                whatsit=_show_avail)

_show_unavail = 'Show unavailable games'
FilterUnavailableGamesData = dict(text=_show_unavail,
                                  icon='filter',
                                  ttip=_show_unavail,
                                  whatsit=_show_unavail)

_show_all = 'Show all games'
FilterAllGamesData = dict(text=_show_all,
                          icon='filter',
                          ttip=_show_all,
                          whatsit=_show_all)

_ttip = 'create a new genre (rpg, strategy, etc.)'
NewGenreData = dict(text='New genre',
                    icon='folder_new',
                    ttip=_ttip,
                    whatsit=_ttip)

_ttip = 'setup a new game'
NewGameData = dict(text='New game',
                   icon='filenew',
                   ttip=_ttip,
                   whatsit=_ttip)

_ttip = 'play this game in dosbox'
LaunchDosboxData = dict(text='Launch dosbox',
                        icon='launch',
                        ttip=_ttip,
                        whatsit=_ttip)

_ttip = 'view games in a flat list'
FlatViewData = dict(text='Flat game list',
                    icon='view_icon',
                    ttip=_ttip,
                    whatsit=_ttip)

_ttip = 'view games in a tree list'
TreeViewData = dict(text='Tree game list',
                    icon='view_tree',
                    ttip=_ttip,
                    whatsit=_ttip)

_ttip = 'view games by short name'
NameViewData = dict(text='Short game names',
                    icon='view_text',
                    ttip=_ttip,
                    whatsit=_ttip)

_ttip = 'view games by title'
TitleViewData = dict(text='Titled game names',
                     icon='view_detailed',
                     ttip=_ttip,
                     whatsit=_ttip)

_ttip = 'Prepare all the missing games'
PrepareAllGamesData = dict(text='Prepare all missing games',
                           icon='fill',
                           ttip=_ttip,
                           whatsit=_ttip)

_ttip = 'Backup and cleanup all available games'
CleanAllGamesData = dict(text='Cleanup all available games',
                         icon='save_all',
                         ttip=_ttip,
                         whatsit=_ttip)

_ttip = 'Archive/Prepare all available games'
ArchiveAllGamesData = dict(text=_ttip,
                           icon='stamp',
                           ttip=_ttip,
                           whatsit=_ttip)

text = 'Launch Dosbox Prompt'
_ttip = 'Launch Dosbox Prompt (with game as c:)'
LaunchDosboxPromptData = dict(text=text,
                          icon='terminal',
                          ttip=_ttip,
                          whatsit=_ttip)

text = 'Launch Main Dosbox Prompt'
_ttip = 'Launch Main Dosbox Prompt (with main dosbox area as c:)'
LaunchMainDosboxPromptData = dict(text=text,
                                  icon='systemtray',
                                  ttip=_ttip,
                                  whatsit=_ttip)

del _ttip
del text
