import os
from qt import SIGNAL, SLOT
from qt import qApp
from qt import QTextBrowser
from qt import QMessageBox
from qt import QFileDialog

#from kdeui import KMessageBox

#from kfile import KFileDialog

#from khtml import KHTMLPart

from base import split_url
from base import opendlg_errormsg
from base import ExistsError

from infodoc import BaseDocument

from gamedata_widgets import EditGameDataDialog
        
# text browser for game info
# uses html
# setSource method handles links, but kde-apidocs
# recommend not using this method
class InfoBrowser(QTextBrowser):
    def __init__(self, parent, name='InfoBrowser'):
        QTextBrowser.__init__(self, parent, name)
        self.app = qApp
        # we need to figure out what to do with setNotifyClick
        #self.setNotifyClick(True)
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
            cmd = self.app.myconfig.get('DEFAULT', 'launch_weblink')
            # for these url's, the name is the site
            weblink_url = gamedata['weblinks'][name]
            if '%s' in cmd:
                os.system(cmd % weblink_url)
            else:
                os.system("%s '%s'" % (cmd, weblink_url))
            # now we reset the name variable to reset the page properly
            name = gamedata['name']
        else:
            QMessageBox.information(self, '%s is unimplemented.' % action)
        # refresh the page
        self.set_game_info(name)
        # need to emit signal here for mainwin to pick up
        # this method is ugly
        if action in ['cleanup', 'prepare', 'edit']:
            mainwin = self.parent().parent()
            mainwin.refreshListView()
            
                        
    def select_title_screenshot(self, name):
        if self.select_title_screenshot_dlg is None:
            file_filter = "*.png|PNG Images\n*|All Files"
            path = self.app.dosbox.get_capture_path(name)
            dlg = QFileDialog(path, file_filter, self, 'select_title_screenshot_dlg', True)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.title_screenshot_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.game_name = name
            dlg.show()
            self.select_title_screenshot_dlg = dlg
        else:
            # we shouldn't need this with a modal dialog
            QMessageBox.information(self, opendlg_errormsg)

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
    
