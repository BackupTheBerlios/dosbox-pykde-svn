import os, sys
import shutil

from dboxpykde.base import ExistsError, FileError
from dboxpykde.base import md5sum, makepaths

from myzipfile import MyZipFile

def _checkifdir(path):
    if not os.path.isdir(path):
        raise FileError, "%s must be a directory" % path

def _itemize_md5sum_line(line):
    hashlen = 32
    return (line[hashlen:].strip(), line[:hashlen])

def make_md5sum_dict(installed_files):
    print 'called make_md5sum_dict'
    return dict(installed_files)

def convert_filename_to_uppercase(filename, root):
    converted = False
    if filename != filename.upper():
        old = os.path.join(root, filename)
        new = os.path.join(root, filename.upper())
        os.rename(old, new)
        converted = True
    return converted

def convert_tree_to_uppercase(path):
    converted = []
    for root, dirs files in os.walk(path, topdown=False):
        for dname in dirs:
            if convert_filename_to_uppercase(dname, root):
                converted.append(os.path.join(root, dname))
        for fname in files:
            if convert_filename_to_uppercase(fname, root):
                converted.append(os.path.join(root, fname))
    return converted

            


# generate md5sums for all files
# in the current directory recursively
# must be in the target directory before calling this
def generate_md5sums():
    installed_files = []
    for root, dirs, files in os.walk('.', topdown=True):
        for name in files:
            filename = os.path.join(root, name)
            md = md5sum(file(filename))
            installed_files.append((filename, md))
    return installed_files

class ArchiveHelper(object):
    def __init__(self, app):
        self.app = app
        
    def make_tmp_path(self, name):
        tpath = os.path.join(self.app.tmpdir, name)
        makepaths(tpath)
        return tpath

    def _unchanged_files_holding_path(self, path):
        return '%s.tmp' % path
    
    def determine_install_zipfilename(self, path=None, name=None):
        INSTALLED_ARCHIVES_PATH = self.app.installed_archives_path
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

    def determine_extras_archivename(self, name):
        EXTRAS_ARCHIVES_PATH = self.app.extras_archives_path
        suffix = '-extras.tar.bz2'
        if not name.endswith(suffix):
            name = '%s%s' % (name, suffix)
        archivename = os.path.join(EXTRAS_ARCHIVES_PATH, name)
        return archivename

    def determine_extras_repos(self, name):
        extras_archives_path = self.app.extras_archives_path
        repos_path = os.path.join(extras_archives_path, name)
        return repos_path
    
    def determine_old_archivename(self, archivename):
        oldnum = 1
        oldarchive = '%s.bkup.%d' % (archivename, oldnum)
        while os.path.exists(oldarchive):
            oldnum += 1
            oldarchive = '%s.bkup.%d' % (archivename, oldnum)
        return oldarchive

    # we use this function to determine the unchanged files
    # in the install path.
    def handle_installed_files(self, path, installed_files):
        unchanged_files = []
        _checkifdir(path)
        here = os.getcwd()
        os.chdir(path)
        count = 1
        for filename, md5hash in installed_files:
            self.report_installed_file_handled(filename, count)
            if not os.path.exists(filename):
                print filename, 'non-existant, skipping.'
            else:
                if md5sum(file(filename)) == md5hash:
                    unchanged_files.append(filename)
                else:
                    print filename, 'has changed.'
            count += 1
        os.chdir(here)
        return unchanged_files

    def report_installed_file_handled(self, filename, count):
        print 'filename', filename, count
    
    # using the list of unchanged files we get from handle_installed_files
    # we remove, or move elsewhere, those files to prepare for archiving
    # the leftovers.  If remove is True, we remove the files (we can restore
    # them later from the installed archive).  If remove is False, we move them
    # temporarily to another directory (currently unhandled).
    def cleanup_unchanged_files(self, path, unchanged_files, remove=True):
        _checkifdir(path)
        here = os.getcwd()
        if not remove:
            newpath = self._unchanged_files_holding_path(path)
            makepaths(newpath)
        os.chdir(path)
        if remove:
            map(os.remove, unchanged_files)
        else:
            print "remove is false, moving files to", newpath
            for afile in unchanged_files:
                dirname, basename = os.path.split(afile)
                newdir = os.path.join(newpath, dirname)
                makepaths(newdir)
                newfile = os.path.join(newdir, basename)
                # clean up the path name
                newfile = os.path.normpath(newfile)
                os.rename(afile, newfile)
            print os.listdir(newpath)
        os.chdir(here)

    # rename the unchanged files that were moved back to their
    # original place
    def rename_unchanged_files_to_orig(self, path, unchanged_files):
        _checkifdir(path)
        here = os.getcwd()
        os.chdir(path)
        newpath = self._unchanged_files_holding_path(path)
        for afile in unchanged_files:
            dirname, basename = os.path.split(afile)
            newdir = os.path.join(newpath, dirname)
            newfile = os.path.join(newdir, basename)
            # clean up the path name
            newfile = os.path.normpath(newfile)
            os.rename(newfile, afile)
        os.chdir(here)
        
    # this function extracts the extras archive for a game to a temporary
    # path, then returns that path
    def extract_extras_archive(self, name, extract_cmd='tar xfj'):
        archivename = self.determine_extras_archivename(name)
        tpath = self.make_tmp_path(name)
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
    def stage_rdiff_backup_archive(self, name, time='now'):
        tpath = self.extract_extras_archive(name)
        staging_path = self.stage_rdiff_backup_repos(tpath, time=time)
        # remove tpath
        self.remove_tree(tpath)
        return staging_path

    # this function restores a rdiff-backup into a staging directory
    # to be later rsync-ed into the game directory
    # returns the staging path
    def stage_rdiff_backup_repos(self, repos_path, time='now'):
        staging_path = '%s-staging' % repos_path
        makepaths(staging_path)
        restore_cmd = 'rdiff-backup --force -r %s %s %s' % (time, repos_path, staging_path)
        result = os.system(restore_cmd)
        if result:
            raise OSError, "there was a problem with %s" % restore_cmd
        return staging_path
    
    def perform_rdiff_backup(self, path, backup_path):
        if not os.path.isdir(backup_path):
            raise ExistsError, "backup path %s doesn't exist" % backup_path
        cmd = 'rdiff-backup -v0 "%s" %s' % (path, backup_path)
        result = os.system(cmd)
        if result:
            raise OSError, "problem with perform_rdiff_backup %s" % cmd
    
    

    def archive_rdiff_backup_repos(self, name, path):
        archivename = self.determine_extras_archivename(name)
        config = self.app.myconfig
        if not config.getboolean('filemanagement', 'overwrite_extras_archives'):
            oldarchive = self.determine_old_archivename(archivename)
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

    def copy_staging_tree_with_rsync(self, staging_path, install_path):
        if not staging_path.endswith('/'):
            staging_path = '%s/' % staging_path
        if not install_path.endswith('/'):
            install_path = '%s/' % install_path
        cmd = 'rsync -a %s "%s"' % (staging_path, install_path)
        result = os.system(cmd)
        if result:
            raise OSError, 'problem with %s' % cmd

    def remove_tree(self, path, system=False):
        if system:
            cmd = 'rm -rf %s' % path
            result = os.system(cmd)
            if result:
                raise OSError, 'problem with %s' % cmd
        else:
            shutil.rmtree(path)
    

class GameFilesHandler(object):
    def __init__(self, app):
        self.app = app
        # datahandler should already be in app object
        # and be a GameDataHandler object
        self.datahandler = self.app.game_datahandler
        self.archivehelper = ArchiveHelper(self.app)

    # unarchive game files into main dosboxpath
    # unarchives from install archive
    # and get latest files from extras  archive
    # if extras is false, just prepare freshly installed game
    def prepare_game(self, name, time='now', extras=True):
        fullpath = self._get_fullpath(name)
        if os.path.exists(fullpath):
            _checkifdir(fullpath)
        else:
            makepaths(fullpath)
        zfilename = self.archivehelper.determine_install_zipfilename(name=name)
        if not os.path.exists(zfilename):
            raise ExistsError, "%s for %s doesn't exist." % (zfilename, name)
        zfile = MyZipFile(zfilename, 'r')
        zfile.extract(path=fullpath, report=self._report_extract_from_installed_archive)
        if extras:
            self.restore_extra_files(name, time=time)

    def restore_extra_files(self, name, time='now'):
        fullpath = self._get_fullpath(name)
        if self.app.myconfig.getboolean('filemanagement', 'extras_archives_tarballs'):
            archivename = self.archivehelper.determine_extras_archivename(name)
            if not os.path.exists(archivename):
                print 'Using fresh install for', name
            else:
                staging_path = self.archivehelper.stage_rdiff_backup_archive(name, time=time)
                self.archivehelper.copy_staging_tree_with_rsync(staging_path, fullpath)
                self.archivehelper.remove_tree(staging_path)
        else:
            repos_path = self.archivehelper.determine_extras_repos(name)
            if not os.path.isdir(repos_path):
                print 'Using fresh install for', name
            else:
                staging_path = self.archivehelper.stage_rdiff_backup_repos(repos_path, time=time)
                self.archivehelper.copy_staging_tree_with_rsync(staging_path, fullpath)
                self.archivehelper.remove_tree(staging_path)
                

    def backup_extra_files(self, name, path=None):
        if path is None:
            path = self._get_fullpath(name)
        tarball = self.app.myconfig.getboolean('filemanagement', 'extras_archives_tarballs')
        # determine where the rdiff-backup repository is
        if tarball:
            # if it's in a tarball, extract it
            repos_path = self.archivehelper.extract_extras_archive(name)
        else:
            repos_path = self.archivehelper.determine_extras_repos(name)
        # do the rdiff-backup
        self.archivehelper.perform_rdiff_backup(path, repos_path)
        # if rdiff-backup repos is stored in a tarball, we need to
        # archive it and remove the repos path
        if tarball:
            self.archivehelper.archive_rdiff_backup_repos(name, repos_path)
            self.archivehelper.remove_tree(repos_path)
            
            
    
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
        zfilename = self.archivehelper.determine_install_zipfilename(name=name)
        if os.path.exists(zfilename):
            raise ExistsError, 'Installed zipfile for %s already exists.' % name
        zfile = MyZipFile(zfilename, 'w')
        zfile.archive_path(path='.', report=self._report_add_to_installed_archive)
        zfile.close()
        os.chdir(here)
        return installed_files
    
        
    def add_new_game(self, gamedata, path):
        print 'ensure all files and directories are uppercase'
        converted = convert_tree_to_uppercase(path)
        if converted:
            print 'these files converted to uppercase', converted
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
        unchanged_files = self.archivehelper.handle_installed_files(fullpath, installed_files)
        # remove the unchanged files
        self.archivehelper.cleanup_unchanged_files(fullpath, unchanged_files)
        # backup the remaining extra files
        self.backup_extra_files(name, path=fullpath)
        # finally remove the installed path
        self.archivehelper.remove_tree(fullpath)

    # move files already in install archive to new location
    # and backup remaining files in extras archive (using rdiff-backup)
    # then move installed files back
    def backup_game_files(self, name):
        fullpath = self._get_fullpath(name)
        installed_files = self.datahandler.get_installed_files(name)
        # figure out which files to remove
        unchanged_files = self.archivehelper.handle_installed_files(fullpath, installed_files)
        # move the unchanged files
        self.archivehelper.cleanup_unchanged_files(fullpath, unchanged_files, remove=False)
        # backup the remaining extra files
        self.backup_extra_files(name, path=fullpath)
        # put unchanged files back to original place
        self.archivehelper.rename_unchanged_files_to_orig(fullpath, unchanged_files)
        # finally remove the path where unchanged files were held
        newpath = self.archivehelper._unchanged_files_holding_path(fullpath)
        self.archivehelper.remove_tree(newpath)

    # get full install path of named game
    def _get_fullpath(self, name):
        mainpath = self.app.main_dosbox_path
        #mainpath = MAIN_DOSBOX_PATH
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

    def audit_game_files(self, name, from_install=True, time='now'):
        fullpath = self._get_fullpath(name)
        installed_files = self.datahandler.get_installed_files(name)
        unchanged_files = self.archivehelper.handle_installed_files(fullpath, installed_files)
        installed_files = [t[0] for t in installed_files]
        changed_files = [f for f in installed_files if f not in unchanged_files]
        here = os.getcwd()
        os.chdir(fullpath)
        extra_files = []
        for root, dirs, files in os.walk('.'):
            for afile in files:
                bfile = os.path.join(root, afile)
                if bfile not in installed_files:
                    extra_files.append(bfile)
        os.chdir(here)
        return unchanged_files, changed_files, extra_files
    
if __name__ == '__main__':
    #af = archive_fresh_install
    #af(os.getcwd(), 'test')
    pass
