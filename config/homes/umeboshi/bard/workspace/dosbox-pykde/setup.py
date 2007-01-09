#!/usr/bin/python
import os, sys, glob
from distutils.core import setup

# we don't want to clutter the namespace in site-packages
# so we hand compile the modules and handle them as datafiles
import compileall
from distutils.command.clean import clean as _clean
from distutils.command.build import build as _build


def get_modules(modules_dir, compiled=False):
    modules = {}
    for root, dirs, files in os.walk(modules_dir):
        for afile in files:
            if afile.endswith('.py'):
                fullpath = os.path.join(root, afile)
                head, tail = os.path.split(root)
                if not modules.has_key(root):
                    modules[root] = []
                modules[root].append(fullpath)
                if compiled:
                    modules[root].append('%sc' % fullpath)
    return modules

# override clean command to remove compiled modules
class clean(_clean):
    def run(self):
        _clean.run(self)
        for root, dirs, files in os.walk(os.getcwd()):
            for afile in files:
                if afile.endswith('~'):
                    #print "removing backup file", os.path.join(root, afile)
                    os.remove(os.path.join(root, afile))
                if afile.endswith('.pyc'):
                    os.remove(os.path.join(root, afile))
                    
# override build command to compile modules
class build(_build):
    def run(self):
        _build.run(self)
        for adir in get_modules(modules_dir).keys():
            compileall.compile_dir(adir, maxlevels=0)
        
version = '0'
description = 'Dosbox frontend for KDE written in PyKDE'
author = 'Joseph Rawson'
author_email = 'umeboshi@gregscomputerservice.com'
url = 'file://.'

scripts = ['dosbox-pykde']

modules_dir = 'lib'
# with the next lines we assume that this is being built with the --prefix /usr option
docs_directory = 'share/doc/dosbox-pykde'
modules_install_path = 'share/dosbox-pykde/modules'


#compileall.compile_dir(modules_dir, maxlevels=1)

data_files = [
    (docs_directory, ['README'])
    ]

# add modules and compiled modules to data_files
# modules may not be compiled yet, but will be when build runs
compiled_modules = get_modules(modules_dir, compiled=True)
for path in compiled_modules.keys():
    tails = []
    head, tail = os.path.split(path)
    if not head:
        install_path = modules_install_path
    else:
        while head:
            tails.insert(0, tail)
            head, tail = os.path.split(head)
        newpath = os.path.join(*tails)
        install_path = os.path.join(modules_install_path, newpath)
    data_files.append((install_path, compiled_modules[path]))

setup(name='dosbox-pykde',
      version=version,
      description=description,
      author=author,
      author_email=author_email,
      url=url,
      scripts=scripts,
      data_files=data_files,
      cmdclass=dict(build=build, clean=clean)
      )

      
