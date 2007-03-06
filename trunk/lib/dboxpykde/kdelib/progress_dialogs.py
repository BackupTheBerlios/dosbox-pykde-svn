from qt import QWidget
from qt import QLabel
from qt import QGridLayout

from kdeui import KProgressDialog
from kdeui import KProgress

from base import get_application_pointer

from dboxpykde.kdelib.base import BaseDialogWindow

class BaseProgressDialog(KProgressDialog):
    def __init__(self, parent, name='BaseProgressDialog'):
        KProgressDialog.__init__(self, parent, name)
        self.app = get_application_pointer()
        
class ArchiveProgressDialog(BaseProgressDialog):
    def __init__(self, parent, action='extract'):
        BaseProgressDialog.__init__(self, parent, name='ArchiveProgressDialog')
        if action == 'extract':
            self._lbl_msg = 'Extracting %s from archive.'
        else:
            self._lbl_msg = 'Adding %s to archive.'

    def report(self, filename, count, total):
        progress = self.progressBar()
        if self.total is None:
            self.total = total
            progress.setTotalSteps(total)
        self.setLabel(self._lbl_msg % filename)
        progress.setProgress(count)
        self.app.processEvents()
        
class MultiGameProgress(QWidget):
    def __init__(self, parent, action, name='MultiGameProgress'):
        QWidget.__init__(self, parent, name)
        self.app = get_application_pointer()
        self.fhandler = self.app.make_new_fileshandler()
        self.action = action
        self.game_progressBar = KProgress(self)
        self.file_progressBar = KProgress(self)
        self.file_progressBarLbl = QLabel(self)
        self.game_progressBarLbl = QLabel(self)
        self.grid = QGridLayout(self, 4, 1, 5, 7)
        self.grid.addWidget(self.file_progressBarLbl, 0, 0)
        self.grid.addWidget(self.file_progressBar, 1, 0)
        self.grid.addWidget(self.game_progressBarLbl, 2, 0)
        self.grid.addWidget(self.game_progressBar, 3, 0)
        if action == 'prepare_game':
            self.game_action = 'Prepare'
            self.fhandler._report_extract_from_installed_archive = self.report_file_extracted
        else:
            self.game_action = 'Clean up'
            self.fhandler.archivehelper.report_installed_file_handled = self.report_file_handled
        
    def set_game_label(self, game):
        message = '%s game <b>%s</b>' % (self.game_action, game)
        self.game_progressBarLbl.setText(message)
        

    def report_file_handled(self, filename, count):
        msg = 'File %s handled.' % filename
        self.file_progressBarLbl.setText(msg)
        self.file_progressBar.setProgress(count)
        self.app.processEvents()

    def report_file_extracted(self, filenamee, count, total):
        if count == 1:
            self.file_progressBar.setTotalSteps(total)
        msg = '%s extracted.' % filenamee
        self.file_progressBarLbl.setText(msg)
        self.file_progressBar.setProgress(count)
        self.app.processEvents()
        
        
    def report_action_on_game(self, game, title):
        progress = self.game_progressBar.progress()
        print 'game progress', progress
        self.set_game_label(title)
        progress += 1
        self.game_progressBar.setProgress(progress)
        if self.action == 'cleanup_game':
            total = len(self.fhandler.datahandler.get_installed_files(game))
            self.file_progressBar.setTotalSteps(total)
            self.file_progressBar.setProgress(0)
        self.app.processEvents()
        
    def act_on_games(self, gamelist, titles):
        num_games = len(gamelist)
        action_method = getattr(self.fhandler, self.action)
        self.game_progressBar.setTotalSteps(num_games)
        for game in gamelist:
            self.report_action_on_game(game, titles[game])
            action_method(game)
            
# make a progress dialog for operations spanning
# multiple games
class MultiGameProgressDialog(BaseDialogWindow):
    # here the action is either 'cleanup_game' or
    # 'prepare_game'
    def __init__(self, parent, action, name='MultiGameProgressDialog'):
        BaseDialogWindow.__init__(self, parent, name=name)
        self.fhandler = self.app.make_new_fileshandler()
        self.action = action
        self.progress = MultiGameProgress(self, action)
        self.setMainWidget(self.progress)
        
    def perform_action(self, gamelist, titles):
        self.progress.act_on_games(gamelist, titles)
    


if __name__ == '__main__':
    print "testing module"
    
