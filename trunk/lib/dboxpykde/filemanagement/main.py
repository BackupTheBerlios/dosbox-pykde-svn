import os, sys
import shutil
from zipfile import ZipFile

from dboxpykde.base import ExistsError, FileError
from dboxpykde.base import md5sum, makepaths

from dboxpykde.config import config
from myzipfile import MyZipFile

# default locations
INSTALLED_ARCHIVES_PATH = config.get('DEFAULT', 'installed_archives_path')
EXTRAS_ARCHIVES_PATH = config.get('DEFAULT', 'extras_archives_path')
TMP_PARENT_PATH = config.get('DEFAULT', 'tmp_parent_path')
MAIN_DOSBOX_PATH = config.get('DEFAULT', 'main_dosbox_path')

makepaths(INSTALLED_ARCHIVES_PATH, EXTRAS_ARCHIVES_PATH)

def _checkifdir(path):
    if not os.path.isdir(path):
        raise FileError, "%s must be a directory" % path

def _itemize_md5sum_line(line):
    hashlen = 32
    return (line[hashlen:].strip(), line[:hashlen])

def make_tmp_path(name):
    tpath = os.path.join(TMP_PARENT_PATH, name)
    makepaths(tpath)
    return tpath

def make_md5sum_dict(installed_files):
    print 'called make_md5sum_dict'
    return dict(installed_files)

def generate_md5sums():
    installed_files = []
    for root, dirs, files in os.walk('.', topdown=True):
        for name in files:
            filename = os.path.join(root, name)
            md = md5sum(file(filename))
            installed_files.append((filename, md))
    return installed_files


def determine_install_zipfilename(path=None, name=None):
    if path is not None:
        msg = "we're not using path argument to determine_install_zipfilename anymore"
        raise StandardError, msg
    suffix = '-installed.zip'
    if name is None:
        name = os.path.basename(path)
    if not name.endswith(suffix):
        name = '%s%s' % (name, suffix)
    zfilename = os.path.join(INSTALLED_ARCHIVES_PATH, name)
    return zfilename

def determine_extras_archivename(name):
    suffix = '-extras.tar.bz2'
    if not name.endswith(suffix):
        name = '%s%s' % (name, suffix)
    archivename = os.path.join(EXTRAS_ARCHIVES_PATH, name)
    return archivename

def determine_old_archivename(archivename):
    oldnum = 1
    oldarchive = '%s.bkup.%d' % (archivename, oldnum)
    while os.path.exists(oldarchive):
        oldnum += 1
        oldarchive = '%s.bkup.%d' % (archivename, oldnum)
    return oldarchive

# we use this function to determine the unchanged files
# in the install path.
def handle_installed_files(path, installed_files):
    unchanged_files = []
    _checkifdir(path)
    here = os.getcwd()
    os.chdir(path)
    for filename, md5hash in installed_files:
        if not os.path.exists(filename):
            print filename, 'non-existant, skipping.'
        else:
            if md5sum(file(filename)) == md5hash:
                unchanged_files.append(filename)
            else:
                print filename, 'has changed.'
    os.chdir(here)
    return unchanged_files

# using the list of unchanged files we get from handle_installed_files
# we remove, or move elsewhere, those files to prepare for archiving
# the leftovers.  If remove is True, we remove the files (we can restore
# them later from the installed archive).  If remove is False, we move them
# temporarily to another directory (currently unhandled).
def cleanup_unchanged_files(path, unchanged_files, remove=True):
    _checkifdir(path)
    here = os.getcwd()
    if not remove:
        newpath = '%s.tmp' % path
        makepaths(newpath)
    os.chdir(path)
    if remove:
        map(os.remove, unchanged_files)
    else:
        print "remove is false, but still unhandled"        
    os.chdir(here)

# this function extracts the extras archive for a game to a temporary
# path, then returns that path
def extract_extras_archive(name, extract_cmd='tar xfj'):
    archivename = determine_extras_archivename(name)
    tpath = make_tmp_path(name)
    if os.path.exists(archivename):
        here = os.getcwd()
        os.chdir(tpath)
        cmd = '%s %s' % (extract_cmd, archivename)
        result = os.system(cmd)
        if result:
            raise OSError, "there was a problem with extract_extras_archive %s" % name
        os.chdir(here)
    else:
        print "no archives exist for", name
    return tpath

# This function extracts the extras archive, then restores the
# rdiff-backup, at "time", to a staging directory, removes the
# temporary extracted path, then returns the staging path.
def stage_rdiff_backup_archive(name, time='now'):
    tpath = extract_extras_archive(name)
    staging_path = '%s-staging' % tpath
    makepaths(staging_path)
    restore_cmd = 'rdiff-backup --force -r %s %s %s' % (time, tpath, staging_path)
    result = os.system(restore_cmd)
    if result:
        raise OSError, "there was a problem with %s" % restore_cmd
    # remove tpath
    remove_tree(tpath)
    return staging_path

def perform_rdiff_backup(path, backup_path):
    if not os.path.isdir(backup_path):
        raise ExistsError, "backup path %s doesn't exist" % backup_path
    cmd = 'rdiff-backup -v0 %s %s' % (path, backup_path)
    result = os.system(cmd)
    if result:
        raise OSError, "problem with perform_rdiff_backup %s" % cmd
    
    

def archive_rdiff_backup_repos(name, path):
    archivename = determine_extras_archivename(name)
    if not config.getboolean('DEFAULT', 'overwrite_extras_archives'):
        oldarchive = determine_old_archivename(archivename)
        if os.path.exists(archivename):
            os.rename(archivename, oldarchive)
    else:
        if os.path.exists(archivename):
            os.remove(archivename)
    here = os.getcwd()
    os.chdir(path)
    cmd = 'tar cj . -f %s' % archivename
    result = os.system(cmd)
    if result:
        raise OSError, "problem with archive_rdiff_backup_repos %s" % cmd
    os.chdir(here)

def copy_staging_tree_with_rsync(staging_path, install_path):
    if not staging_path.endswith('/'):
        staging_path = '%s/' % staging_path
    if not install_path.endswith('/'):
        install_path = '%s/' % install_path
    cmd = 'rsync -a %s %s' % (staging_path, install_path)
    result = os.system(cmd)
    if result:
        raise OSError, 'problem with %s' % cmd

def remove_tree(path, system=False):
    if system:
        cmd = 'rm -rf %s' % path
        result = os.system(cmd)
        if result:
            raise OSError, 'problem with %s' % cmd
    else:
        shutil.rmtree(path)
    

def move_installed_files(path, name=None):
    raise StandardError, "don't call this function yet."
    _checkifdir(path)
    here = os.getcwd()
    os.chdir(path)
    

class GameFilesHandler(object):
    def __init__(self, datahandler):
        # datahandler should be GameDataHandler object
        self.datahandler = datahandler
        self.config = config

    # unarchive game files into main dosboxpath
    # unarchives from install archive
    # and get latest files from extras  archive
    def prepare_game(self, name, time='now'):
        fullpath = self._get_fullpath(name)
        if os.path.exists(fullpath):
            _checkifdir(fullpath)
        else:
            makepaths(fullpath)
        zfilename = determine_install_zipfilename(name=name)
        archivename = determine_extras_archivename(name)
        if not os.path.exists(zfilename):
            raise ExistsError, "%s for %s doesn't exist." % (zfilename, name)
        zfile = MyZipFile(zfilename, 'r')
        zfile.extract(path=fullpath, report=self._report_extract_from_installed_archive)
        if not os.path.exists(archivename):
            print 'Using fresh install for %s' % name
        else:
            staging_path = stage_rdiff_backup_archive(name, time=time)
            copy_staging_tree_with_rsync(staging_path, fullpath)
            remove_tree(staging_path)

    def _report_add_to_installed_archive(self, filename, count, total):
        method = '_report_add_to_installed_archive'
        print '%s -> %s, %d of %d' % (method, filename, count, total)
        
    def _report_extract_from_installed_archive(self, filename, count, total):
        method = '_report_extract_from_installed_archive'
        print '%s -> %s, %d of %d' % (method, filename, count, total)
        
    # archive a fresh game install
    def archive_fresh_install(self, gamedata, path):
        name = gamedata['name']
        fullpath = path
        _checkifdir(fullpath)
        here = os.getcwd()
        os.chdir(path)
        installed_files = generate_md5sums()
        zfilename = determine_install_zipfilename(name=name)
        if os.path.exists(zfilename):
            raise ExistsError, 'Installed zipfile for %s already exists.' % name
        zfile = MyZipFile(zfilename, 'w')
        zfile.archive_path(path='.', report=self._report_add_to_installed_archive)
        zfile.close()
        os.chdir(here)
        return installed_files
    
        
    def add_new_game(self, gamedata, path):
        print 'archive as fresh install'
        installed_files = self.archive_fresh_install(gamedata, path)
        print 'archived %d files' % len(installed_files)
        self.datahandler.add_new_game(gamedata, installed_files)
        print 'added game %s to datahandler' % gamedata['name']
        
    # remove files already in install archive and backup
    # remaining files in extras archive (using rdiff-backup)
    # then remove files
    def cleanup_game(self, name):
        fullpath = self._get_fullpath(name)
        installed_files = self.datahandler.get_installed_files(name)
        # figure out which files to remove
        unchanged_files = handle_installed_files(fullpath, installed_files)
        # remove the unchanged files
        cleanup_unchanged_files(fullpath, unchanged_files)
        # extract the extras archive to hold the remaining files
        tpath = extract_extras_archive(name)
        # do the rdiff-backup
        perform_rdiff_backup(fullpath, tpath)
        # archive the rdiff-backup repository
        archive_rdiff_backup_repos(name, tpath)
        # remove the temp path
        remove_tree(tpath)
        # finally remove the installed path
        remove_tree(fullpath)

    # get full install path of named game
    def _get_fullpath(self, name):
        mainpath = MAIN_DOSBOX_PATH
        dosboxpath = self.datahandler.get_game_data(name)['dosboxpath']
        return os.path.join(mainpath, dosboxpath)
    
    # thinking about renaming get_game_status
    def game_is_available(self, name):
        return self.get_game_status(name)
    
    def get_game_status(self, name):
        fullpath = self._get_fullpath(name)
        if os.path.isdir(fullpath):
            return True
        else:
            return False
        
if __name__ == '__main__':
    #af = archive_fresh_install
    #af(os.getcwd(), 'test')
    pass
