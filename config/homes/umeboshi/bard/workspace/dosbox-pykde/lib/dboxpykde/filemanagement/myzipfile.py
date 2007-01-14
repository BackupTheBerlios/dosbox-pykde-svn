import os, sys
import time
from datetime import datetime
from zipfile import ZipFile, ZipInfo

from dboxpykde.base import makepaths

class MyZipFile(ZipFile):
    def _extract_file(self, name, path):
        zinfo = self.getinfo(name)
        bytes = self.read(name)
        fullpath = os.path.join(path, name)
        newfile = file(fullpath, 'w')
        newfile.write(bytes)
        newfile.close()
        # set the mtime
        dt = datetime(*zinfo.date_time)
        timestamp = time.mktime(dt.timetuple())
        os.utime(fullpath, (timestamp, timestamp))
        
    def extract(self, name=None, path=None, report=None):
        if path is None:
            path = os.getcwd()
        if not os.path.isdir(path):
            raise IOError, 'directory %s not found.' % path
        if name is None:
            namelist = self.namelist()
            total = len(namelist)
            count = 0
            for filename in namelist:
                if report is not None:
                    report(filename, count, total)
                dirname = os.path.dirname(filename)
                if dirname:
                    complete_dirname = os.path.join(path, dirname)
                    makepaths(complete_dirname)
                basename = os.path.basename(filename)
                if basename:
                    self._extract_file(filename, path)
                count += 1
                
    def archive_path(self, path=None, report=None):
        here = os.getcwd()
        if path is None:
            path = here
        os.chdir(path)
        # calculate total files and dirs first
        total = 0
        for root, dirs, files in os.walk('.', topdown=True):
            total += 1
            total += len(files)
        count = 0
        for root, dirs, files in os.walk('.', topdown=True):
            for filename in files:
                fullpath = os.path.join(root, filename)
                if report is not None:
                    report(fullpath, count, total)
                self.write(fullpath)
                count += 1
            # do the directories last
            for dirname in dirs:
                fullpath = os.path.join(root, dirname)
                # only add empty directories
                if not os.listdir(fullpath):
                    fullpath = '%s/' % fullpath
                    info = ZipInfo(fullpath)
                    st = os.stat(fullpath)
                    mtime = time.localtime(st.st_mtime)
                    date_time = mtime[0:6]
                    info.date_time = date_time
                    self.writestr(info, '')
                if report is not None:
                        report(fullpath, count, total)
                count += 1
        os.chdir(here)
        
def unzip_file(filename, path):
    if not os.path.exists(path):
        makepaths(path)
    if not os.path.isdir(path):
        raise StandardError, "%s already exists and is not a directory." % path
    #zfile = ZipFile(filename, 'r')
    zfile = MyZipFile(filename, 'r')
    zfile.extract(path=path)

def extract_report(filename, count, total):
    print 'extracting', filename, count, total

def archive_report(filename, count, total):
    print 'archiving', filename, count, total
    
if __name__ == '__main__':
    zipfilename = sys.argv[1]
    path = sys.argv[2]
    #unzip_file(zipfilename, path)
    makepaths(path)
    mf = MyZipFile(zipfilename, 'r')
    mf.extract(path=path, report=extract_report)
    empty_dirs = [os.path.join(path, adir) for adir in ['heythere', 'hello', 'something/else']]
    #makepaths(*empty_dirs)
    mf = MyZipFile('anewfile.zip', 'w')
    mf.archive_path(path, report=archive_report)
    mf.close()
    
    
