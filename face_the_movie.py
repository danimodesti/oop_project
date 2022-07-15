from webbrowser import BackgroundBrowser
from PySimpleGUI import PySimpleGUI as sg
from movie import *
from read_csv import *
import random
import textwrap
import cv2
from PIL import Image, ImageTk
import re


# Layout 
# sg.theme('DarkBlue')
font = ("Dimitri Swank", 40)
fontHint = ("Dimitri Swank", 15)
fontName = ("Dimitri Swank", 10)
font_button = ("Dimitri", 20)
movies = []

# Elementos graficos ----------------
title = [
    [sg.Text('FACE', text_color=('white'), key='-text-', font=font)],
    [sg.Text('THE', text_color=('white'),key='-text-', font=font)],
    [sg.Text('MOVIE', text_color=('white'),key='-text-', font=font)]
]

buttons = [
    [sg.Button('Jogar', button_color=('white', sg.theme_background_color()), font=font_button, border_width = 0)],
    [sg.Button('Sair', button_color=('white', sg.theme_background_color()), font=font_button, border_width = 0)]
]

buttonNextHint = [
    [sg.Button('Proxima Dica', button_color=('white', sg.theme_background_color()), font=font_button, border_width = 0)]
]

Layout = [
    [sg.VPush()],
    [sg.Column(title) , sg.Column(buttons)],
    [sg.VPush()]
]
# ----------------------------------

class FaceTheMovie:
   
    def __init__(self):
        
        # Janela
        janela = sg.Window('Face the Movie', Layout, size=(600,300), element_justification = 'c', use_default_focus=False)
        # Ler os eventos
        while True:
            eventos, valores = janela.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Jogar':
                janela.close()
                print('JOGO AQUI')
                
                #Criando um novo jogo
                self.newGame()

            if eventos == 'Sair' :
                break

    def newGame(self):
        #preencher lista de filmes com as informações do .csv
        readCSV(movies)

        #Teste - printando os filmes lidos 
        print("Printando filmes ------------------------------------------")
        for i in range(len(movies)):
            print(movies[i])

        self.newPhase()

    def newPhase(self):

        #preparando o ambiente grafico ----------------

        #lista com nomes das imagens e dos filmes que serao as alternativas
        self.images = []
        self.names = []

        for i in range(len(movies)):
            #pegando os nomes das imagens
            self.images.append(f'./imagens/{movies[i].imgName}')

            #pegando os nomes dos filmes e adicionando quebra de linha
            namePieces = textwrap.wrap(movies[i].name,20)
            for i in range(len(namePieces) - 1):
                namePieces[0] = namePieces[i] + "\n" + namePieces[i+1]

            #adicionando os nomes com quebra de linha na lista de nomes
            self.names.append(namePieces[0])
        #-----------------------------------------------
        
        try:
            #adicionando as imagens na tela
            imgLayouts = []

            for i in range(10):
                #definindo as 'keys' das imagens e dos botoes
                imgKey = "-img" + str(i) + "-"
                btnKey = "-btnDesc"+ str(i) + "-"

                #chamando a funcao de criacao de layout e adicionando na lista de layouts
                imgLayouts.append(self.makeImageLayout(self.images[i], imgKey, self.names[i], btnKey))

        except:
            print("Não foi possível encontrar as imagens!")

        # sorteando um filme para ser adivinhado
        selectedMovie = self.shuffleMovies()
        possibleHints = [1, 2, 3, 4, 5, 6]

        # selecionando uma dica
        hint = self.newHint(selectedMovie, possibleHints)
        
        #layout da pagina
        Layout2 = [
            #Elementos da pagina
            [sg.Text('PREPARAR', key='-text-', font=font)],
            [sg.Text(hint, key='-textHint-', font=fontHint)],
            [sg.Column(imgLayouts[0]) , sg.Column(imgLayouts[1]), sg.Column(imgLayouts[2]), sg.Column(imgLayouts[3]), sg.Column(imgLayouts[4])],
            [sg.Column(imgLayouts[5]) , sg.Column(imgLayouts[6]), sg.Column(imgLayouts[7]), sg.Column(imgLayouts[8]), sg.Column(imgLayouts[9])],
            [sg.Column(buttonNextHint)]
        ]

        #abrindo uma nova janela
        janela = sg.Window('OPA', Layout2, size=(900,700), element_justification = 'c', use_default_focus=False)

        # Ler os eventos
        while True:
            eventos, valores = janela.read()
            #Fechando o programa
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Proxima Dica':
                # selecionando uma nova dica
                hint = self.newHint(selectedMovie, possibleHints)
                #atualizando o elemento texto que representa a dica
                janela.Element('-textHint-').update(hint)
                
            if eventos.startswith('-btnDesc'):
                
                #verificando qual e o numero da alternativa que foi selecionada
                numImg = re.sub("[^0-9]", "", eventos)
                #descolorindo a imagem referente a alternativa selecionada
                imgGray = self.decolorizeImage(self.images[int(numImg)])

                #determinando qual sera o nome da imagem
                imgName = "-img" + numImg + "-"

                #atualizando a imagem do layout para a imagem em preto e branco
                janela[imgName].update(data = imgGray)


    def shuffleMovies(self):
        #sorteando um filme e retirando ele da lista
        try:
            random.shuffle(movies)
            return movies.pop()
        except:
            print("Nao foi possivel selecionr um filme!")

        

    def newHint(self, selectedMovie, possibleHints):

        #caso todas as dicas ja tenham sido mostradas
        if len(possibleHints) == 0:
            return "Não há mais dicas!"

        #sorteando uma dica e retirando ela da lista
        random.shuffle(possibleHints)
        x = possibleHints.pop()

        #dicas
        if x == 1:
            hint = selectedMovie.director
            hint += " dirigiu esse filme."
        elif x == 2:
            hint = "O gênero desse filme e: "
            hint += str(selectedMovie.genre)
        elif x == 3:
            hint = selectedMovie.actor
            hint += " estrela esse filme."
        elif x == 4:
            hint = "O coadjuvante e: "
            hint += selectedMovie.supporting
        elif x == 5:
            hint = "O filme foi lançado em: "
            hint += str(selectedMovie.year)
        elif x == 6:
            hint = "Sua nota no IMDB e: "
            hint += selectedMovie.imdbScore
        
        return hint

    def decolorizeImage(self, imgName):

        #lendo imagem original
        originalImg = cv2.imread(imgName)
        #convertendo a cor
        imgGray = cv2.cvtColor(originalImg, cv2.COLOR_BGR2GRAY)

        #convertendo o formato da imagem
        data = Image.fromarray(imgGray)
        image = ImageTk.PhotoImage(image=data)

        return image


    def makeImageLayout(self, nameImg, imgKey, nameMovie, btnKey ):

        # ------------------- Layout Definition -------------------
        imgLayout = [[sg.Image(nameImg, key=imgKey)],
                    [sg.Text(nameMovie, text_color=('white'), font=fontName)],
                    [sg.Button('Descartar', key=btnKey, button_color=('white', sg.theme_background_color()), font=fontHint, border_width = 0)]]

        # ------------------- Window Creation -------------------
        return imgLayout

