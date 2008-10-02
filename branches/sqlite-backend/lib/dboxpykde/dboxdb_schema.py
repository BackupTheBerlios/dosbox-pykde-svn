import os
os.environ['_USELESS_DB_BACKEND'] = 'sqlite'

from useless.sqlgen.classes import Table, Column, ColumnType
from useless.sqlgen.defaults import PkNum
from useless.sqlgen.defaults import PkName
from useless.sqlgen.defaults import Bigname
from useless.sqlgen.defaults import Text
from useless.sqlgen.defaults import Num

DATE = ColumnType('date')
    
def Date(name):
    return Column(name, DATE)

class AutoId(Column):
    def __init__(self, colname):
        Column.__init__(self, colname, NUM)
        self.constraint.pk = True
        self.constraint.unique = True
        self.constraint.null = False
        self.constraint.auto = True

    def __write__(self):
        col = '%s' % self.name
        col += ' INTEGER AUTOINCREMENT'
        return col



class GenresTable(Table):
    def __init__(self):
        gcol = PkName('genre')
        ccol = Text('comment')
        Table.__init__(self, 'genres', [gcol, ccol])
        
class GenreParentsTable(Table):
    def __init__(self):
        gcol = PkName('genre')
        pcol = PkName('parent')
        Table.__init__(self, 'genre_parent', [gcol, pcol])

class GamesTable(Table):
    def __init__(self):
        gmcol = PkName('game')
        gncol = Name('genre')
        fncol = Bigname('fullname')
        dbpth = Bigname('dosboxpath')
        launch = Bigname('launchcmd')
        desc  = Text('desc')
        cols = [gmcol, gncol, fncol, dbpth, launch, desc]
        Table.__init__(self, 'games', cols)


class WeblinkTable(Table):
    def __init__(self):
        weblinkid = AutoId('weblinkid')
        site = Name('site')
        url = Bigname('url')
        cols = [weblinkid, site, url]
        Table.__init__(self, 'weblinks', cols)


class WeblinkGamesTable(Table):
    def __init__(self):
        game = Name('game')
        weblinkid = Num('weblinkid')
        Table.__init__(self, 'weblinks_games', [game, weblinkid])
        
    
