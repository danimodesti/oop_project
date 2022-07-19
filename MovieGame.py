#
# Ana Cristina Silva de Oliveira — 11965630
# Danielle Modesti — 12543544
# Laura Ferré Scotelari — 12543436
# Rebeca Vieira Carvalho — 12543530
# 
# POO — 3o semestre — Professor Delamaro
# 
# Projeto Final - POO

class Movie():

    def __init__(self, id, name, director, actor, supporting, genre, year, imdbScore, imgName, 
                                                    curiosity, runTime, rating, oscar, level):
        self.id = id
        self.name = name
        self.director = director
        self.actor = actor
        self.supporting = supporting
        self.year = year
        self.genre = genre
        self.imdbScore = imdbScore
        self.imgName = imgName
        self.supporting = supporting
        self.curiosity = curiosity
        self.runTime = runTime
        self.rating = rating
        self.oscar = oscar
        self.level = level

    def getLevel(self):
        return self.level
    
    def getId(self):
        return self.id

    def getYear(self):
        return self.year

    def getGenre(self):
        return self.genre

    def getSupporting(self):
        return self.supporting

    def getActor(self):
        return self.actor

    def getimdbScore(self):
        return self.imdbScore

    def getDirector(self):
        return self.director
        
    def getCuriosity(self):
        return self.curiosity

    def getRating(self):
        return self.rating

    def getOscar(self):
        return self.oscar

    def getRunTime(self):
        return self.runTime
        
    def __str__(self):
        string = "\n\tName: "+ str(self.name) + "\n\tDirector: "+str(self.director) +"\n\t"
        string += "Actor: " + str(self.actor) + "\n\tSupporting: " + str(self.supporting) +"\n\t"
        string += "Release year: " + str(self.year) + "\n\tGenre: " + str(self.genre) +"\n\t"
        string += "IMDB Score: " + str(self.imdbScore) + "\n\tImg name: " + str(self.imgName) +"\n\t"
        string += "Curiosity: " + str(self.curiosity) + "\n\trunTime: " + str(self.runTime) +"\n\t"
        string += "rating: " + str(self.rating) + "\n\tOscar: " + str(self.oscar) +"\n\t"
        string += "level: " + str(self.level) + "\n\t"
        
        return  string
