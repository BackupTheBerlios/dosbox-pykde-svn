import os

from xml.dom.minidom import parse as parse_file

from base import ExistsError

from gamesdataxml import GameElement, GameElementParser


class GameDataHandlerCompat(object):
    def __init__(self, app):
        self.app = app
        self.directories = self.app.data_directories
        self.gamedata_dir = self.directories['games']

    def _gamedatafilename(self, name):
        return os.path.join(self.gamedata_dir, '%s.xml' % name)

    def _installedfilesname(self, name):
        filename = '%s-md5sums.txt' % name
        return os.path.join(self.gamedata_dir, filename)
    

    def _write_xmlfile(self, element, filename):
        gamedatafile = file(filename, 'w')
        #element.writexml(gamedatafile)
        xmldata = element.toxml('utf-8')
        gamedatafile.write(xmldata)
        gamedatafile.close()
        
    def _update_xmlfile(self, gamedata, filename):
        parser = self._parse_gamedata_xmlfile(filename)
        element = GameElement(gamedata)
        self._write_xmlfile(element, filename)
        
        
    def _parse_gamedata_xmlfile(self, filename):
        parsed_element = parse_file(file(filename))
        parser = GameElementParser(parsed_element)
        return parser
    
    def add_new_game(self, gamedata, installed_files):
        name = gamedata['name']
        gamedatafilename = self._gamedatafilename(name)
        if os.path.exists(gamedatafilename):
            raise ExistsError, "%s already exists. can't add as new." % gamedatafilename
        else:
            element = GameElement(gamedata)
            self._write_xmlfile(element, gamedatafilename)
            self._add_md5sums_file(name, installed_files)
            
    def _add_md5sums_file(self, name, installed_files):
        mdfilename = self._installedfilesname(name)
        mdfile = file(mdfilename, 'w')
        for filename, mdhash in installed_files:
            mdfile.write('%s  %s\n' % (mdhash, filename))
        mdfile.close()
        
        
    def get_game_names(self):
        ls = os.listdir(self.gamedata_dir)
        games = [x[:-4] for x in ls if x.endswith('.xml')]
        return games

    def _parse_gamedata_file(self, name):
        gamedatafilename = self._gamedatafilename(name)
        return self._parse_gamedata_xmlfile(gamedatafilename)
    
    def get_game_data(self, name):
        parser = self._parse_gamedata_file(name)
        return parser.get_gamedata()

    def update_game_data(self, gamedata):
        filename = self._gamedatafilename(gamedata['name'])
        self._update_xmlfile(gamedata, filename)

    def get_title_screenshot_filename(self, name):
        screenshots_path = os.path.join(self.directories['screenshots'], name)
        return os.path.join(screenshots_path, 'title.png')
        
    # simple way to make title screenshot
    # assumes a png picture is selected
    # automatically overwrites whatever is already there
    def make_title_screenshot(self, name, picpath):
        title_pic_filename = self.get_title_screenshot_filename(name)
        dirname, basename = os.path.split(title_pic_filename)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        picdata = file(picpath).read()
        title_pic_file = file(title_pic_filename, 'w')
        title_pic_file.write(picdata)
        title_pic_file.close()

    def _itemize_md5sum_line(self, line):
        hashlen = 32
        return (line[hashlen:].strip(), line[:hashlen])

    def get_installed_files(self, name):
        installed_files = []
        mdfilename = self._installedfilesname(name)
        for line in file(mdfilename):
            if line:
                filename, mdhash = self._itemize_md5sum_line(line)
                installed_files.append((filename, mdhash))
        return installed_files
    
#########################        
class GameDataHandlerSkeleton(object):
    def __init__(self, app):
        self.app = app
        self.directories = self.app.data_directories
        self.gamedata_dir = self.directories['games']

    def add_new_game(self, gamedata, installed_files):
        pass
    
    def get_game_names(self):
        pass
    
    def get_game_data(self, name):
        pass
    

    def update_game_data(self, gamedata):
        pass

    def get_installed_files(self, name):
        pass
    
        
    def get_title_screenshot_filename(self, name):
        screenshots_path = os.path.join(self.directories['screenshots'], name)
        return os.path.join(screenshots_path, 'title.png')
        
    # simple way to make title screenshot
    # assumes a png picture is selected
    # automatically overwrites whatever is already there
    def make_title_screenshot(self, name, picpath):
        title_pic_filename = self.get_title_screenshot_filename(name)
        dirname, basename = os.path.split(title_pic_filename)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        picdata = file(picpath).read()
        title_pic_file = file(title_pic_filename, 'w')
        title_pic_file.write(picdata)
        title_pic_file.close()


if __name__ == '__main__':
    #xfile = file('amazon.xml')
    gdh = GameDataHandler('.')
    pp = gdh.get_game_data('bat')
