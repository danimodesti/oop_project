#
# Ana Cristina Silva de Oliveira — 11965630
# Danielle Modesti — 12543544
# Laura Ferré Scotelari — 12543436
# Rebeca Vieira Carvalho — 12543530
#
# POO — 3o semestre — Professor Delamaro
#
# Projeto Final - POO
from math import ceil, floor
import random
from MovieGame import *
import textwrap

# from oop_project.MovieGame import Movie

# Classe tabuleiro contem os filmes de cada rodada
# e o filme sorteado para ser encontrado
# Gerencia as dicas e a interface grafica da pagina


class Gameboard():

    def __init__(self, score, allMovies, numMovies, level):
        self.matchMovies = self.drawMovies(allMovies, numMovies, level)
        self.numMovies = numMovies
        self.score = score
        self.selectedMovie = ""
        self.hints = list()
        self.hintIndex = -1

    def increaseScore(self, value):
        self.score += value

    def winScore(self, value):
        self.score = ceil(self.score * value)

    def penaltyScore(self, value):
        self.score = floor(self.score * value)
        if self.score <= 0:
            self.score = 0
            return 0
        return self.score

    def decreaseScore(self, value):
        self.score -= value
        if self.score <= 0:
            self.score = 0
            return 0
        return self.score

    def getScore(self):
        return int(self.score)

    def getNumMovies(self):
        return self.numMovies

    def getSelectedMovie(self):
        return self.selectedMovie
    
    def getIdSelectedMovie(self):
        return int(self.selectedMovie.getId())

    # Seleciona os
    def drawMovies(self, allMovies, numMovies, level):
        match = list()
        try:
            random.shuffle(allMovies)
            for i in range(len(allMovies)):
                if type(allMovies[i]) is Movie:
                    # Seleciona os filmes com o nivel especificado de acordo com a quantidade de filmes
                    if allMovies[i].getLevel() == level and len(match) < numMovies:
                        match.append(allMovies[i])
            random.shuffle(match)
        except:
            print("Erro em sortear filmes")

        return match
    
    def shuffleMovies(self):
        random.shuffle(self.matchMovies)

    def showMovies(self):
        print("Printando FILMES ------------------------------------------")
        for i in range(len(self.matchMovies)):
            print(self.matchMovies[i])

    def drawSelectedMovie(self):
        # sorteando um filme e retirando ele da lista
        try:
            random.shuffle(self.matchMovies)
            self.selectedMovie = self.matchMovies[0]
            # print(type(self.matchMovies[0]))
            # está dando ruim aq
            # print("<FILME SELECIONADO> ", self.selectedMovie)
            # self.getSelectedMovie(self.selectedMovie)
            # self.getIdSelectedMovie()
        except:
            print("Nao foi possivel selecionar um filme!")

    def loadImagesAndNames(self, images, names):
        for i in range(len(self.matchMovies)):
            # pegando os nomes das imagens
            images.append(
                [self.matchMovies[i].id, f'./imagens/{self.matchMovies[i].imgName}'])

            # pegando os nomes dos filmes e adicionando quebra de linha
            namePieces = textwrap.wrap(self.matchMovies[i].name, 20)
            for i in range(len(namePieces) - 1):
                namePieces[0] = namePieces[i] + "\n" + namePieces[i+1]

            # adicionando os nomes com quebra de linha na lista de nomes
            names.append(namePieces[0])
            
    def newHint(self, possibleHints):
        # caso todas as dicas ja tenham sido mostradas
        if len(possibleHints) == 0:
            return "Não há mais dicas!"

        # sorteando uma dica e retirando ela da lista
        random.shuffle(possibleHints)
        x = possibleHints.pop()

        # dicas
        if x == 1:
            hint = self.selectedMovie.getDirector()
            hint += " dirigiu esse filme."
        elif x == 2:
            hint = "O gênero desse filme e: "
            hint += str(self.selectedMovie.getGenre())
        elif x == 3:
            hint = self.selectedMovie.getActor()
            hint += " estrela esse filme."
        elif x == 4:
            hint = "O coadjuvante e: "
            if type(self.selectedMovie) is Movie:
                hint += self.selectedMovie.getSupporting()
        elif x == 5:
            hint = "O filme foi lançado em: "
            hint += str(self.selectedMovie.getYear())
        elif x == 6:
            hint = "Sua nota no IMDB e: "
            hint += self.selectedMovie.getimdbScore()
        elif x == 7:
            hint = "Curiosidade: "
            hint += self.selectedMovie.getCuriosity()
            if len(hint) > 129:
                # Quebrando linha da curiosidade
                hintPieces = textwrap.wrap(hint, 130)
                hintPieces2 = ""
                for i in range(len(hintPieces) - 1):
                    hintPieces2 += str(hintPieces[i]) + "\n" + str(hintPieces[i+1])
                hint = hintPieces2
        elif x == 8:
            hint = "Duração do filme: "
            hint += self.selectedMovie.getRunTime()
        elif x == 9:
            hint = "Classificação indicativa: "
            hint += self.selectedMovie.getRating()
        elif x == 10:
            hint = "Esse filme "
            if self.selectedMovie.getOscar() == "não":
                hint += self.selectedMovie.getOscar() + " "
            hint += "ganhou um Oscar"

        return hint
    
    def getActualHint(self):
        if self.hintIndex != -1: 
            return self.hints[self.hintIndex]
        return ""

    def drawHints(self, gameModeHint = 0):
        if gameModeHint == 2: possibleHints = [7]
        else: possibleHints = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.hintIndex = 0

        # selecionando uma dica
        self.hints = list()
        while possibleHints:
            self.hints.append(self.newHint(possibleHints))
    
    def nextHint(self):
        if self.hintIndex + 1 < 10: 
            # print("NEXT: ")
            # print(self.hintIndex)
            self.hintIndex += 1 # Adiciona uma posicao na dica
            return self.hints[self.hintIndex]
        return None
    
    def previousHint(self):
        if self.hintIndex - 1 >= 0: 
            # print("PREVIOUS")
            # print(self.hintIndex)
            self.hintIndex -= 1 # Adiciona uma posicao na dica
            return self.hints[self.hintIndex]
        return None            
    