#
# Ana Cristina Silva de Oliveira — 11965630
# Danielle Modesti — 12543544
# Laura Ferré Scotelari — 12543436
# Rebeca Vieira Carvalho — 12543530
# 
# POO — 3o semestre — Professor Delamaro
# 
# Projeto Final - POO

class user():
    def __init__(self, name):
        self.name = name
        self.level = 0
        self.totalScore = 0
    
    def getName(self):
        return self.name
    
    def getLevel(self):
        return self.level