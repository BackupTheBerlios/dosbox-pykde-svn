import os
import urllib2

from dboxpykde.path import path

from htmlparser import AbandonGameParser
from htmlparser import AbandonDownloadParser


UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
Charset = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
Mimes = 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'
Language = 'en-us,en;q=0.5'

class BaseHttpHandler(object):
    def __init__(self):
        self.cookies = urllib2.HTTPCookieProcessor()
        self.proxy = urllib2.ProxyHandler()
        self._install_handlers()

    def _install_handlers(self):
        install = urllib2.install_opener
        build = urllib2.build_opener
        install(build(self.proxy))
        install(build(self.cookies))

    # taken from youtube-dl
    def make_request(self, url, data=None):
        request = urllib2.Request(url)
        if data is not None:
            request.add_data(data)
        request.add_header('User-Agent', UserAgent)
        request.add_header('Accept-Charset', Charset)
        request.add_header('Accept', Mimes)
        request.add_header('Accept-Language', Language)
        return request

    def perform_request(self, url, data=None):
        request = self.make_request(url, data=data)
        response = urllib2.urlopen(request)
        return response

        
class AbandonGamesHandler(BaseHttpHandler):
    def __init__(self, app):
        BaseHttpHandler.__init__(self)
        self.app = app
        self.parser = AbandonGameParser()
        self._base_url = 'http://www.abandonia.com'
        self._cachedir = self.app.datadir / 'cache'
        self._htmldir = self._cachedir / 'html'
        self._gamedir = self._cachedir / 'games'
        self._extrasdir = self._cachedir / 'extras'
        for adir in [self._htmldir, self._gamedir, self._extrasdir]:
            if not adir.exists():
                adir.mkdir()

    def get_game_id(self, url):
        return int(url.split('/en/games/')[1].split('/')[0])


    def _htmlfilename(self, gameid):
        fname = 'game-%d.html' % gameid
        return self._htmldir / fname

    def is_game_downloaded(self, gameid):
        fname = path('%s-nogame' % self._htmlfilename(gameid))
        if fname.exists():
            return False
        else:
            return True


    def game_download_path(self, filename):
        return self._gamedir / filename

    def does_download_exist(self, filename):
        game = self.game_download_path(filename)
        return game.exists()
    
    def set_game_downloaded(self, gameid):
        fname = path('%s-nogame' % self._htmlfilename(gameid))
        os.remove(fname)

    def extras_path(self, filename=''):
        return self._extrasdir / filename
    
    def is_extra_downloaded(self, filename):
        epath = self.extras_path(filename=filename)
        return epath.exists()
    
    def get_game_data(self, gameid):
        self.parser.clear_data()
        print gameid, type(gameid), 'in get_game_data'
        self.parser.gameid = gameid
        data = file(self._htmlfilename(gameid)).read()
        self.parser.feed(data)
        self.parser.gameid = gameid

    def _get_html_file(self, url, filename):
        data = self.perform_request(url).read()
        if data:
            outfile = file(filename, 'w')
            outfile.write(data)
            outfile.close()
        else:
            raise ValueError, "empty data for %s" % url
        
    def handle_url(self, url):
        gameid = self.get_game_id(url)
        html = self._htmlfilename(gameid)
        data = ''
        if not html.exists():
            self._get_html_file(url, html)
            dl = '%s-nogame' % html
            # make an empty file that will be removed
            # when game is downloaded
            file(dl, 'w')
        self.get_game_data(gameid)
        
        
    def get_dl_link(self):
        print self._base_url, self.parser.download_link
        dl_link = self._base_url + self.parser.download_link
        print dl_link
        response = self.perform_request(dl_link)
        self._dlr = response.read()
        parser = AbandonDownloadParser()
        parser.feed(str(self._dlr))
        self.real_download_link = parser.download_link

    def search_for_game(self, text):
        # replace spaces with +'s
        search_term = '+'.join(text.split())
        search_url = '%s/en/search_abandonia/%s' % (self._base_url, search_term)
        response = self.perform_request(search_url)
        

    def get_all_html_ids(self):
        ls = self._htmldir.files('game-*.html')
        gameids = []
        for f in ls:
            gameid = int(f.split('game-')[1].split('.')[0])
            gameids.append(gameid)
        gameids.sort()
        return gameids
    
    
        
if __name__ == '__main__':
    m = AbandonGameParser()
    w = file('dunetest.html').read()
    
    m.feed(w)
    h = AbandonGamesHandler()
    u = 'http://www.abandonia.com/en/games/383'
    u = 'http://www.abandonia.com/en/games/593/'
    
