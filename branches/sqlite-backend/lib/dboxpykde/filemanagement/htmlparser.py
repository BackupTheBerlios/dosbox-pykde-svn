import os, sys
from sgmllib import SGMLParser
import re

from dboxpykde.path import path


class BaseParser(SGMLParser):
    def __init__(self, verbose=0):
        SGMLParser.__init__(self, verbose)
        self._data = ''
        self._write_data = False
        
    def handle_data(self, data):
        if self._write_data:
            self._data += data
            if not self.literal:
                self._write_data = False
        else:
            return SGMLParser.handle_data(self, data)
            
    def _clear_data(self):
        self._data = ''

class AbandonDownloadParser(BaseParser):
    def __init__(self, verbose=0):
        BaseParser.__init__(self, verbose=verbose)
        self.download_link = None
        
    def start_a(self, attributes):
        attributes = dict(attributes)
        if 'http://files.abandonia.com/ramdisk/' in attributes['href']:
            self.download_link = attributes['href']

class AbandonSearchParser(BaseParser):
    def clear_data(self):
        self.clear_gamedata()
        self._clear_state_data()
        
    def clear_gamedata(self):
        self.results = None
        
    def _clear_state_data(self):
        # state markers
        pass
        
    def feed(self, data):
        #self.clear_data()
        #d = re.compile('<div class="game_description">.+?</div>', re.DOTALL)   
        #self.desc = d.findall(data)[0].replace('\n', '')
        BaseParser.feed(self, data)



class AbandonGameParser(BaseParser):
    def __init__(self, verbose=0):
        BaseParser.__init__(self, verbose=verbose)
        self.clear_data()

    def clear_data(self):
        self.clear_gamedata()
        self._clear_state_data()
        
    def clear_gamedata(self):
        self.download_link = None
        self.real_download_link = None
        self.files = []
        self.desc = ''
        self.title = ''
        self.smallinfo = {}
        self.gameid = None
        
    def _clear_state_data(self):
        # state markers
        self._reached_desc_div = False
        self._in_title_div = False
        self._in_smallinfo = False
        self._in_smallinfo_title = False
        self._in_smallinfo_ans = False
        
    def start_a(self, attributes):
        if self._write_data and self.literal:
            self._data += '<a>'
            return 
        attributes = dict(attributes)
        if '/downloadgame/' in attributes['href']:
            self.download_link = attributes['href']
            print 'self.download_link', self.download_link
            self.gameid = int(os.path.basename(self.download_link))
            print self.gameid
        if '/files/extras/' in attributes['href']:
            self.files.append(path(attributes['href']))

    def start_div(self, attributes):
        attributes = dict(attributes)
        if self._in_smallinfo:
            self._smallinfo_divcount += 1
        if attributes.has_key('class'):
            Class = attributes['class']
            if Class == 'title_black':
                print 'in title div'
                self._write_data = True
                self._in_title_div = True
            elif Class == 'game_smallinformation':
                self._in_smallinfo = True
                self._smallinfo_divcount = 0
            elif Class == 'game_smallinformation_title':
                self._write_data = True
                self._in_smallinfo_title = True
            elif Class == 'game_smallinformation_answer':
                self._write_data = True
                self._in_smallinfo_ans = True
                
    def end_div(self):
        if self._in_title_div:
            print 'done with title'
            self.title = self._data
            self._write_data = False
            self._in_title_div = False
            self._clear_data()
        if self._in_smallinfo:
            self._smallinfo_divcount -= 1

        if self._in_smallinfo_title:
            data = self._data.strip()
            if data.endswith(':'):
                data = data[:-1]
            data = data.lower()
            if data:
                self._current_label = data
            self._clear_data()
            self._write_data = False
            self._in_smallinfo_title = False
            
        if self._in_smallinfo_ans:
            data = self._data.strip()
            if data:
                self.smallinfo[self._current_label] = data
            self._clear_data()
            self._write_data = False
            self._in_smallinfo_ans = False
            
    def feed(self, data):
        self.clear_data()
        d = re.compile('<div class="game_description">.+?</div>', re.DOTALL)   
        self.desc = d.findall(data)[0].replace('\n', '')
        BaseParser.feed(self, data)

    
if __name__ == '__main__':
    pass
