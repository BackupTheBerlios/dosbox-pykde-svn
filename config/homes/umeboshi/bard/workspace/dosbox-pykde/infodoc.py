import os

from forgetHTML import Inline
from forgetHTML import SimpleDocument
from forgetHTML import Anchor, Table
from forgetHTML import TableRow, TableCell
from forgetHTML import TableHeader, Header
from forgetHTML import Image

from base import make_url

class Bold(Inline):
    tag = 'b'
    
class BaseDocument(SimpleDocument):
    def __init__(self, app, title='BaseDocument', **args):
        SimpleDocument.__init__(self, title=title)
        self.app = app
        self.filehandler = app.game_fileshandler
        self.datahandler = self.filehandler.datahandler
        self.maintable = Table(class_='BaseDocumentTable', border=1, cellspacing=0,
                               width='100%')
        self.body.set(self.maintable)

    def set_info(self, name):
        gamedata = self.datahandler.get_game_data(name)
        fullname = TableHeader(gamedata['fullname'], colspan=0, align='center')
        fullname_row = TableRow(fullname)
        self.maintable.set(fullname_row)
        desc_lbl = Bold('description')
        desc_lbl_cell = TableCell(desc_lbl, colspan=0, align='center', bgcolor='DarkSeaGreen4')
        desc_lbl_row = TableRow(desc_lbl_cell)
        self.maintable.append(desc_lbl_row)
        desc = TableCell(gamedata['description'], colspan=0)
        desc_row = TableRow(desc)
        self.maintable.append(desc_row)
        # setup title screenshot section
        row = TableRow()
        cell = TableCell(colspan=0)
        row.set(cell)
        cell.append(self.make_title_screenshot_table(gamedata))
        self.maintable.append(row)
        
        # setup dosbox data section
        dosbox_data_row = TableRow()
        dosbox_data_cell = TableCell(colspan=0)
        dosbox_data_row.set(dosbox_data_cell)
        dosbox_data_cell.append(self.make_dosbox_data_table(gamedata))
        self.maintable.append(dosbox_data_row)

        # setup status and action section
        action_row = TableRow()
        action_cell = TableCell(colspan=0)
        action_row.append(action_cell)
        self.maintable.append(action_row)
        action_cell.set(self.make_action_table(name))


    def make_title_screenshot_table(self, gamedata):
        name = gamedata['name']
        screenshot = self.app.game_datahandler.get_title_screenshot_filename(name)
        tableatts = dict(class_='titlescreenshottable', width='100%')
        ss_table = Table(**tableatts)
        lbl = TableHeader('Title Screenshot', colspan=0, align='center')
        row = TableRow(lbl)
        ss_table.set(row)
        ss_row = TableRow()
        ss_cell = TableCell(align='center')
        ss_table.append(ss_row)
        ss_row.append(ss_cell)
        status = os.path.exists(screenshot)
        if not status:
            ss_cell.set('Screenshot unavailable')
        else:
            img = Image(src=screenshot, width='320', height='240')
            ss_cell.set(img)
        ss_update_row = TableRow()
        ss_update_cell = TableCell()
        ss_update_row.append(ss_update_cell)
        if status:
            anchor = Anchor('Update Screenshot', href=make_url('set_title_screenshot', name))
        else:
            anchor = Anchor('Select Screenshot', href=make_url('set_title_screenshot', name))
        ss_update_cell.set(anchor)
        ss_table.append(ss_update_row)
        return ss_table
    
    def make_dosbox_data_table(self, gamedata):
        tableatts = dict(class_='dosboxdatatable', width='100%', border=0,
                         cellspacing=0)
        dosbox_data_table = Table(**tableatts)
        # setup header
        dosbox_data_lbl = TableHeader('Dosbox data', colspan=0, align='center')
        dosbox_data_row = TableRow(dosbox_data_lbl)
        dosbox_data_table.set(dosbox_data_row)
        # setup dosboxpath
        dosboxpath_lbl = TableCell('dosbox path:')
        dosboxpath = TableCell(gamedata['dosboxpath'])
        dosboxpath_row = TableRow()
        dosboxpath_row.append(dosboxpath_lbl)
        dosboxpath_row.append(dosboxpath)
        dosbox_data_table.append(dosboxpath_row)
        # setup launchcmd
        launchcmd_lbl = TableCell('launch command:')
        launchcmd = TableCell(gamedata['launchcmd'])
        launchcmd_row = TableRow()
        launchcmd_row.append(launchcmd_lbl)
        launchcmd_row.append(launchcmd)
        dosbox_data_table.append(launchcmd_row)
        return dosbox_data_table
    
    def make_action_table(self, name):
        atable = Table(class_='ActionTable')
        available_row = TableRow()
        status = self.filehandler.get_game_status(name)
        if status:
            available_cell = TableCell('available', bgcolor='DarkSeaGreen4')
        else:
            available_cell = TableCell('unavailable', bgcolor='Red')
        if not status:
            filemanage_anchor = Anchor('prepare game', href=make_url('prepare', name))
        else:
            filemanage_anchor = Anchor('clean up game area', href=make_url('cleanup', name))
        filemanage_cell = TableCell(filemanage_anchor)

        available_row.append(available_cell)
        available_row.append(filemanage_cell)
        atable.append(available_row)
        #filemanage_row = TableRow()
        #filemanage_row.append(filemanage_cell)
        #atable.append(filemanage_row)
        edit_row = TableRow()
        edit_anchor = Anchor("edit this game's data", href=make_url('edit', name))
        edit_row.append(TableCell(edit_anchor))
        atable.append(edit_row)
        return atable
