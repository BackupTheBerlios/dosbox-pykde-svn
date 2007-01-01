from forgetHTML import SimpleDocument
from forgetHTML import Anchor, Table
from forgetHTML import TableRow, TableCell
from forgetHTML import TableHeader, Header

# this is what separates parts of the url
url_delimeter = '||'

# handy function to split urls created in the text browser
def split_url(url):
    return str(url).split(url_delimeter)

def make_url(*args):
    return url_delimeter.join(args)

class BaseDocument(SimpleDocument):
    def __init__(self, app, title='BaseDocument', **args):
        SimpleDocument.__init__(self, title=title)
        self.app = app
        self.maintable = Table(class_='BaseDocumentTable')
        self.body.set(self.maintable)

    def set_info(self, name):
        pass
