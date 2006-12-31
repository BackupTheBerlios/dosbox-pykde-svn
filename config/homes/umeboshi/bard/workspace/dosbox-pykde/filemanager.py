import os, sys
from zipfile import ZipFile

from useless.base.util import md5sum

class ExistsError(StandardError):
    pass

class FileError(StandardError):
    pass
# default locations
INSTALLED_ARCHIVES_PATH = '/mirrors/share/archives/dosbox-installed'

def generate_md5sums():
    if os.path.exists('md5sums.txt'):
        raise ExistsError, 'md5sums.txt already exists'
    notregex = '-not -regex "./md5sums.txt"'
    bashcmd = "find -type f %s -exec md5sum '{}' >> md5sums.txt \;" % notregex
    os.system('bash -c "%s"' % bashcmd)

def _checkifdir(path):
    if not os.path.isdir(path):
        raise FileError, "%s must be a directory" % path

def _itemize_md5sum_line(line):
    hashlen = 32
    return (line[hashlen:].strip(), line[:hashlen])

def make_md5sum_dict(md5sumtext):
    md5dict = {}
    for line in md5sumtext.split('\n'):
        if line:
            k, v = _itemize_md5sum_line(line)
            md5dict[k] = v
    return md5dict

def determine_zipfilename(path, name=None):
    if name is None:
        name = os.path.basename(path)
    if not name.endswith('.zip'):
        name = '%s.zip' % name
    zfilename = os.path.join(INSTALLED_ARCHIVES_PATH, name)
    return zfilename

def archive_fresh_install(path, name=None):
    _checkifdir(path)
    here = os.getcwd()
    os.chdir(path)
    generate_md5sums()
    zfilename = determine_zipfilename(path, name)
    if os.path.exists(zfilename):
        raise ExistsError, '%s already exists.' % zfilename
    os.system('zip -r %s .' % zfilename)
    os.chdir(here)

def cleanup_install_path(path, name=None):
    _checkifdir(path)
    here = os.getcwd()
    zfilename = determine_zipfilename(path, name)
    if not os.path.exists(zfilename):
        raise ExistsError, "%s doesn't exist." % zfilename
    zfile = ZipFile(zfilename, 'r')
    md5sumstext = zfile.read('md5sums.txt')
    md5sums = make_md5sum_dict(md5sumstext)
    return md5sums

# come back to this later
def _python_fill_zip(zfilename):
    zfile = ZipFile(zfilename, 'w')
    for root, dirs, files in os.walk('./', topdown=True):
        for filename in files:
            fullpath = os.path.join(root, filename)
            zfile.write(fullpath)
        for dirname in dirs:
            fullpath = os.path.join(root, dirname)
            if not len(os.listdir(fullpath)):
                zi = ZipInfo('foo')
            zfile.write(fullpath)
    zfile.close()
    
    
        

if __name__ == '__main__':
    af = archive_fresh_install
    af(os.getcwd(), 'test')
    
