from email.mime import image
from select import select
from webbrowser import BackgroundBrowser
from PySimpleGUI import PySimpleGUI as sg
from movie import *
from user import *
from read_csv import *
from gameboard import *
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
fontButton = ("Dimitri", 20)
fontUserLayout = ("Helvetica", 15)
fontName = ("Helvetica", 12)
movies = []

# Elementos graficos ----------------
title = [
    [sg.Text('FACE', text_color=('white'), key='-text-', font=font)],
    [sg.Text('THE', text_color=('white'),key='-text-', font=font)],
    [sg.Text('MOVIE', text_color=('white'),key='-text-', font=font)]
]

buttons = [
    [sg.Button('Jogar', button_color=('white', sg.theme_background_color()), font=fontButton, border_width = 0)],
    [sg.Button('Ranks', button_color=('white', sg.theme_background_color()), font=fontButton, border_width = 0)],
    [sg.Button('Sair', button_color=('white', sg.theme_background_color()), font=fontButton, border_width = 0)]
]

buttonNextHint = [
    [sg.Button('Proxima Dica', button_color=('white', sg.theme_background_color()), font=fontButton, border_width = 0)]
]

Layout = [
    [sg.VPush()],
    [sg.Column(title) , sg.Column(buttons)],
    [sg.VPush()]
]

UserLayout = [
    [sg.VPush()],
    [sg.Text('Insira aqui seu nome', text_color=('white'), key='-text-', font=fontUserLayout)],
    [sg.InputText()],
    [sg.Button('Entrar', button_color=('white', sg.theme_background_color()), font=fontButton, border_width = 0)],
    [sg.VPush()]
]

RankLayout = [
    [sg.Text('MELHORES PONTUACOES', text_color=('white'), key='-text-', font=font)]
]
# ----------------------------------

class FaceTheMovie:

    allMovies = list()
   
    def __init__(self):
        # Entrada e criacao do objeto User
        windowUser = sg.Window('BEM VINDO', UserLayout, size=(400,200), element_justification = 'c', use_default_focus=False)
        while True:
            eventos, valores = windowUser.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Entrar':
                if valores[0] != '': # Nao aceita nomes nulos

                    userName = valores[0]
                    self.user = user(userName) # Criando o usuario

                    windowUser.close()
                    print(f'USER NAME: {self.user.getName()}')
                
                    #Criando um novo jogo
                    self.mainMenu()

    def mainMenu(self):
        levelNumber = self.user.getLevel()
        level = 'Padrao'
        if levelNumber == 0:
            level = 'Iniciante'

        # Atualiza o menu com o nome do usuario
        NewLayout = [[sg.Text(f'Seu nome para ranks: {self.user.getName()} | Nivel: {level}', text_color=('white'), key='-textName-', font=fontName)]] + Layout
        
        # Janela
        window = sg.Window('Face the Movie', NewLayout, size=(600,300), element_justification = 'c', use_default_focus=False)
        # Ler os eventos
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Jogar':
                window.close()
                print('JOGO AQUI')
                
                #Criando um novo jogo
                self.newGame()

            if eventos == 'Ranks':
                window.close()
                print('RANQ AQUI')
                # Abrindo a lista de Ranks
                self.showRank()

            if eventos == 'Sair' :
                break

    def showRank(self):
        # Ler csv do rank e mostrar na tela
        print("SHoW RaNK")

    def newGame(self):
        #preencher lista de filmes com as informações do .csv
        readCSV(self.allMovies)

        # Teste - printando os filmes lidos 
        print("Printando filmes ------------------------------------------")
        for i in range(len(self.allMovies)):
            print(self.allMovies[i])

        self.newPhase()

    def newPhase(self):
        
        # Cria o gameboard de uma partida
        self.gameboard = gameboard(self.allMovies, 15, self.user.getLevel())
        self.gameboard.showMovies()


        #lista com nomes das imagens e dos filmes que serao as alternativas
        images = []
        names = []

        self.gameboard.loadImagesAndNames(images, names)
        print(f"IMAGES: {len(images)} AND YUP: {names}")
        
        try:
            #adicionando as imagens na tela
            imgLayouts = []

            for i in range(self.gameboard.getNumMovies()):
                #definindo as 'keys' das imagens e dos botoes
                imgKey = "-img" + str(i) + "-"
                btnKey = "-btnDesc"+ str(i) + "-"
                btnGuessKey = "-btnAdv"+ str(i) + "-"
                print(f"IMAGES: {images[i]}, {imgKey}, {names[i]}, {btnKey}")

                #chamando a funcao de criacao de layout e adicionando na lista de layouts
                imgLayouts.append(self.makeImageLayout(images[i], imgKey, names[i], btnKey, btnGuessKey))

        except:
            print("Não foi possível encontrar as imagens!")

        print(len(imgLayouts))

        # sorteando um filme para ser adivinhado
        self.gameboard.drawSelectedMovie()
        possibleHints = [1, 2, 3, 4, 5, 6]

        # selecionando uma dica
        hint = self.gameboard.newHint(possibleHints)
        
        #layout da pagina
        Layout2 = [
            #Elementos da pagina
            [sg.Text('PREPARAR', key='-text-', font=font)],
            [sg.Text(hint, key='-textHint-', font=fontHint)],
        ]

        # Imagens
        line = []

        for i in range(len(imgLayouts)):
            line += [sg.Column(imgLayouts[i]),]
            if i != 0 and i % 7 == 0 :
                Layout2 += [line] 
                line = []

        Layout2 += [[sg.Column(buttonNextHint)]]
        
        #abrindo uma nova janela
        window = sg.Window('GAME', Layout2, element_justification = 'c', use_default_focus=False).Finalize()
        window.Maximize()
        
        # Ler os eventos
        while True:
            eventos, valores = window.read()
            #Fechando o programa
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Proxima Dica':
                # Diminuindo a pontuacao
                self.gameboard.decreaseScore(250)
                # selecionando uma nova dica
                hint = self.gameboard.newHint(possibleHints)
                #atualizando o elemento texto que representa a dica
                window.Element('-textHint-').update(hint)
                
            if eventos.startswith('-btnDesc'):
                
                #verificando qual e o numero da alternativa que foi selecionada
                numImg = re.sub("[^0-9]", "", eventos)

                #descolorindo a imagem referente a alternativa selecionada
                imgGray = self.decolorizeImage(images[int(numImg)])

                #determinando qual sera o nome da imagem
                imgName = "-img" + numImg + "-"

                if window[eventos].get_text() == 'Descartar': 
                    #atualizando a imagem do layout para a imagem em preto e branco
                    window[imgName].update(data = imgGray)
                    window[eventos].update('Reverter')

                elif window[eventos].get_text() == 'Reverter': 
                    print(images[int(numImg)])
                    window[imgName].update(images[int(numImg)])
                    window[eventos].update('Descartar')


    def decolorizeImage(self, imgName):

        #lendo imagem original
        originalImg = cv2.imread(imgName)

        #convertendo a cor
        imgGray = cv2.cvtColor(originalImg, cv2.COLOR_BGR2GRAY)

        #convertendo o formato da imagem
        data = Image.fromarray(imgGray)
        image = ImageTk.PhotoImage(image=data)

        return image


    def makeImageLayout(self, nameImg, imgKey, nameMovie, btnKey, btnGuessKey ):

        # ------------------- Layout Definition -------------------
        imgLayout = [
            [sg.Image(nameImg, key=imgKey)],
            [sg.Text(nameMovie, text_color=('white'), font=fontName)],
            [sg.Button('Descartar', key=btnKey, button_color=('white', sg.theme_background_color()), font=fontHint, border_width = 0)],
            # [sg.Button('Adivinhar', key=btnGuessKey, button_color=('white', sg.theme_background_color()), font=fontHint, border_width = 0)]
        ]

        # ------------------- Window Creation -------------------
        return imgLayout

