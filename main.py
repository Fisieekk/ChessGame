import Utils.Controller.Game

# TODO: I found some bugs:
#  Bug with Queen moving despite check is still a issue,
#  Mate isn't calculated properly in some situations
# TODO: UNDO doesn't work yet
# TODO: improve material_diff chart
# Promotion works but GUI is terrible xDDD

game = Utils.Controller.Game.Game()
# game.gb.stalemate_test()
game.main()

