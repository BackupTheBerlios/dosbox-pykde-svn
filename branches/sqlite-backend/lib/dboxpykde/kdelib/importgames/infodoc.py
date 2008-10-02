import os
import time

from dboxpykde.contrib.forgetHTML import Inline
from dboxpykde.contrib.forgetHTML import SimpleDocument
from dboxpykde.contrib.forgetHTML import Anchor, Table
from dboxpykde.contrib.forgetHTML import TableRow, TableCell
from dboxpykde.contrib.forgetHTML import TableHeader, Header
from dboxpykde.contrib.forgetHTML import Image
from dboxpykde.contrib.forgetHTML import Paragraph, Break
from dboxpykde.contrib.forgetHTML import Span, Ruler, Pre
from dboxpykde.contrib.forgetHTML import Text
from dboxpykde.base import make_url

from dboxpykde.infodoc import Bold, BaseDocument

class AbandoniaInfoDocument(BaseDocument):
    def set_info(self, handler):
        self.handler = handler
        parser = handler.parser
        base_url = handler._base_url
        title = TableHeader(parser.title)
        row = TableRow(title)
        self.maintable.set(row)
        self._makeinfo(base_url, parser)
        #cell = TableCell(Pre(text, style="font-size: xx-small"))
        #self.maintable.append(TableRow(cell))

    def _make_smallinfo(self, info):
        infotable = Table()
        infotable.append(TableRow(TableHeader('Small Information', colspan=2)))
        for k, v in info.items():
            row = TableRow()
            cell = TableCell('%s:' % k.capitalize())
            row.set(cell)
            cell = TableCell(v)
            row.append(cell)
            infotable.append(row)
        self.maintable.append(TableRow(TableCell(infotable)))

    def _makeinfo(self, base, parser):
        print parser.gameid, type(parser.gameid), 'in _makeinfo'
        text = 'GameID: %d' % parser.gameid
        available = self.handler.is_game_downloaded(parser.gameid)
        bgcolor = {True:'DarkSeaGreen', False:'IndianRed'}[available]
        if parser.download_link is None:
            bgcolor = 'Goldenrod'
        self.maintable.append(TableRow(TableCell(text, bgcolor=bgcolor)))
        if parser.smallinfo:
            self._make_smallinfo(parser.smallinfo)
        text = Text(parser.desc)
        text.set_rawtext(True)
        span = Span(text, style='font-size: xx-small')
        cell = TableCell(span)
        row = TableRow(cell)
        self.maintable.append(row)
        if parser.download_link is not None:
            if self.handler.is_game_downloaded(parser.gameid):
                dp = Bold('Available')
            else:
                dlurl = base + parser.download_link
                dp = Anchor('download page', href='download')
            self.maintable.append(TableRow(TableCell(dp)))
        else:
            self.maintable.append(TableRow(TableCell('No Download Available')))
        if parser.files:
            self.maintable.append(TableRow(TableCell(Bold('Files'))))
            for f in parser.files:
                url = '%s%s' % (base, f)
                filename = f.basename()
                if self.handler.is_extra_downloaded(filename):
                    extra = Bold(filename)
                else:
                    extra = Anchor(filename, href='extras/%s' % url)
                #anchor = Anchor(os.path.basename(f), href=url)
                self.maintable.append(TableRow(TableCell(extra)))
        
