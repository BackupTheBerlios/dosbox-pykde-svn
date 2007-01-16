import os
from qt import SIGNAL, SLOT
from qt import PYSIGNAL
from qt import QString

from kdecore import KApplication


from kdeui import KTextBrowser
from kdeui import KMessageBox

from kfile import KFileDialog

from khtml import KHTMLPart

from dboxpykde.base import split_url
from dboxpykde.base import opendlg_errormsg
from dboxpykde.base import ExistsError

from dboxpykde.infodoc import BaseDocument

from gamedata_widgets import EditGameDataDialog

# would like to use this class, but don't
# understand how to connect url clicks
class InfoPart(KHTMLPart):
    def __init__(self, parent, name='InfoPart'):
        KHTMLPart.__init__(self, parent, name)
        # setup app pointer
        self.app = KApplication.kApplication()
        self.doc = BaseDocument(self.app)
        self.connect(self, SIGNAL('onURL(QString)'), self.setSource)
        #self.connect(self, SIGNAL('urlSelected(QString)'), self.setSource)
                
    def set_game_info(self, name):
        self.begin()
        self.doc.set_info(name)
        self.write(self.doc.output())
        self.end()

    def setSource(self, *args):
        print 'setSource called', args
    # this is selected when a url is clicked
    def setSourceOK(self, url):
        #action, key, filename = split_url(url)
        action, name = split_url(url)
        print action, name
        filehandler = self.app.game_fileshandler
        if action == 'cleanup':
            filehandler.cleanup_game(name)
        elif action == 'prepare':
            filehandler.prepare_game(name)

        self.set_game_info(name)
        
# text browser for game info
# uses html
# setSource method handles links, but kde-apidocs
# recommend not using this method
class InfoBrowser(KTextBrowser):
    def __init__(self, parent, name='InfoBrowser'):
        KTextBrowser.__init__(self, parent, name)
        self.app = KApplication.kApplication()
        self.setNotifyClick(True)
        self.doc = BaseDocument(self.app)
        # setup dialog pointers
        self.select_title_screenshot_dlg = None
        
    def set_game_info(self, name):
        # the following two lines used to work fine
        # but don't now
        #self.doc.set_info(name)
        #self.setText(self.doc.output())
        # so instead we do this quick hack
        # make a new document
        self.doc = BaseDocument(self.app)
        # display empty document
        self.setText(self.doc.output())
        # continue with what used to work
        self.doc.set_info(name)
        self.setText(self.doc.output())
        #self.emit(SIGNAL('sourceChanged(QString)'), (QString(name)))
        self.emit(PYSIGNAL('GameInfoSet'), (name,))
        
    # this is selected when a url is clicked
    def setSource(self, url):
        #action, key, filename = split_url(url)
        action, name = split_url(url)
        filehandler = self.app.game_fileshandler
        if action == 'cleanup':
            filehandler.cleanup_game(name)
        elif action == 'prepare':
            filehandler.prepare_game(name)
        elif action == 'edit':
            dlg = EditGameDataDialog(self, name)
            dlg.show()
        elif action == 'set_title_screenshot':
            self.select_title_screenshot(name)
        elif action == 'open_weblink':
            # get gamedata from doc object
            # to keep from excessive xml parsing
            gamedata = self.doc.gamedata
            cmd = self.app.config.get('DEFAULT', 'launch_weblink')
            # for these url's, the name is the site
            weblink_url = gamedata['weblinks'][name]
            if '%s' in cmd:
                os.system(cmd % weblink_url)
            else:
                os.system("%s '%s'" % (cmd, weblink_url))
            # now we reset the name variable to reset the page properly
            name = gamedata['name']
        else:
            KMessageBox.error(self, '%s is unimplemented.' % action)
        # refresh the page
        self.set_game_info(name)
                        
    def select_title_screenshot(self, name):
        if self.select_title_screenshot_dlg is None:
            file_filter = "*.png|PNG Images\n*|All Files"
            path = self.app.dosbox.get_capture_path(name)
            dlg = KFileDialog(path, file_filter, self, 'select_title_screenshot_dlg', True)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.title_screenshot_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.game_name = name
            dlg.show()
            self.select_title_screenshot_dlg = dlg
        else:
            # we shouldn't need this with a modal dialog
            KMessageBox.error(self, opendlg_errormsg)

    def title_screenshot_selected(self):
        print 'screenshot selected'
        dlg = self.select_title_screenshot_dlg
        url = dlg.selectedURL()
        fullpath = str(url.path())
        print 'screenshot at', fullpath
        name = dlg.game_name
        handler = self.app.game_datahandler
        handler.make_title_screenshot(name, fullpath)
        self.destroy_select_title_screenshot_dlg()
        self.set_game_info(name)
        
    def destroy_select_title_screenshot_dlg(self):
        self.select_title_screenshot_dlg = None
        
if __name__ == '__main__':
    print "testing module"
    
