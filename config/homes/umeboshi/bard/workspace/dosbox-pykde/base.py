# basic definitions used by many modules
import os
from md5 import md5

class ExistsError(StandardError):
    pass

class FileError(StandardError):
    pass

class TooManyElementsError(StandardError):
    pass

# this function taken from useless.base.util
def makepaths(*paths):
    for path in paths:
        if not os.path.isdir(path):
            os.makedirs(path)

# default block size
BLOCK_SIZE = 1024

# this function taken from useless.base.util
def md5sum(afile):
    """returns the standard md5sum hexdigest
    for a file object"""
    m = md5()
    block = afile.read(BLOCK_SIZE)
    while block:
        m.update(block)
        block = afile.read(BLOCK_SIZE)
    return m.hexdigest()


# this is what separates parts of the url
url_delimeter = '||'

# handy function to split urls created in the text browser
def split_url(url):
    return str(url).split(url_delimeter)

def make_url(*args):
    return url_delimeter.join(args)

opendlg_errormsg = 'There is already a dialog box open.  Close it or restart the program'
