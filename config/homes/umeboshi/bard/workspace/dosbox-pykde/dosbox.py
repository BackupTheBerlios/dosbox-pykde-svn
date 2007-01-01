import os
from ConfigParser import ConfigParser

DosboxConfigSections = ['sdl', 'dosbox', 'render', 'cpu', 'mixer',
                        'midi', 'sblaster', 'gus', 'speaker', 'bios', 'serial',
                        'dos', 'ipx', 'autoexec']
# override default ConfigParser
# to keep sections in order, and autoexec section last
class DosboxConfig(ConfigParser):
    pass
    

# app is the KDE application class
class Dosbox(object):
    def __init__(self, app):
        self.app = app
        self.main_config_dir = self.app.main_config_dir
        self.default_config = os.path.join(self.main_config_dir, 'dosbox.conf.default')
        self._dosbox_binary = self.app.config.get('DEFAULT', 'dosbox_binary')
        
        
    def _configfilename(self, name):
        return os.path.join(self.main_config_dir, 'configs', '%s.dosboxrc' % name)

    def conf_opt(self, name):
        configfilename = self._configfilename(name)
        if not os.path.isfile(configfilename):
            configfilename = self.default_config
        return '-conf %s' % configfilename

    def _get_args(self, name):
        handler = self.app.game_datahandler
        gamedata = handler.get_game_data(name)
        dosboxpath = gamedata['dosboxpath']
        launchcmd = '-c %s' % gamedata['launchcmd']
        mount_opt = '-c "mount c %s"' % self.app.config.get('DEFAULT', 'main_dosbox_path')
        cdrive_opt = '-c c:'
        cd_path_opt = '-c "cd %s"' % dosboxpath
        conf_opt = self.conf_opt(name)
        # order is mount_opt cdrive_opt cd_path_opt launchcmd conf_opt
        args = '%s %s %s %s %s' % (mount_opt, cdrive_opt, cd_path_opt, launchcmd, conf_opt)
        return args
    
    def _cmd(self, name):
        args = self._get_args(name)
        cmd = '%s %s' % (self._dosbox_binary, args)
        print 'dosbox cmd -- ', cmd
        return cmd
    
    def run_game(self, name):
        cmd = self._cmd(name)
        os.system(cmd)
        
    
