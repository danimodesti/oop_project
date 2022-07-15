#
# Ana Cristina Silva de Oliveira — 11965630
# Danielle Modesti — 12543544
# Laura Ferré Scotelari — 12543436
# Rebeca Vieira Carvalho — 12543530
# 
# POO — 3o semestre — Professor Delamaro
# 
# Projeto Final - POO

class movie():

    def __init__(self, id, name, director, actor, supporting, genre, year, imdbScore, imgName):
        self.id = id
        self.name = name
        self.director = director
        self.actor = actor
        self.supporting = supporting
        self.year = year
        self.genre = genre
        self.imdbScore = imdbScore
        self.imgName = imgName
        
    def __str__(self):
        string = "\n\tName: "+ str(self.name) + "\n\tDirector: "+str(self.director) +"\n\t"
        string += "Actor: " + str(self.actor) + "\n\tSupporting: " + str(self.supporting) +"\n\t"
        string += "Release year: " + str(self.year) + "\n\tGenre: " + str(self.genre) +"\n\t"
        string += "IMDB Score: " + str(self.imdbScore) + "\n\tImg name: " + str(self.imgName) +"\n"
        return  string