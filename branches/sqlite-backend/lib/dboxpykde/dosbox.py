import os
import subprocess

from ConfigParser import ConfigParser

from dboxpykde.base import makepaths

DosboxConfigSections = ['sdl', 'dosbox', 'render', 'cpu', 'mixer',
                        'midi', 'sblaster', 'gus', 'speaker', 'bios', 'serial',
                        'dos', 'ipx', 'autoexec']

# override default ConfigParser
# to keep sections in order, and autoexec section last
# currently this isn't done, autoexec section is unsupported
class DosboxConfig(ConfigParser):
    pass
    
class SimpleDosboxHandler(object):
    def __init__(self):
        self._mount_opt = None
        

    def set_dosbox_binary(self, binary):
        self._dosbox_binary = binary

    def set_config_file(self, filename):
        self._config_file = filename

    

# app is the KDE application object
class DosboxOrig(object):
    def __init__(self, app):
        self.app = app
        self.main_config_dir = self.app.main_config_dir
        self.profiles_dir = os.path.join(self.main_config_dir, 'profiles')
        self.default_config = os.path.join(self.main_config_dir, 'dosbox.conf.default')
        self.tmp_parent_path = os.path.join(self.app.tmpdir, 'dosbox-area')
        if not os.path.isdir(self.tmp_parent_path):
            makepaths(self.tmp_parent_path)
        self._dosbox_binary = self.app.myconfig.get('dosbox', 'dosbox_binary')
        self.current_profile = None
        profiles = self.get_profile_list()
        if not profiles or 'default' not in profiles:
            print 'creating default profile'
            cfg = self.get_default_config()
            self.save_profile('default', cfg)
        self.set_current_profile('default')
        
        
    def get_capture_path(self, name):
        return os.path.join(self.main_config_dir, 'capture', name)

    
    def _mapper_filename(self, name):
        return os.path.join(self.main_config_dir, 'configs', '%s.mapper.txt' % name)
    
    def _configfilename(self, name):
        fname = '%s.dosbox.conf' % name
        return os.path.join(self.tmp_parent_path, fname)
    
    def _game_specific_configfilename(self, name):
        return os.path.join(self.main_config_dir, 'configs', '%s.dosboxrc' % name)
    
    def _get_profile_configfilename(self, profile):
        return os.path.join(self.main_config_dir, 'profiles', '%s.dosbox.conf' % profile)

    def get_profile_list(self):
        files = os.listdir(self.profiles_dir)
        profiles = []
        for filename in files:
            suffix = '.dosbox.conf'
            if filename.endswith(suffix):
                profile = filename[: - len(suffix)]
                profiles.append(profile)
        return profiles

    def get_default_config(self):
        config = ConfigParser()
        config.read([self.default_config])
        return config

    def save_profile(self, profilename, configobj):
        filename = self._get_profile_configfilename(profilename)
        profile = file(filename, 'w')
        configobj.write(profile)
        profile.close()

    def load_profile(self, profile):
        filename = self._get_profile_configfilename(profile)
        cfg = ConfigParser()
        cfg.read([filename])
        return cfg

    def set_current_profile(self, profile):
        #cfg = self.load_profile(profile)
        self.current_profile = profile
        
    def generate_configuration(self, name):
        config = DosboxConfig()
        # order is default then game-specific
        # game-specific overrides default
        cfiles = [self.default_config]
        if self.current_profile is not None:
            cfiles.append(self._get_profile_configfilename(self.current_profile))
        cfiles.append(self._game_specific_configfilename(name))
        config.read(cfiles)
        # setup capture directory
        path = self.get_capture_path(name)
        if not os.path.exists(path):
            makepaths(path)
        config.set('dosbox', 'captures', path)
        mapperfile = self._mapper_filename(name)
        if os.path.exists(mapperfile):
            config.set('sdl', 'mapperfile', mapperfile)
        configfilename = self._configfilename(name)
        dirname = os.path.dirname(configfilename)
        if not os.path.exists(dirname):
            makepaths(dirname)
        config.write(file(configfilename, 'w'))
        

    def conf_opt(self, name):
        configfilename = self._configfilename(name)
        if not os.path.isfile(configfilename):
            raise ExistsError, "%s doesn't exist." % configfilename
        return '-conf "%s"' % configfilename

    def _get_args(self, name, launch_game=True, use_config=True):
        handler = self.app.game_datahandler
        gamedata = handler.get_game_data(name)
        main_dosbox_path = self.app.myconfig.get('dosbox', 'main_dosbox_path')
        cdrive_is_main_dosbox_path = self.app.myconfig.getboolean('dosbox',
                                                         'cdrive_is_main_dosbox_path')
        dosboxpath = gamedata['dosboxpath']
        launchcmd = gamedata['launchcmd']
        conf_opt = None
        if use_config:
            conf_opt = self.conf_opt(name)
        if cdrive_is_main_dosbox_path:
            launchcmd_opt = '-c %s' % gamedata['launchcmd']
            mount_opt = '-c "mount c %s"' % main_dosbox_path
            cdrive_opt = '-c c:'
            cd_path_opt = '-c "cd %s"' % dosboxpath
            # order is mount_opt cdrive_opt cd_path_opt launchcmd conf_opt
            # mount c: -- 'cd' to c: -- cd $dosboxpath -- launchcmd
            args = ' '.join([mount_opt, cdrive_opt, cd_path_opt, launchcmd_opt, conf_opt])
        else:
            # using this method may allow longfilenames in intermediate paths
            if launch_game:
                fullpath = os.path.join(main_dosbox_path, dosboxpath, launchcmd)
            else:
                fullpath = os.path.join(main_dosbox_path, dosboxpath)
            # args are much smaller with option
            if conf_opt is None:
                args = '"%s"' % fullpath
            else:
                args = '"%s" %s' % (fullpath, conf_opt)
        return args

    # default args to None here instead of ''
    # if args is '', then just dosbox is run
    def _cmd(self, name, args=None):
        if args is None:
            args = self._get_args(name)
        cmd = '%s %s' % (self._dosbox_binary, args)
        print 'dosbox cmd -- ', cmd
        return cmd
    
    def run_game(self, name):
        self.generate_configuration(name)
        cmd = self._cmd(name)
        os.system(cmd)

    def launch_dosbox_prompt(self, name, genconfig=True):
        if genconfig:
            self.generate_configuration(name)
        args = self._get_args(name, launch_game=False, use_config=genconfig)
        cmd = self._cmd(name, args)
        os.system(cmd)


class DosboxNew(object):
    def __init__(self, app):
        self.app = app
        self.main_config_dir  = self.app.main_config_dir
        self.profiles_dir = self.main_config_dir / 'profiles'
        self.default_config = self.main_config_dir / 'dosbox.conf.default'
        self.tmp_parent_path = self.app.tmpdir / 'dosbox-area'
        if not self.tmp_parent_path.exists():
            self.tmp_parent_path.makedirs()
        self._dosbox_binary = self.app.myconfig.get('dosbox', 'dosbox_binary')
        self.current_profile = None

    def get_capture_path(self, name):
        return self.main_config_dir / 'capture' / name

    def _mapper_filename(self, name):
        fname = '%s.mapper.txt' % name
        return self.main_config_dir / 'configs' / fname

    def _configfilename(self, name):
        fname = '%s.dosbox.conf' % name
        return self.tmp_parent_path / fname

    def _game_specific_configfilename(self, name):
        fname = '%s.dosboxrc' % name
        return self.main_config_dir / 'configs' / fname

    def _get_profile_configfilename(self, profile):
        fname = '%s.dosbox.conf' % profile
        return self.profiles_dir / fname

    def get_profile_list(self):
        files = [f.basename() for f in self.profiles_dir.listdir()]
        profiles = []
        for filename in files:
            suffix = '.dosbox.conf'
            if filename.endswith(suffix):
                profile = filename[:-len(suffix)]
                profiles.append(profile)
        return profiles

    def get_default_config(self):
        config = ConfigParser()
        config.read(self.default_config)
        return config

    def save_profile(self, profilename, configobj):
        filename = self._get_profile_configfilename(profilename)
        profile = filename.open('w')
        configobj.write(profile)
        profile.close()

    def load_profile(self, profile):
        filename = self._get_profile_configfilename(profile)
        cfg = ConfigParser()
        cfg.read([filename])
        return cfg

    def set_current_profile(self, profile):
        self.current_profile = profile

    def generate_configuration(self, name):
        config = DosboxConfig()
        # order is default then game-specific
        # game-specific overrides default
        cfiles = [self.default_config]
        if self.current_profile is not None:
            cfiles.append(self._get_profile_configfilename(self.current_profile))
        cfiles.append(self._game_specific_configfilename(name))
        config.read(cfiles)
        cpath = self.get_capture_path(name)
        if not cpath.exists():
            cpath.makedirs()
        config.set('dosbox', 'captures', cpath)
        mapperfile = self._mapper_filename(name)
        if mapperfile.exists():
            config.set('sdl', 'mapperfile', mapperfile)
        configfilename = self._configfilename(name)
        dirname = configfilename.dirname()
        if not dirname.exists():
            dirname.makedirs()
        config.write(configfilename.open('w'))

    def _launchcmd_opt(self, launchcmd):
        return ['-c', launchcmd]

    def _mount_opt(self, mpath):
        cmd = 'mount c %s' % mpath
        return ['-c', cmd]

    def _cdrive_opt(self):
        return ['-c', 'c:']

    # cd means change directory
    # not compact disc
    def _cd_path_opt(self, cdpath):
        cmd = 'cd %s' % cdpath
        return ['-c', cmd]

    def _conf_opt(self, name):
        configfilename = self._configfilename(name)
        if not configfilename.isfile():
            raise ExistsError, "%s doesn't exist." % configfilename
        return ['-conf', configfilename]
    
    # this is same as the old function
    # it needs to be split into smaller functions
    def _get_args(self, name, launch_game=True, use_config=True):
        handler = self.app.game_datahandler
        gamedata = handler.get_game_data(name)
        main_dosbox_path = self.app.myconfig.getpath('dosbox', 'main_dosbox_path')
        cdrive_is_main_dosbox_path = self.app.myconfig.getboolean('dosbox',
                                                                  'cdrive_is_main_dosbox_path')
        dosboxpath = gamedata['dosboxpath']
        launchcmd = gamedata['launchcmd']
        conf_opt = []
        if use_config:
            conf_opt = self._conf_opt(name)
        if cdrive_is_main_dosbox_path:
            args = []
            args += self._mount_opt(main_dosbox_path)
            args += self._cdrive_opt()
            args += self._cd_path_opt(dosboxpath)
            args += self._launchcmd_opt(launchcmd)
            args += conf_opt
        else:
            if launch_game:
                fullpath = main_dosbox_path / dosboxpath / launchcmd
            else:
                fullpath = main_dosbox_path / dosboxpath
            if not conf_opt:
                args = [fullpath]
            else:
                args = [fullpath] +  conf_opt
        args = [str(arg) for arg in args]
        return args
    
        
    def _cmd(self, name, args=[]):
        if not args:
            args = self._get_args(name)
        cmd = [self._dosbox_binary ] + args
        print 'dosbox cmd -- ', cmd
        return cmd

    def run_game(self, name):
        self.generate_configuration(name)
        cmd = self._cmd(name)
        subprocess.call(cmd)

    def launch_dosbox_prompt(self, name, genconfig=True):
        if genconfig:
            self.generate_configuration(name)
        args = self._get_args(name, launch_game=False, use_config=genconfig)
        cmd = self._cmd(name, args)
        subprocess.call(cmd)
        
            
    
Dosbox = DosboxNew
#Dosbox = DosboxOrig
