#
# Ana Cristina Silva de Oliveira — 11965630
# Danielle Modesti — 12543544
# Laura Ferré Scotelari — 12543436
# Rebeca Vieira Carvalho — 12543530
# 
# POO — 3o semestre — Professor Delamaro
# 
# Projeto Final - POO
from GameBoard import *

class User():
    def __init__(self, name, totalScore = 0):
        self.name = name
        self.level = 1
        self.totalScore = totalScore
    
    def getName(self):
        return self.name

    def setTotalScore(self, val):
        if val > 0:
            self.totalScore = val
    
    def increaseTotalScore(self, val):
        self.totalScore += val

    def getTotalScore(self):
        return int(self.totalScore)
    
    def getLevel(self):
        return self.level
    
    def increaseLevel(self):
        if self.level + 1 < 4: 
            self.level += 1
        return self.level
    
    def toString(self):
        print(f"NAME: {self.getName()} | TOTAL SCORE: {self.totalScore}")
    
    def __lt__(self, otherUser):
        return self.getTotalScore() < otherUser.getTotalScore()