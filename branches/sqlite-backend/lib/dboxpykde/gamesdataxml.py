import os

from xml.dom.minidom import Element, Text
from xml.dom.minidom import parse as parse_file
from xml.dom.minidom import parseString as parse_string

from base import ExistsError
from base import TooManyElementsError

from basexml import ParserHelper
from basexml import BaseElement
from basexml import BaseTextElement

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

if __name__ == '__main__':
    pass
