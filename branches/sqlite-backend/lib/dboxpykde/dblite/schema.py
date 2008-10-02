from useless.sqlgen.classes import Table, Column, ColumnType
from useless.sqlgen.defaults import Text, Name, Bigname
from useless.sqlgen.defaults import PkNum, Num, NUM
from useless.sqlgen.defaults import DateTime
from useless.sqlgen.defaults import PkBigname, PkName


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


class GamesTable(Table):
    def __init__(self):
        gameid = PkName('gameid')
        # this wil be the fullname element in xml data
        title = Bigname('title')
        title.constraint.unique = True
        dosboxpath = Bigname('dosboxpath')
        launchcmd = Bigname('launchcmd')
        # this will be the description element in xml data
        desc = Text('desc')
        cols = [gameid, title, dosboxpath, launchcmd, desc]
        Table.__init__(self, 'games', cols)
        
class GameMd5sumsTable(Table):
    def __init__(self):
        gameid = PkName('gameid')
        filename = PkBigname('filename')
        md5sum  = Name('md5sum')
        cols = [gameid, filename, md5sum]
        Table.__init__(self, 'game_installed_files', cols)
        

class GameLinksTable(Table):
    def __init__(self):
        gameid = PkName('gameid')
        site = PkBigname('site')
        url = Text('url')
        Table.__init__(self, 'game_links', [gameid, site, url])
        

class AbandoniaGamesTable(Table):
    def __init__(self):
        gamenum = PkNum('gamenum')
        title = Bigname('title')
        desc = Text('desc')
        # we are going to store a dictionary in
        # smallinfo for a little while
        smallinfo = Text('smallinfo')
        cols = [gamenum, title, desc, smallinfo]
        Table.__init__(self, 'abandonia_games', cols)
        
class AbandoniaFilesTable(Table):
    def __init__(self):
        gamenum = PkNum('gamenum')
        filetype = Name('filetype')
        filename = Bigname('filename')
        cols = [gamenum, filetype, filename]
        Table.__init__(self, 'abandonia_files', cols)

# this table relates gameid's between
# games and abandonia_games
class AbandoniaRelationsTable(Table):
    def __init__(self):
        gameid = PkName('gameid')
        gamenum = PkNum('gamenum')
        Table.__init__(self, 'abandonia_rel', [gameid, gamenum])
    
    
def generate_schema(cursor):
    tables = [
        GamesTable,
        GameMd5sumsTable,
        GameLinksTable,
        AbandoniaGamesTable,
        AbandoniaFilesTable,
        AbandoniaRelationsTable,
        ]
    for tclass in tables:
        table = tclass()
        print "creating", table.name
        cursor.create_table(table)
        
if __name__ == '__main__':
    pass

