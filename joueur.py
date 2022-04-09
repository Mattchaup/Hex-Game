class Player:
    def __init__(self,name,color,id,temps):
        self.name = name
        self.color = color
        self.id = id
        self.time = temps

    def __str__(self):
        return f"{self.name};{self.color};{self.id};{self.time}"