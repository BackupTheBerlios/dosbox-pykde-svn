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
        for root, dirs, files in os.walk(os.getcwd()):
            for afile in files:
                if afile.endswith('~'):
                    #print "removing backup file", os.path.join(root, afile)
                    os.remove(os.path.join(root, afile))
                if afile.endswith('.pyc'):
                    os.remove(os.path.join(root, afile))
                    
version = '0'
description = 'Dosbox frontend for KDE written in PyKDE'
author = 'Joseph Rawson'
author_email = 'umeboshi@gregscomputerservice.com'
url = 'file://.'

scripts = ['dosbox-pykde']

# with the next lines we assume that this is being built with the --prefix /usr option
docs_directory = 'share/doc/dosbox-pykde'

packages = ['dboxpykde']
subpacks = ['common', 'filemanagement', 'kdelib', 'qtwin']
kdelib_subpacks = ['dosboxcfg']
packages += ['dboxpykde.%s' % p for p in subpacks]
#packages += ['konsultant.managers.%s' % p for p in managers]
packages += ['dboxpykde.kdelib.%s' % p for p in kdelib_subpacks]

package_dir = {'' : 'lib'}


data_files = [
    (docs_directory, ['README'])
    ]

setup(name='dosbox-pykde',
      version=version,
      description=description,
      author=author,
      author_email=author_email,
      url=url,
      packages=packages,
      package_dir=package_dir,
      scripts=scripts,
      data_files=data_files,
      cmdclass=dict(clean=clean)
      )

      
