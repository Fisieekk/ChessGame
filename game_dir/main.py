from utils import game as g


quit_option = 0
while not quit_option:
    game = g.Game()
    quit_option = game.main()
