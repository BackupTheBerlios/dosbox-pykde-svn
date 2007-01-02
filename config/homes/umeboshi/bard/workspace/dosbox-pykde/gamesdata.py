import os

from xml.dom.ext import PrettyPrint
#from xml.dom.minidom import DOMImplementation, Document
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
            return None

    def reform(self, element):
        name = element.tagName.encode()
        if element.hasChildNodes():
            try:
                value = element.firstChild.data.encode()
            except AttributeError:
                value = None
        else:
            value = None
        BaseTextElement.__init__(self, name, value)

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
        
class GameElement(BaseElement):
    def __init__(self, gamedata):
        name = gamedata['name']
        BaseElement.__init__(self, 'game', **dict(name=name))
        self.appendChild(FullNameElement(gamedata['fullname']))
        self.appendChild(DosboxPathElement(gamedata['dosboxpath']))
        self.appendChild(LaunchCmdElement(gamedata['launchcmd']))
        self.appendChild(DescriptionElement(gamedata['description']))
        

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

    def get_gamedata(self):
        gamedata = {}
        gamedata['name'] = self.name
        for key in ['fullname', 'description', 'launchcmd', 'dosboxpath']:
            gamedata[key] = self.elements[key].get()
        return gamedata
    
class GameDataHandler(object):
    def __init__(self, directories):
        self.directories = directories
        self.gamedata_dir = directories['games']

    def _gamedatafilename(self, name):
        return os.path.join(self.gamedata_dir, '%s.xml' % name)

    def _make_xmlfile(self, gamedata, filename):
        element = GameElement(gamedata)
        gamedatafile = file(filename, 'w')
        element.writexml(gamedatafile)
        
    def add_new_game(self, gamedata):
        gamedatafilename = self._gamedatafilename(gamedata['name'])
        if os.path.exists(gamedatafilename):
            raise ExistsError, "%s already exists. can't add as new." % gamedatafilename
        else:
            self._make_xmlfile(gamedata, gamedatafilename)
        
    def get_game_names(self):
        ls = os.listdir(self.gamedata_dir)
        games = [x[:-4] for x in ls if x.endswith('.xml')]
        return games

    def get_game_data(self, name):
        gamedatafilename = self._gamedatafilename(name)
        parsed_element = parse_file(file(gamedatafilename))
        parser = GameElementParser(parsed_element)
        return parser.get_gamedata()

    def update_game_data(self, gamedata):
        filename = self._gamedatafilename(gamedata['name'])
        self._make_xmlfile(gamedata, filename)

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
    xfile = file('amazon.xml')
    gdh = GameDataHandler('.')
    pp = gdh.get_game_data('bat')
