class Brain:
    def __init__(self, name, location):
        # parameter name (Str) is the name of the character (is in the disease documentation file with this name)
        # other stuff like the "type" of the character (e.g. Spreader, Diseased) will be implemented in subclasses
        self.name = name
        self.perished = False
        self.square = location # the square object where the Brain currently is at

    def get_name(self):
        return self.name

    def get_perished(self):
        return self.perished

    def move(self, current_square):
        # current_square: A Square object were the Brain is currently at
        # all subclasses will move differently so will be reimplemented
        pass

    def perish(self):
        self.perished = True

