import os, sys
from ConfigParser import ConfigParser

# setup ConfigParser
config = ConfigParser()
configfiles = ['dosbox-pykde.conf', os.path.expanduser('~/.dosbox-pykde.conf')]
config.read(configfiles)

if __name__ == '__main__':
    print 'testing config module'
    
