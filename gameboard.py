#
# Ana Cristina Silva de Oliveira — 11965630
# Danielle Modesti — 12543544
# Laura Ferré Scotelari — 12543436
# Rebeca Vieira Carvalho — 12543530
# 
# POO — 3o semestre — Professor Delamaro
# 
# Projeto Final - POO
import random
from movie import *
import textwrap

# Classe tabuleiro contem os filmes de cada rodada
# e o filme sorteado para ser encontrado
# Gerencia as dicas e a interface grafica da pagina
class gameboard():

    def __init__(self, allMovies, numMovies, level):
        self.matchMovies = self.drawMovies(allMovies, numMovies, level)
        self.numMovies = numMovies
        self.score = 5000
    
    def decreaseScore(self, value):
        self.score -= value
    
    def getScore(self):
        return score

    def getNumMovies(self):
        return self.numMovies

    # Seleciona os 
    def drawMovies(self, allMovies, numMovies, level):
        # print(f"ALLMOVIES: {allMovies} || numMovies: {numMovies} || level: {level}")
        match = list()
        try:
            for i in range(len(allMovies)):
                if type(allMovies[i]) is movie:
                    # Seleciona os filmes com o nivel especificado de acordo com a quantidade de filmes
                    if allMovies[i].getLevel() == level and len(match) < numMovies:
                        match.append(allMovies[i])
            random.shuffle(match)
        except:
            print("Erro em sortear filmes")
        
        return match

    def showMovies(self):
        print("Printando FILMES ------------------------------------------")
        for i in range(len(self.matchMovies)):
            print(self.matchMovies[i])
    
    def drawSelectedMovie(self):
        #sorteando um filme e retirando ele da lista
        try:
            random.shuffle(self.matchMovies)
            self.selectedMovie = self.matchMovies[0]
        except:
            print("Nao foi possivel selecionr um filme!")
    
    def loadImagesAndNames(self, images, names):
        for i in range(len(self.matchMovies)):
            #pegando os nomes das imagens
            images.append([self.matchMovies[i].id, f'./imagens/{self.matchMovies[i].imgName}'])

            #pegando os nomes dos filmes e adicionando quebra de linha
            namePieces = textwrap.wrap(self.matchMovies[i].name,20)
            for i in range(len(namePieces) - 1):
                namePieces[0] = namePieces[i] + "\n" + namePieces[i+1]

            #adicionando os nomes com quebra de linha na lista de nomes
            names.append(namePieces[0])
    
    def getIdSelectedMovie(self):
        return self.selectedMovie.getId()

    def newHint(self, possibleHints):
          #caso todas as dicas ja tenham sido mostradas
        if len(possibleHints) == 0:
            return "Não há mais dicas!"

        #sorteando uma dica e retirando ela da lista
        random.shuffle(possibleHints)
        x = possibleHints.pop()

        #dicas
        if x == 1:
            hint = self.selectedMovie.director
            hint += " dirigiu esse filme."
        elif x == 2:
            hint = "O gênero desse filme e: "
            hint += str(self.selectedMovie.genre)
        elif x == 3:
            hint = self.selectedMovie.actor
            hint += " estrela esse filme."
        elif x == 4:
            hint = "O coadjuvante e: "
            hint += self.selectedMovie.supporting
        elif x == 5:
            hint = "O filme foi lançado em: "
            hint += str(self.selectedMovie.year)
        elif x == 6:
            hint = "Sua nota no IMDB e: "
            hint += self.selectedMovie.imdbScore
        
        return hint

    
