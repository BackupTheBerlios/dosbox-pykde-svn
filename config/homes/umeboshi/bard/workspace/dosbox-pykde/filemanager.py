import os, sys
from zipfile import ZipFile

from useless.base.util import md5sum
from useless.base.util import makepaths

class ExistsError(StandardError):
    pass

class FileError(StandardError):
    pass

# default locations
INSTALLED_ARCHIVES_PATH = '/mirrors/share/archives/dosbox-installed'
EXTRAS_ARCHIVES_PATH = '/mirrors/share/archives/dosbox-extras'
TMP_PARENT_PATH = '/tmp/dosbox-area'
MAIN_DOSBOX_PATH = '/mirrors/share/dosbox'


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

def determine_install_zipfilename(path, name=None):
    suffix = '-installed.zip'
    if name is None:
        name = os.path.basename(path)
    if not name.endswith(suffix)
        name = '%s%s' % (name, suffix)
    zfilename = os.path.join(INSTALLED_ARCHIVES_PATH, name)
    return zfilename

def determine_extras_archivename(name):
    suffix = '-extras.tar.gz'
    if not name.endswith(suffix):
        name = '%s%s' % (name, suffix)
    archivename = os.path.join(EXTRAS_ARCHIVES_PATH, name)
    return archivename

def archive_fresh_install(path, name=None):
    _checkifdir(path)
    here = os.getcwd()
    os.chdir(path)
    generate_md5sums()
    zfilename = determine_install_zipfilename(path, name)
    if os.path.exists(zfilename):
        raise ExistsError, '%s already exists.' % zfilename
    os.system('zip -r %s .' % zfilename)
    os.chdir(here)

def make_tmp_path(name):
    tpath = os.path.join(TMP_PARENT_PATH, name)
    makepaths(tpath)
    return tpath

def extract_extras_archive(name, archivename, tpath=None):
    if tpath is None:
        tpath = make_tmp_path(name)
    os.chdir(tpath)
    os.system('tar xvfj %s' % archivename)
    
def cleanup_install_path(path, name=None):
    _checkifdir(path)
    here = os.getcwd()
    os.chdir(path)
    zfilename = determine_install_zipfilename(path, name)
    if not os.path.exists(zfilename):
        raise ExistsError, "%s doesn't exist." % zfilename
    zfile = ZipFile(zfilename, 'r')
    md5sumstext = zfile.read('md5sums.txt')
    md5sums = make_md5sum_dict(md5sumstext)
    for filename, md5hash in md5sums.items():
        if md5sum(file(filename)) == md5hash:
            print filename, 'ok, removing'
            os.remove(filename)
        else:
            print filename, 'has changed, keeping'
    archivename = determine_extras_archivename(name)
    shortname = os.path.basename(archivename)
    # ready the tmp space
    tpath = make_tmp_path(name)
    if not os.path.exists(archivename):
        print 'New archive, %s' % shortname
    else:
        extract_extras_archive(name, archivename, tpath)
    # perform rdiff-backup
    os.chdir(path)
    cmd = 'rdiff-backup . %s' % tpath
    # rearchive extras
    # don't remove oldarchive yet
    oldnum = 1
    oldarchive = '%s.bkup.%d' % (archivename, oldnum)
    while os.path.exists(oldarchive):
        oldnum += 1
        oldarchive = '%s.bkup.%d' % (archivename, oldnum)
    if os.path.exists(archivename):
        os.rename(archivename, oldarchive)
    # start archival
    os.chdir(tpath)
    cmd = 'tar cvj . -f %s' % archivename
    os.system(cmd)
    # go back
    os.chdir(here)
    # remove tmp stuff
    os.system('rm -fr %s' % tpath)
    # remove install area
    os.system('rm -fr %s' % path)


def prepare_game(path, name=None):
    here = os.getcwd()
    if os.path.exists(path):
        _checkifdir(path)
    else:
        makepaths(path)
    os.chdir(path)
    zfilename = determine_install_zipfilename(path, name)
    archivename = determine_extras_archivename(name)
    if not os.path.exists(zfilename):
        raise ExistsError, "%s doesn't exist"
    # unzip fresh install
    os.system('unzip %s' % zfilename)
    if not os.path.exists(archivename):
        print "Using fresh install"
    else:
        tpath = make_tmp_path(name)
        extract_extras_archive(name, archivename, tpath)
        cmd = 'rdiff-backup -r now %s %s' % (tpath, path)
        os.system(cmd)
        os.system('rm -rf %s' % tpath)
    os.chdir(here)
    
        


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
    
