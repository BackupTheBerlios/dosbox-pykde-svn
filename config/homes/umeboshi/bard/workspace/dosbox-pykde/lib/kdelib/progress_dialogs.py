from kdeui import KProgressDialog

class BaseProgressDialog(KProgressDialog):
    def __init__(self, parent, name='BaseProgressDialog'):
        KProgressDialog.__init__(self, parent, name)

# make a progress dialog for operations spanning
# multiple games
class MultiGameProgressDialog(BaseProgressDialog):
    def set_label(self, game):
        message = '%s game <b>%s</b>' % (self.game_action, game)
        self.setLabel(message)
    


if __name__ == '__main__':
    print "testing module"
    
