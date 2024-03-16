class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.own=[]
        self.taken=[]
        self.king = True

#Getter
    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_own(self):
        return self.own

    def get_taken(self):
        return self.taken

    def get_king(self):
        return self.king

#Setter
    def set_own(self, own):
        self.own = own

    def set_taken(self, taken):
        self.taken = taken

    def set_king(self, king):
        self.king = king

    def __str__(self):
        return f"Name: {self.name}, Color: {self.color}, Own: {self.own}, Taken: {self.taken}, King: {self.king}"
    
# Remove
    def remove_chess(self,chess):
        self.own.remove(chess)
        self.taken.append(chess)