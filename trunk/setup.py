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
        here = os.getcwd()
        for root, dirs, files in os.walk(here):
            for afile in files:
                if afile.endswith('~'):
                    #print "removing backup file", os.path.join(root, afile)
                    os.remove(os.path.join(root, afile))
                if afile.endswith('.pyc'):
                    os.remove(os.path.join(root, afile))
        os.chdir('data/doc')
        map(os.remove, glob.glob('*.html'))
        os.chdir(here)
        
class build(_build):
    def run(self):
        _build.run(self)
        here = os.getcwd()
        os.chdir('data/doc')
        print 'building documentation'
        os.system('meinproc index.docbook')
        os.chdir(here)
        # remember that data_files and docs_directory_html are global here
        # this needs to be done here for the html pages to be included in the
        # data files, without statically listing them in the data_files definition
        data_files.append((docs_directory_html, glob.glob('data/doc/*.html')))

        

version = '0'
description = 'Dosbox frontend for KDE written in PyKDE'
author = 'Joseph Rawson'
author_email = 'umeboshi@gregscomputerservice.com'
url = 'file://.'

scripts = ['dosbox-pykde']

# with the next lines we assume that this is being built with the --prefix /usr option
docs_directory = 'share/doc/dosbox-pykde'
docs_directory_html = os.path.join(docs_directory, 'html')

packages = ['dboxpykde']
subpacks = ['common', 'contrib', 'filemanagement', 'kdelib', 'qtwin']
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
      cmdclass=dict(clean=clean, build=build)
      )

      
