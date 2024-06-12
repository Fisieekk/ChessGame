import game_dir.utils.game_files.game as g


quit_option = 0
while not quit_option:
    game = g.Game()
    quit_option = game.main()
