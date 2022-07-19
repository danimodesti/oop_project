from email.mime import image
from select import select
from webbrowser import BackgroundBrowser
from PySimpleGUI import PySimpleGUI as sg
from pandas import read_csv
from MovieGame import *
from UserGame import *
from ReadCSV import *
from GameBoard import *
import random
import textwrap
import cv2
from PIL import Image, ImageTk
import re


# Layout
# sg.theme('DarkBlue')
font = ("Arial", 40)
fontHint = ("Arial", 15)
fontName = ("Arial", 10)
fontButton = ("Arial", 20)
fontUserLayout = ("Helvetica", 15)
fontName = ("Helvetica", 12)
movies = []

# ----------------------------------


class FaceTheMovie():
    allMovies = list()
    rounds = 0

    def __init__(self):
        UserLayout = [
            [sg.VPush()],
            [sg.Text('Insira aqui seu nome', text_color=(
                'white'), key='-text-', font=fontUserLayout)],
            [sg.InputText()],
            [sg.Button('Entrar', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)],
            [sg.VPush()]
        ]
        # Entrada e criacao do objeto User
        windowUser = sg.Window('BEM VINDO', UserLayout, size=(
            400, 200), element_justification='c', use_default_focus=False)
        while True:
            eventos, valores = windowUser.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Entrar':
                if valores[0] != '':  # Nao aceita nomes nulos

                    userName = valores[0]
                    self.user = User(userName)  # Criando o usuario
                    # adiciona nome no csv para ranking
                   # addUserNameCSV(self.user.getName(),self.user.getTotalScore()) 
                    # linha teste
                    addUserNameCSV(self.user.getName(),0) 
                    windowUser.close()
                    print(f'USER NAME: {self.user.getName()}')

                    # Criando um novo jogo
                    self.mainMenu()

    def mainMenu(self):
        title = [
            [sg.Text('FACE', text_color=('white'), key='-text-', font=font)],
            [sg.Text('THE', text_color=('white'), key='-text-', font=font)],
            [sg.Text('MOVIE', text_color=('white'), key='-text-', font=font)]
        ]

        buttons = [
            [sg.Button('Jogar', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)],
            [sg.Button('Ranks', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)],
            [sg.Button('Sair', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)]
        ]
        Layout = [
            [sg.VPush()],
            [sg.Column(title), sg.Column(buttons)],
            [sg.VPush()]
        ]

        levelNumber = self.user.getLevel()
        level = 'Padrao'
        if levelNumber == 1:
            level = 'Iniciante'
        elif levelNumber == 2:
            level = 'Intermediario'
        else:
            level = 'Profissional'
        # Atualiza o menu com o nome do usuario
        NewLayout = [[sg.Text(f'Seu nome para ranks: {self.user.getName()} | Nivel: {level}', text_color=(
            'white'), key='-textName-', font=fontName)]] + Layout

        # Janela
        window = sg.Window('Face the Movie', NewLayout, size=(
            600, 300), element_justification='c', use_default_focus=False)
        # Ler os eventos
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Jogar':
                window.close()
                print('JOGO AQUI')

                # Criando um novo jogo
                self.newGame()

            if eventos == 'Ranks':
                window.close()
                print('RANQ AQUI')
                # Abrindo a lista de Ranks
                self.showRank()

            if eventos == 'Sair':
                break

    def showRank(self):
        buttons = [
            [sg.Button('Voltar', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)],
            [sg.Button('Sair', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)]
        ]
        
        RankLayout = [
            [sg.Text('MELHORES PONTUACOES', text_color=(
                'white'), key='-text-', font=font)],
            [sg.Column(buttons, vertical_alignment="bottom",element_justification='right',expand_x=True)]
        ]
        
        window = sg.Window('Ranking', RankLayout, size=(
            900, 400), element_justification='c', use_default_focus=False)
        # Ler os eventos
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Voltar':
                window.close()
                print('JOGO AQUI')

                # volta para o menu principal
                self.mainMenu()

            if eventos == 'Sair':
                break
        # Ler csv do rank e mostrar na tela
        print("SHoW RaNK")

    def newGame(self):

        # preencher lista de filmes com as informações do .csv
        self.allMovies = list()
        readCSV(self.allMovies)

        # Teste - printando os filmes lidos
        # print("Printando filmes ------------------------------------------")
        # for i in range(len(self.allMovies)):
        #     print(self.allMovies[i])

        self.newPhase()

    def newPhase(self):
        buttonNextHint = [
            [sg.Button('Proxima Dica', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)]
        ]

        # Cria o Gameboard de uma partida
        self.Gameboard = Gameboard(self.allMovies, 15, self.user.getLevel())
        self.Gameboard.showMovies()

        # lista com nomes das imagens e dos filmes que serao as alternativas
        images = []
        names = []

        self.Gameboard.loadImagesAndNames(images, names)
        # print(f"IMAGES: {len(images)} AND YUP: {names}")

        try:
            # adicionando as imagens na tela
            imgLayouts = []

            for i in range(self.Gameboard.getNumMovies()):
                # definindo as 'keys' das imagens e dos botoes
                imgKey = "-img" + str(images[i][0]) + "-"
                btnKey = "-btnDesc" + str(images[i][0]) + "-"
                btnGuessKey = "-btnAdv" + str(images[i][0]) + "-"
                print(f"IMAGES: {images[i]}, {imgKey}, {names[i]}, {btnKey}")

                # chamando a funcao de criacao de layout e adicionando na lista de layouts
                imgLayouts.append(self.makeImageLayout(
                    images[i][1], imgKey, names[i], btnKey, btnGuessKey))

        except:
            print("Não foi possível encontrar as imagens!")

        print(len(imgLayouts))

        # sorteando um filme para ser adivinhado
        self.Gameboard.drawSelectedMovie()
        print(self.Gameboard.selectedMovie)
        print(self.Gameboard.getIdSelectedMovie())
        possibleHints = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # selecionando uma dica
        hint = self.Gameboard.newHint(possibleHints)

        # layout da pagina
        Layout2 = [
            # Elementos da pagina
            # [sg.Text('PREPARAR', key='-text-', font=font)],
            [sg.Text(hint, key='-textHint-', font=fontHint)],
        ]

        # Imagens
        line = []

        for i in range(len(imgLayouts)):
            line += [sg.Column(imgLayouts[i]), ]
            if i != 0 and i % 7 == 0:
                Layout2 += [line]
                line = []

        Layout2 += [line]

        Layout2 += [[sg.Column(buttonNextHint)]]

        # abrindo uma nova janela
        window = sg.Window(
            'GAME', Layout2, element_justification='c', use_default_focus=False).Finalize()
        window.Maximize()

        # Ler os eventos
        while True:
            eventos, valores = window.read()
            # Fechando o programa
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Proxima Dica':
                # Diminuindo a pontuacao
                self.Gameboard.decreaseScore(250)
                # selecionando uma nova dica
                hint = self.Gameboard.newHint(possibleHints)
                # atualizando o elemento texto que representa a dica
                window.Element('-textHint-').update(hint)

            if eventos.startswith('-btnDesc'):

                # verificando qual e o numero da alternativa que foi selecionada
                idImg = re.sub("[^0-9]", "", eventos)

                index = 0
                for i in range(len(images)):
                    if images[i][0] == int(idImg):
                        index = i
                        break

                # descolorindo a imagem referente a alternativa selecionada
                imgGray = self.decolorizeImage(images[index][1])

                # determinando qual sera o nome da imagem
                imgName = "-img" + idImg + "-"

                if window[eventos].get_text() == 'Descartar':
                    # atualizando a imagem do layout para a imagem em preto e branco
                    window[imgName].update(data=imgGray)
                    window[eventos].update('Reverter')

                elif window[eventos].get_text() == 'Reverter':
                    # print(len(images))
                    # print(idImg)
                    window[imgName].update(images[index][1])
                    window[eventos].update('Descartar')

            if eventos.startswith('-btnAdv'):
                # verificando qual e o numero da alternativa que foi selecionada
                idMovie = re.sub("[^0-9]", "", eventos)
                print(f"ID MOVIE: {idMovie}")

                if self.Gameboard.getIdSelectedMovie() == int(idMovie):
                    sg.popup_no_titlebar(
                        'Parabens! Voce acertou o filme, vamos para a proxima rodada!', keep_on_top=True, background_color='black')
                    self.Gameboard.increaseScore(250)
                    self.increaseRounds()
                    if self.getRounds() == 3:
                        self.user.increaseLevel()
                        sg.popup_no_titlebar(
                            'Parabens! Voce passou de nível, vamos dificultar um pouco mais 😈', keep_on_top=True, background_color='black')
                        window.close()
                        self.setRounds() # reinicia a contagem das rodadas
                        self.newPhase()
                    else:
                        window.close()
                        self.newPhase() # reinicia jogo
                else:
                    self.Gameboard.decreaseScore(150)
                    sg.popup_no_titlebar(
                        'ERROU', keep_on_top=True, background_color='black')

    def endGame(self):
        self.mainMenu()

    def decolorizeImage(self, imgName):

        # lendo imagem original
        originalImg = cv2.imread(imgName)

        # convertendo a cor
        imgGray = cv2.cvtColor(originalImg, cv2.COLOR_BGR2GRAY)

        # convertendo o formato da imagem
        data = Image.fromarray(imgGray)
        image = ImageTk.PhotoImage(image=data)

        return image

    def makeImageLayout(self, nameImg, imgKey, nameMovie, btnKey, btnGuessKey):

        # ------------------- Layout Definition -------------------
        imgLayout = [
            [sg.Image(nameImg, key=imgKey)],
            [sg.Text(nameMovie, text_color=('white'), font=fontName)],
            [sg.Button('Descartar', key=btnKey, button_color=(
                'white', sg.theme_background_color()), font=fontHint, border_width=0)],
            [sg.Button('Adivinhar', key=btnGuessKey, button_color=(
                'white', sg.theme_background_color()), font=fontHint, border_width=0)]
        ]

        # ------------------- Window Creation -------------------
        return imgLayout

    def increaseRounds(self):
        self.rounds += 1

    def getRounds(self):
        return self.rounds
    
    def setRounds(self):
        self.rounds = 0
