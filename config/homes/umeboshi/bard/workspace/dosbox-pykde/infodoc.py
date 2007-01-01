from forgetHTML import SimpleDocument
from forgetHTML import Anchor, Table
from forgetHTML import TableRow, TableCell
from forgetHTML import TableHeader, Header

from base import make_url

class BaseDocument(SimpleDocument):
    def __init__(self, app, title='BaseDocument', **args):
        SimpleDocument.__init__(self, title=title)
        self.app = app
        self.filehandler = app.game_fileshandler
        self.datahandler = self.filehandler.datahandler
        self.maintable = Table(class_='BaseDocumentTable')
        self.body.set(self.maintable)

    def set_info(self, name):
        gamedata = self.datahandler.get_game_data(name)
        fullname = TableHeader(gamedata['fullname'])
        fullname_row = TableRow(fullname)
        self.maintable.set(fullname_row)
        desc = TableCell(gamedata['description'])
        desc_row = TableRow(desc)
        self.maintable.append(desc_row)
        dosboxpath = TableCell(gamedata['dosboxpath'])
        dosboxpath_row = TableRow(dosboxpath)
        self.maintable.append(dosboxpath_row)
        action_row = TableRow()
        action_cell = TableCell()
        action_row.append(action_cell)
        self.maintable.append(action_cell)
        action_cell.set(self.make_action_table(name))
        
    def make_action_table(self, name):
        atable = Table(class_='ActionTable')
        available_row = TableRow()
        status = self.filehandler.get_game_status(name)
        if status:
            available_cell = TableCell('available')
        else:
            available_cell = TableCell('unavailable')
        available_row.append(available_cell)
        atable.append(available_row)
        filemanage_row = TableRow()
        if not status:
            filemanage_anchor = Anchor('prepare game', href=make_url('prepare', name))
        else:
            filemanage_anchor = Anchor('clean up game area', href=make_url('cleanup', name))
        filemanage_cell = TableCell(filemanage_anchor)
        filemanage_row.append(filemanage_cell)
        atable.append(filemanage_row)
        return atable
