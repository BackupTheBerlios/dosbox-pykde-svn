from kdeui import KProgressDialog

from base import get_application_pointer

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
        

# make a progress dialog for operations spanning
# multiple games
class MultiGameProgressDialog(BaseProgressDialog):
    def set_label(self, game):
        message = '%s game <b>%s</b>' % (self.game_action, game)
        self.setLabel(message)
    


if __name__ == '__main__':
    print "testing module"
    
