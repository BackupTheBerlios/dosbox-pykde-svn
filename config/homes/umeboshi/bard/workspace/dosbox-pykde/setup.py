#!/usr/bin/python
import os, sys, glob
from distutils.core import setup

# we don't want to clutter the namespace in site-packages
# so we hand compile the modules and handle them as datafiles
import compileall
from distutils.command.clean import clean as _clean
from distutils.command.build import build as _build



# override clean command to remove compiled modules
class clean(_clean):
    def run(self):
        _clean.run(self)
        compiled = glob.glob(os.path.join(modules_dir, '*.pyc'))
        map(os.remove, compiled)

# override build command to compile modules
class build(_build):
    def run(self):
        _build.run(self)
        compileall.compile_dir(modules_dir, maxlevels=0)
        
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
# get a list of the modules
modules = glob.glob(os.path.join(modules_dir, '*.py'))

# append compiled modules to list (they shouldn't be made yet,
# but when they are, they'll be listed here to install as datafiles)
modules += ['%sc' % m for m in modules]

#compileall.compile_dir(modules_dir, maxlevels=1)

data_files = [
    (docs_directory, ['README']),
    (modules_install_path, modules)
    ]

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

      
