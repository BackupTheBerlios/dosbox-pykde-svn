import os
import subprocess

from qt import SIGNAL, SLOT
from qt import PYSIGNAL
from qt import QString
from qt import QWidget

from kdeui import KTextBrowser
from kdeui import KMessageBox

from kfile import KFileDialog

from khtml import KHTMLPart

from dboxpykde.base import split_url
from dboxpykde.base import opendlg_errormsg
from dboxpykde.base import ExistsError

from base import BaseDialogWindow
from base import get_application_pointer

from dboxpykde.infodoc import MainGameInfoDocument

from gamedata_widgets import EditGameDataDialog
from progress_dialogs import BaseProgressDialog


# this ugly critter is a start of an audit game
from qt import QLabel
from kdeui import KProgress
from dboxpykde.infodoc import AuditGameDocument

class AuditGameDialog(BaseDialogWindow):
    def __init__(self, parent, name='AuditGameDialog'):
        BaseDialogWindow.__init__(self, parent, name=name)
        #self.grid = QGridLayout(self, 2, 1, 5, 7)
        self.frame = KTextBrowser(self)
        self.frame.setNotifyClick(True)
        self.frame.setSource = self.setSource
        self.doc = AuditGameDocument(self.app)
        #self.grid.addWidget(self.frame, 0, 0)
        self.progress_label = QLabel(self)
        self.progress = KProgress(self)
        #self.grid.addWidget(self.progress, 1, 0)
        self.setMainWidget(self.frame)
        layout = self.layout()
        # we use insertWidget instead of
        # addWidget here so the widgets
        # are above the dialog buttons
        # self frame should be at 0 index in the layout
        # we set the progress and label below this
        layout.insertWidget(1, self.progress)
        # inserting into index 1 here knocks self.progress down to 2
        layout.insertWidget(1, self.progress_label)
        # disable and hide extra buttons
        self.enableButtonApply(False)
        self.showButtonApply(False)
        self.enableButtonCancel(False)
        self.showButtonCancel(False)
        # the dialog should be a little taller than what
        # it defaults to
        self.resize(0, 300)
        
    def report_md5check(self, filename, count):
        self.progress_label.setText('checking %s' % filename)
        self.progress.setProgress(count)
        self.app.processEvents()
    
    def audit_game(self, name, from_install=True, time='now'):
        filehandler = self.app.make_new_fileshandler()
        total = len(filehandler.datahandler.get_installed_files(name))
        self.progress.setTotalSteps(total)
        filehandler.archivehelper.report_installed_file_handled = self.report_md5check
        unchanged, changed, extra = filehandler.audit_game_files(name,
                                                                 from_install=from_install, time=time)
        self.doc.set_info(unchanged, changed, extra)
        self.frame.setText(self.doc.output())
        self.progress_label.setText('Audit Completed')

    def setSource(self, url):
        print url
        if url == 'show':
            self.doc.append_unchanged_files()
            self.frame.setText(self.doc.output())
        
class InfoBrowserCommon(object):
    def _init_common(self):
        # setup app pointer
        self.app = get_application_pointer()
        self.doc = MainGameInfoDocument(self.app)
        # setup dialog pointers
        self.select_title_screenshot_dlg = None
        self.app.dcop.addMethod('void editGameData (QString)', self.edit_game_data_dialog)
        
    def edit_game_data_dialog(self, name):
        dlg = EditGameDataDialog(self.dialog_parent, name)
        # here we connect the GameDataUpdated signal to the set_game_info method
        dlg.connect(dlg, PYSIGNAL('GameDataUpdated'), self.set_game_info)
        dlg.show()
        
    # this is selected when a url is clicked
    def _perform_url_action(self, url):
        #action, key, filename = split_url(url)
        action, name = split_url(url)
        filehandler = self.app.game_fileshandler
        if action == 'cleanup':
            filehandler.cleanup_game(name)
        elif action == 'backup':
            filehandler.backup_game_files(name)
        elif action == 'prepare':
            self.prepare_game(name)
        elif action == 'prepare-fresh':
            filehandler.prepare_game(name, extras=False)
        elif action == 'audit-install':
            dlg = AuditGameDialog(self.dialog_parent)
            dlg.show()
            self.app.processEvents()
            dlg.audit_game(name, from_install=True)
            #filehandler.audit_game_files(name, from_install=True)
        elif action == 'edit':
            self.edit_game_data_dialog(name)
        elif action == 'set_title_screenshot':
            self.select_title_screenshot(name)
        elif action == 'open_weblink':
            # get gamedata from doc object
            # to keep from excessive xml parsing
            gamedata = self.doc.gamedata
            cmd = self.app.myconfig.get('externalactions', 'launch_weblink')
            # for these url's, the name is the site
            weblink_url = gamedata['weblinks'][name]
            if '%s' in cmd:
                cmd = cmd % weblink_url
            else:
                cmd = "%s '%s'" % (cmd, weblink_url)
            subprocess.call(cmd, shell=True)
            
            # now we reset the name variable to reset the page properly
            name = gamedata['name']
        elif action == 'launch':
            self.app.mainwindow.launchDosboxAction.activate()
            #import pdb
            #pdb.set_trace()
        else:
            KMessageBox.error(self.dialog_parent, '%s is unimplemented.' % action)
        # refresh the page
        self.set_game_info(name)
                        
    def select_title_screenshot(self, name):
        #raise StandardError, 'select_title_screenshot has a few problems.'
        if self.select_title_screenshot_dlg is None:
            file_filter = "*.png|PNG Images\n*|All Files"
            path = self.app.dosbox.get_capture_path(name)
            dlg = KFileDialog(path, file_filter, self.dialog_parent,
                              'select_title_screenshot_dlg', True)
            dlg.connect(dlg, SIGNAL('okClicked()'), self.title_screenshot_selected)
            dlg.connect(dlg, SIGNAL('cancelClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.connect(dlg, SIGNAL('closeClicked()'), self.destroy_select_title_screenshot_dlg)
            dlg.game_name = name
            dlg.show()
            self.select_title_screenshot_dlg = dlg
        else:
            # we shouldn't need this with a modal dialog
            KMessageBox.error(self.dialog_parent, opendlg_errormsg)

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
        #print 'going to set game info to', name
        # the screenshot is not changing automatically here
        # I don't know how to fix this problem
        self.set_game_info(name)
        #print 'game info should be set to', name
        
    def destroy_select_title_screenshot_dlg(self):
        self.select_title_screenshot_dlg = None


    def _report_extract_from_installed_archive(self, filename, count, total):
        dlg = self.extract_from_installed_archive_progress
        progress = dlg.progressBar()
        if dlg.total is None:
            dlg.total = total
            progress.setTotalSteps(total)
        dlg.setLabel('Extracting %s from archive.' % filename)
        progress.setProgress(count)
        self.app.processEvents()
        
    def prepare_game(self, name):
        filehandler = self.app.game_fileshandler
        filehandler._report_extract_from_installed_archive = self._report_extract_from_installed_archive
        dlg = BaseProgressDialog(self.dialog_parent)
        self.extract_from_installed_archive_progress = dlg
        dlg.resize(400, 200)
        dlg.total = None
        dlg.show()
        filehandler.prepare_game(name)
        dlg.close()
        
        

# would like to use this class, but don't
# understand how to connect url clicks
class InfoPart(KHTMLPart, InfoBrowserCommon):
    def __init__(self, parent, name='InfoPart'):
        KHTMLPart.__init__(self, parent, name)
        self._init_common()
        # we need to make a parent for the dialogs
        # the KHTMLPart does not work for this as it
        # is derived from QObject and not QWidget
        self._widget = QWidget(None, 'dialog_parent')
        self.dialog_parent = self._widget
        # start a blank page
        self.begin()
        self.write('')
        self.end()
        
    def set_game_info(self, name):
        self.begin()
        self.write('')
        self.end()
        self.app.processEvents()
        self.begin()
        self.doc.set_info(name)
        self.write(self.doc.output())
        self.end()
        self.emit(PYSIGNAL('GameInfoSet'), (name,))
        print 'game info set to', name
        
    def urlSelected(self, url, button, state, target, args):
        self._perform_url_action(url)
        
# text browser for game info
# uses html
# setSource method handles links, but kde-apidocs
# recommend not using this method
class InfoBrowser(KTextBrowser, InfoBrowserCommon):
    def __init__(self, parent, name='InfoBrowser'):
        KTextBrowser.__init__(self, parent, name)
        self._init_common()
        self.setNotifyClick(True)
        self.dialog_parent = self
        
    def set_game_info(self, name):
        # the following two lines used to work fine
        # but don't now
        #self.doc.set_info(name)
        #self.setText(self.doc.output())
        # so instead we do this quick hack
        # display empty document
        self.setText('')
        # continue with what used to work
        self.doc.set_info(name)
        self.setText(self.doc.output())
        #self.emit(SIGNAL('sourceChanged(QString)'), (QString(name)))
        self.emit(PYSIGNAL('GameInfoSet'), (name,))

    # this is selected when a url is clicked
    def setSource(self, url):
        self._perform_url_action(url)

        
if __name__ == '__main__':
    print "testing module"
    
