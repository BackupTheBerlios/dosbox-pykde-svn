import os

from xml.dom.minidom import Element, Text
from xml.dom.minidom import parse as parse_file
from xml.dom.minidom import parseString as parse_string

from base import ExistsError
from base import TooManyElementsError

# this class taken from useless.base.xmlfile
class ParserHelper(object):
    def _get_single_section(self, element, section):
        sections = element.getElementsByTagName(section)
        if len(sections) > 1:
            raise TooManyElementsError, 'too many %s sections' %section
        else:
            return sections

    def get_elements_from_section(self, element, section, tag, atts=[]):
        sections = self._get_single_section(element, section)
        if len(sections):
            return sections[0].getElementsByTagName(tag)
        else:
            return []

    def get_attribute(self, element, attribute):
        return element.getAttribute(attribute).encode()

    def get_single_element(self, element, tagname):
        elist = self._get_single_section(element, tagname)
        return elist[0]

    # eclass should be subclass of BaseTextElement
    # eclass should have single argument of textdata
    def get_text_element(self, eclass, tagname, element):
        txt_element = self.get_single_element(element, tagname)
        # pass an empty string to new_element
        new_element = eclass('')
        new_element.reform(txt_element)
        return new_element
        
# this class taken from useless.xmlgen.base
class BaseElement(Element):
    def __init__(self, tagname, **atts):
        Element.__init__(self, tagname)
        self.setAttributes(**atts)
        
    def setAttributes(self, **atts):
        for k,v in atts.items():
            if k == 'class_':
                self.setAttribute('class', str(v))
            else:
                self.setAttribute(k, str(v))

# this class modified from useless.base.xmlfile TextElement
class BaseTextElement(BaseElement):
    def __init__(self, name, text, **atts):
        BaseElement.__init__(self, name, **atts)
        self.set(text)

    def set(self, text):
        while self.hasChildNodes():
            del self.childNodes[0]
        if text is not None:
            textnode = Text()
            textnode.data = text
            self.appendChild(textnode)

    def get(self):
        if self.hasChildNodes():
            return self.firstChild.data.encode().strip()
        else:
            return ''

    # this method is used to "reform" a parsed element
    # so we can use get, set on the parsed element
    def reform(self, element):
        name = element.tagName.encode()
        if element.hasChildNodes():
            try:
                value = element.firstChild.data.encode()
            except AttributeError:
                value = None
        else:
            value = None
        atts = {}
        for att in dict(element.attributes):
            atts[att.encode()] = element.getAttribute(att).encode()
        BaseTextElement.__init__(self, name, value, **atts)

class DescriptionElement(BaseTextElement):
    def __init__(self, text):
        BaseTextElement.__init__(self, 'description', text)

class FullNameElement(BaseTextElement):
    def __init__(self, fullname):
        BaseTextElement.__init__(self, 'fullname', fullname)

class LaunchCmdElement(BaseTextElement):
    def __init__(self, launchcmd):
        BaseTextElement.__init__(self, 'launchcmd', launchcmd)

class DosboxPathElement(BaseTextElement):
    def __init__(self, path):
        BaseTextElement.__init__(self, 'dosboxpath', path)

class WeblinkSectionElement(BaseElement):
    def __init__(self):
        BaseElement.__init__(self, 'weblinks')
        
class WeblinkElement(BaseTextElement):
    def __init__(self, site, url):
        BaseTextElement.__init__(self, 'weblink', url, site=site)
        
class GameElement(BaseElement):
    def __init__(self, gamedata):
        name = gamedata['name']
        BaseElement.__init__(self, 'game', **dict(name=name))
        self.appendChild(FullNameElement(gamedata['fullname']))
        self.appendChild(DosboxPathElement(gamedata['dosboxpath']))
        self.appendChild(LaunchCmdElement(gamedata['launchcmd']))
        self.appendChild(DescriptionElement(gamedata['description']))
        weblink_section = WeblinkSectionElement()
        self.appendChild(weblink_section)
        # this if statement should be removed later
        # once it's determined to be unnecessary
        if gamedata.has_key('weblinks'):
            weblinks = gamedata['weblinks']
            for site in weblinks:
                weblink_section.appendChild(WeblinkElement(site, weblinks[site]))

class GameElementParser(ParserHelper):
    def __init__(self, parsed_xml):
        self.game_element = self.get_single_element(parsed_xml, 'game')
        element = self.game_element
        self.name = self.get_attribute(self.game_element, 'name')
        self.elements = {}
        self.elements['fullname'] = self.get_text_element(FullNameElement,
                                                          'fullname', element)
        self.elements['description'] = self.get_text_element(DescriptionElement,
                                                             'description', element)
        self.elements['launchcmd'] = self.get_text_element(LaunchCmdElement,
                                                           'launchcmd', element)
        self.elements['dosboxpath'] = self.get_text_element(DosboxPathElement,
                                                            'dosboxpath', element)
        # this should be a list, possibly empty
        self.elements['weblinks'] = []
        for e in self.get_elements_from_section(element, 'weblinks', 'weblink'):
            wl = WeblinkElement('', '')
            wl.reform(e)
            self.elements['weblinks'].append(wl)
            
    def get_gamedata(self):
        gamedata = {}
        gamedata['name'] = self.name
        for key in ['fullname', 'description', 'launchcmd', 'dosboxpath']:
            gamedata[key] = self.elements[key].get()
        gamedata['weblinks'] = {}
        for element in self.elements['weblinks']:
            site = element.getAttribute('site')
            url = element.get()
            gamedata['weblinks'][site] = url
        return gamedata

class GameDataHandler(object):
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
    
        
if __name__ == '__main__':
    #xfile = file('amazon.xml')
    gdh = GameDataHandler('.')
    pp = gdh.get_game_data('bat')
