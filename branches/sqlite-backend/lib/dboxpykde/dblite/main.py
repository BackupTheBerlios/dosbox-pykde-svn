import os

from useless.db.lowlevel import LocalConnection
from useless.db.midlevel import StatementCursor
from useless.sqlgen.clause import Eq

from dboxpykde.base import ExistsError

#from schema import generate_schema


class TooManyRows(LookupError):
    pass

class Connection(LocalConnection):
    def __init__(self, dbname='test.db', autocommit=1, encoding='utf-8'):
        LocalConnection.__init__(self, dbname=dbname, autocommit=autocommit,
                                 encoding=encoding)
        
    def stmtcursor(self):
        return StatementCursor(self)


# this class tries to mimic the GameDataHandler
# and should work as a compatibility layer
# for upgrading from an older installation
class GameDataBaseCompat(object):
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.stmtcursor()
        if not self.cursor.tables():
            print 'generating database schema'
            import schema
            schema.generate_schema(self.cursor)
            del schema
            
    def _id_clause(self, gameid):
        return Eq('gameid', gameid)
    
    def get_game_names(self):
        rows = self.cursor.select(table='games')
        return [row.gameid for row in rows]

    def get_installed_files(self, gameid):
        clause = Eq('gameid', gameid)
        rows = self.cursor.select(table='game_installed_files', clause=clause)
        return [(row.filename, row.md5sum) for row in rows]

    def get_game_data(self, gameid):
        rows = self.cursor.select(table='games', clause=self._id_clause(gameid))
        if len(rows) == 1:
            row = rows[0]
            gamedata = dict(name=gameid, fullname=row.title, description=row.desc,
                            launchcmd=row.launchcmd, dosboxpath=row.dosboxpath,
                            weblinks=dict())
            rows = self.cursor.select(table='game_links', clause=self._id_clause(gameid))
            for row in rows:
                gamedata['weblinks'][row.site] = row.url
            return gamedata
        else:
            raise LookupError, 'game %s not found' % gameid

    def add_new_game(self, gamedata, installed_files):
        gameid = gamedata['name']
        title = gamedata['fullname']
        desc = gamedata['description']
        data = dict(gameid=gameid, title=title, desc=desc)
        for key in ['dosboxpath', 'launchcmd']:
            data[key] = gamedata[key]
        self.cursor.insert(table='games', data=data)
        if gamedata.has_key('weblinks'):
            weblinks = gamedata['weblinks']
            data = dict(gameid=gameid)
            for site in weblinks:
                data['site'] = site
                data['url'] = weblinks[site]
                self.cursor.insert('game_links', data=data)
        data = dict(gameid=gameid)
        for filename, md5sum in installed_files:
            data.update(dict(filename=filename, md5sum=md5sum))
            self.cursor.insert(table='game_installed_files', data=data)
            
    def update_game_data(self, gamedata):
        gameid = gamedata['name']
        clause = self._id_clause(gameid)
        data = dict(title=gamedata['fullname'],
                    desc=gamedata['description'],
                    dosboxpath=gamedata['dosboxpath'],
                    launchcmd=gamedata['launchcmd'])
        self.cursor.update(table='games', data=data, clause=clause)
        if gamedata.has_key('weblinks'):
            if gamedata['weblinks']:
                print "we don't handle updating weblinks yet"
                print "it shouldn't be needed in the compat class anyway"

    # this is new, because we don't pass the app object to this class
    def set_screenshots_path(self, directory):
        self.screenshots_path = directory

    def get_title_screenshot_filename(self, name):
        return self.screenshots_path / name / 'title.png'

    def make_title_screenshot(self, name, picpath):
        title_pic_filename = self.get_title_screenshot_filename(name)
        dirname = title_pic_filename.dirname()
        if not dirname.exists():
            dirname.mkdir()
        picdata = file(picpath).read()
        title_pic_file = file(title_pic_filename, 'w')
        title_pic_file.write(picdata)
        title_pic_file.close()
        
                

        
        
    
if __name__ == '__main__':
    import os
    
    dbfile = 'test.db'
    if os.environ.has_key('DBFILE'):
        dbfile = os.environ['DBFILE']
    conn = Connection(dbname=dbfile,
                      autocommit=True, encoding='ascii')
    cursor = conn.stmtcursor()
    
