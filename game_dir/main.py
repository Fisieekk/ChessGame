import json
from utils import game as g


quit_option = 0
while not quit_option:
    game = g.Game()
    quit_option = game.main()


def show_json() -> None:
    """
    Show the past games saved in the past_games.json file
    :return:  None
    """
    with open(r"game_dir/utils/past_games.json") as f:
        data = json.load(f)
    print("-" * 30)
    for saved_game in data:
        for key, value in saved_game.items():
            print("{}: {}".format(key, value))
        print("-" * 30)


# show_json()
