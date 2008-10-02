import os
os.environ['_USELESS_DB_BACKEND'] = 'sqlite'
from useless.db.lowlevel import LocalConnection
from useless.db.midlevel import StatementCursor


class Connection(LocalConnection):
    def __init__(self, dbname='test.db', autocommit=1, encoding='utf-8'):
        LocalConnection.__init__(self, dbname='test.db', autocommit=autocommit,
                                 encoding=encoding)

    def stmtcursor(self):
        return StatementCursor(self)

