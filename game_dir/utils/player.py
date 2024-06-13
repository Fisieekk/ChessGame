class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.own = []
        self.taken = []
        self.king = True

    def get_name(self) -> str:
        """
        Get the name of the player
        :return: name of the player
        """
        return self.name

    def get_color(self) -> str:
        """
        Get the color of the player
        :return: color of the player
        """
        return self.color

    def get_own(self):
        """
        Get the own chess of the player
        :return: own chess of the player
        """
        return self.own

    def get_taken(self):
        return self.taken

    def get_king(self):
        return self.king

    def set_own(self, own):
        self.own = own

    def set_taken(self, taken):
        self.taken = taken

    def set_king(self, king):
        self.king = king

    def __str__(self):
        return f"Name: {self.name}, Color: {self.color}, Own: {self.own}, Taken: {self.taken}, King: {self.king}"

    # Remove
    def remove_chess(self, chess):
        self.own.remove(chess)
        self.taken.append(chess)
