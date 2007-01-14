# basic definitions used by many modules
import os
from md5 import md5

class ExistsError(StandardError):
    pass

class FileError(StandardError):
    pass

class TooManyElementsError(StandardError):
    pass

class NotUsedAnymoreError(StandardError):
    pass

def makepaths(*paths):
    for path in paths:
        try:
            os.makedirs(path)
        except OSError, inst:
            # expect the error 17, 'File exists'
            if inst.args[0] == 17:
                pass
            else:
                raise inst
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
