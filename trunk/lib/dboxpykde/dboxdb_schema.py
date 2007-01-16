from useless.sqlgen.classes import Table
from useless.sqlgen.defaults import PkName
from useless.sqlgen.defaults import Bigname
from useless.sqlgen.defaults import Text
from useless.sqlgen.defaults import Num


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
        gmcol = PkName('name')
        gncol = Name('genre')
        fncol = Bigname('fullname')
        Table.__init__(self, 'games', [gmcol, gncol, fncol])
        
