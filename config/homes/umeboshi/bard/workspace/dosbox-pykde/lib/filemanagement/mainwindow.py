import os


# main window class
class MainWindowCommon(object):
    # call this after self.app has been setup
    def _init_common(self):
        self.config = self.app.config
        self.resize(*self.config.get_xy('mainwindow', 'mainwindow_size'))
        # initialize game data
        self.initialize_important_game_data()
        self._treedict = {}
        self._show_filter = 'all'
        # setup default view options
        self.flat_tree_view = self.config.get('mainwindow', 'flat_tree_view')
        self.name_title_view = self.config.get('mainwindow', 'name_title_view')

        # init actions menus toolbar
        self.initActions()
        self.initMenus()
        self.initToolbar()

        # setup dialog pointers
        self.new_game_dir_dialog = None
        self.add_new_game_dlg = None
        
    def initlistView(self):
        # the -1 is to set the column's WidthMode to Maximum instead of Manual
        self.listView.addColumn('games', -1)
        self.refreshListView()

    def initialize_important_game_data(self):
        self.game_titles = {}
        self.game_paths = {}
        handler = self.app.game_datahandler
        self.game_names = handler.get_game_names()
        for game in self.game_names:
            gamedata = handler.get_game_data(game)
            self.game_titles[game] = gamedata['fullname']
            self.game_paths[game] = gamedata['dosboxpath']

    def update_important_game_data(self, name):
        handler = self.app.game_datahandler
        gamedata = handler.get_game_data(name)
        self.game_titles[name] = gamedata['fullname']
        self.game_paths[name] = gamedata['dosboxpath']
        if name not in self.game_names:
            self.game_names.append(name)
            self.game_names.sort()

    def _appendListItem_common(self, parent, name, itemclass):
        if self.name_title_view == 'name':
            item_label = name
        else:
            item_label = self.game_titles[name]
        item = None
        if self._show_filter == 'all':
            item = itemclass(parent, item_label)
        else:
            fhandler = self.app.game_fileshandler
            available = fhandler.get_game_status(name)
            if self._show_filter == 'available':
                if available:
                    item = itemclass(parent, item_label)
            elif self._show_filter == 'unavailable':
                if not available:
                    item = itemclass(parent, item_label)
        if item is not None:
            item.game = name
        
    def refreshListView_common(self, itemclass):
        self.listView.clear()
        # the tree view option may get too long
        # with a large number of games.  I have tried
        # to make this fairly quick for a small number of
        # directories, but a lot of directories will almost
        # surely slow it down.
        if self.flat_tree_view == 'tree':
            self._treedict = {}
            self.listView.setRootIsDecorated(True)
            for name in self.game_names:
                path = self.game_paths[name]
                # basename should always equal name
                # we only need the dirname
                dirname, basename = os.path.split(path)
                # this statement needs fixing for windows
                dirs = dirname.split('/')
                parent = None
                for adir in dirs:
                    if parent is None:
                        if adir not in self._treedict:
                            self._treedict[adir] = itemclass(self.listView, adir)
                            self._treedict[adir].dirname = adir
                        parent = self._treedict[adir]
                    else:
                        path = os.path.join(parent.dirname, adir)
                        if path not in self._treedict:
                            self._treedict[path] = itemclass(parent, adir)
                            self._treedict[path].dirname = path
                        parent = self._treedict[path]
                self._appendListItem(self._treedict[dirname], basename)            
        else:
            self.listView.setRootIsDecorated(False)
            for game in self.game_names:
                self._appendListItem(self.listView, game)
            
    def selectionChanged(self):
        item = self.listView.currentItem()
        if hasattr(item, 'game'):
            self.selectGame(item.game, called_externally=False)

    # if this method is called externally, i.e. through dcop
    # we need to select the KListViewItem that matches also
    # if this method is not called externally, it means that the
    # listitem has already been selected
    def selectGame(self, name, called_externally=True):
        raise NotImplementedError, "selectGame not implemented in common class"
                    
    def initActions(self):
        raise NotImplementedError, "initActions not implemented in common class"
        
    def initMenus(self):
        raise NotImplementedError, "initMenus not implemented in common class"
    
    def initToolbar(self):
        raise NotImplementedError, "initToolbar not implemented in common class"
        
    def slotNewGame(self):
        raise NotImplementedError, "slotNewGame not implemented in common class"

    def destroy_new_game_dir_dlg(self):
        self.new_game_dir_dialog = None

    def destroy_add_new_game_dlg(self):
        self.add_new_game_dlg = None
        
    # new genre probably won't be implemented
    def slotNewGenre(self):
        raise NotImplementedError, "slotNewGenre not implemented in common class"

    def slotLaunchDosbox(self, game=None):
        raise NotImplementedError, "slotLaunchDosbox not implemented in common class"
        
    def select_new_game_path(self):
        raise NotImplementedError, "select_new_game_path not implemented in common class"
            
    def add_new_game_common(self, name, gamedata):
        if name not in self.game_names:
            # add game to data handler
            handler = self.app.game_datahandler
            handler.add_new_game(gamedata)
            # archive as fresh install
            filehandler = self.app.game_fileshandler
            filehandler.archive_fresh_install(name)
            # update quick reference dictionaries
            self.update_important_game_data(name)
            # update the list
            self.refreshListView()
            # now we should be done with this dialog
        else:
            self.add_new_game_dlg = None
            raise ExistsError, 'game %s already exists'
        self.add_new_game_dlg = None
        
    def slotFlatView(self):
        self.flat_tree_view = 'flat'
        self.refreshListView()
        
    def slotTreeView(self):
        self.flat_tree_view = 'tree'
        self.refreshListView()
        
    def slotNameView(self):
        self.name_title_view = 'name'
        self.refreshListView()
        
    def slotTitleView(self):
        self.name_title_view = 'title'
        self.refreshListView()

    def _available_games(self):
        fhandler = self.app.game_fileshandler
        return [g for g in self.game_names if fhandler.game_is_available(g)]

    def _unavailable_games(self):
        fhandler = self.app.game_fileshandler
        return [g for g in self.game_names if not fhandler.game_is_available(g)]
    
    def _prepare_games_orig(self, gamelist):
        fhandler = self.app.game_fileshandler
        for game in gamelist:
            fhandler.prepare_game(game)

    def _clean_games_orig(self, gamelist):
        fhandler = self.app.game_fileshandler
        for game in gamelist:
            fhandler.cleanup_game(game)

    def _clean_games(self, gamelist):
        self._perform_multigame_action(gamelist, 'cleanup_game')
        
    def _prepare_games(self, gamelist):
        self._perform_multigame_action(gamelist, 'prepare_game')
        
    # here action is either 'cleanup_game'
    # or 'prepare_game'
    def _perform_multigame_action(self, gamelist, action):
        raise NotImplementedError, "_perform_multigame_action not implemented in common class"
        
    def slotPrepareAllGames(self):
        missing = self._unavailable_games()
        self._prepare_games(missing)

    def slotCleanAllGames(self):
        available = self._available_games()
        self._clean_games(available)

    def slotArchiveAllGames(self):
        available = self._available_games()
        self._clean_games(available)
        self._prepare_games(available)

    def slotFilterAllGames(self):
        self._show_filter = 'all'
        self.refreshListView()
        
    def slotFilterAvailableGames(self):
        self._show_filter = 'available'
        self.refreshListView()

    def slotFilterUnavailableGames(self):
        self._show_filter = 'unavailable'
        self.refreshListView()

if __name__ == '__main__':
    print "testing module"
    
