from ctypes import sizeof
from email.mime import image
from select import select
from tkinter import S
from webbrowser import BackgroundBrowser
from PySimpleGUI import PySimpleGUI as sg
from pandas import read_csv
from MovieGame import *
from UserGame import *
from ReadCSV import *
from GameBoard import *
import cv2
from PIL import Image, ImageTk
import re

# Configuracoes de sLayout
font = ("Arial", 40)
fontHint = ("Arial", 15)
fontName = ("Arial", 10)
fontText = ("Arial", 10)
fontButton = ("Arial", 20)
fontPopUp = ("Arial", 15)
fontUserLayout = ("Helvetica", 15)
fontName = ("Helvetica", 12)
movies = []

class FaceTheMovie():
    allMovies = list()
    rounds = 0

    # Construtor --------------------------
    def __init__(self):
        self.alreadyDraw = list()
        self.userWindow()
    
    # Entrada do Usuario ------------------------------------------------
    def userWindow(self):
        UserLayout = [
            [sg.VPush()],
            [sg.Text('Insira aqui seu nome', text_color=(
                'white'), key='-text-', font=fontUserLayout)],
            [sg.InputText()],
            [sg.Button('Entrar', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)],
            [sg.VPush()]
        ]

        # Entrada e criacao do objeto User ------------------------------
        windowUser = sg.Window('BEM VINDO', UserLayout, size=(
            400, 200), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico')

        # Eventos da janela de usuario
        while True:
            eventos, valores = windowUser.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Entrar':
                if valores[0] != '':  # Nao aceita nomes nulos

                    userName = valores[0]
                    self.user = User(userName)  # Criando o usuario
                    
                    # adiciona nome no csv para ranking
                    # linha teste
                    # addUserNameCSV(self.user.getName(), self.user.getTotalScore()) 

                    windowUser.close() # Fecha 
                    print(f'USER NAME: {self.user.getName()}')

                    # Criando um novo jogo
                    self.mainMenu()

    # Menu Principal --------------------------------
    def mainMenu(self):

        # Intefaces ---------------------------------
        title = [
            [sg.Text('FACE', text_color=('white'), key='-text-', font=font)],
            [sg.Text('THE', text_color=('white'), key='-text-', font=font)],
            [sg.Text('MOVIE', text_color=('white'), key='-text-', font=font)]
        ]

        buttons = [
            [sg.Button('Jogar', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0, pad=(10,0))],
            [sg.Button('Ranks', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0, pad=(10,0))],
            [sg.Button('Como Jogar', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0, pad=(10,0))],
            [sg.Button('Sair', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0, pad=(10,0))]
        ]
        Layout = [
            [sg.VPush()],
            [sg.Column(title), sg.Column(buttons)],
            [sg.VPush()]
        ]

        # Determinando Atributos iniciais do Usuario ---------------------------------------------
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

        # Janela do Menu ------------------------------------------------
        window = sg.Window('Face the Movie', NewLayout, size=(
            700, 400), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico')

        # Ler os eventos do Menu
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Jogar':
                window.close() # Fecha janela de menu
                self.newGame() # Cria um novo jogo

            if eventos == 'Ranks':
                window.close() # Fecha a janela de menu
                self.showRank() # Mostra a janela de rank

            if eventos == 'Como Jogar':
                window.close()
                self.howToPlay()

            if eventos == 'Sair':
                break
    
    def howToPlay(self):
        # Layouts ------------------------
        # Texto de teste kkkkk
        howToPlay = "TEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\nTEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n"
        howToPlay += "TEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\nTEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n"
        howToPlay += "TEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\nTEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n"
        howToPlay += "TEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\nTEXTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n"

        howToPlayLayout = [
            [sg.Text('Como jogar', text_color=('white'), key='-text-', font=font)],
            [sg.Text(howToPlay, text_color=('white'), key='-text-', font=fontText, justification='center')],
            [sg.Button('Voltar', button_color=('white', sg.theme_background_color()), font=fontButton, border_width=0)]
        ]
        
        # Janela de Rank ----------------------------------
        window = sg.Window('Como Jogar', howToPlayLayout, size=(
            700, 500), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico')

        # Ler os eventos
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                window.close()
                self.mainMenu()
            if eventos == 'Voltar':
                window.close()
                print('JOGO AQUI')

                # volta para o menu principal
                self.mainMenu()
    
    # Mostrar Rank ---------------------------------------------
    def showRank(self):

        # Layouts ------------------------
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
        
        # Janela de Rank ----------------------------------
        window = sg.Window('Ranking', RankLayout, size=(
            900, 400), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico')

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

        # Preencher lista de filmes com as informações do .csv
        self.allMovies = list()
        readCSV(self.allMovies)

        # Chama nova fase
        self.newPhase()

    # Nova fase --------------------------------------------------------
    def newPhase(self):

        # Cria o objeto 'Tabuleiro' de uma partida -----------------
        self.Gameboard = Gameboard(self.allMovies, 15, self.user.getLevel())
        
        # Sorteando um filme para ser adivinhado ----------------
        self.Gameboard.drawSelectedMovie()

        # Verificando se o filme já não foi sorteado nas rodadas passadas
        added = 0
        while added == 0:
            if self.alreadyDraw.count(self.Gameboard.getIdSelectedMovie()) == 0:
                self.alreadyDraw.append(self.Gameboard.getIdSelectedMovie())
                added = 1
            else: self.Gameboard.drawSelectedMovie()        
        
        # Sorteando as dicas do filme selecionado ---------------
        self.Gameboard.drawHints()
        hint = self.Gameboard.getActualHint() # selecionando uma dica

        # Interface ----------------------------------------
        buttonNextHint = [
            [sg.Button('< Dica Anterior', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0), 
                sg.VerticalSeparator(),
             sg.Button('Proxima Dica >', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)]
        ]
        
        # Lista com nomes das imagens e dos filmes que serao as alternativas
        images = []
        names = []

        self.Gameboard.loadImagesAndNames(images, names)
        try:
            # Adicionando as imagens no layout
            imgLayouts = []

            for i in range(self.Gameboard.getNumMovies()):

                # definindo as 'keys' das imagens e dos botoes
                imgKey = "-img" + str(images[i][0]) + "-"
                btnKey = "-btnDesc" + str(images[i][0]) + "-"
                btnGuessKey = "-btnAdv" + str(images[i][0]) + "-"
                # print(f"IMAGES: {images[i]}, {imgKey}, {names[i]}, {btnKey}")

                # chamando a funcao de criacao de layout e adicionando na lista de layouts
                imgLayouts.append(self.makeImageLayout(
                    images[i][1], imgKey, names[i], btnKey, btnGuessKey))

        except:
            print("Não foi possível encontrar as imagens!")

        # layout da Pagina
        Layout2 = [
            [sg.Text(hint, key='-textHint-', font=fontHint, pad=(30,20), justification='center')],
        ]

        # Adicionando as imagens no layout
        line = []
        for i in range(len(imgLayouts)):
            line += [sg.Column(imgLayouts[i], element_justification='c', pad=(0,2)),]
            if i != 0 and i % 7 == 0: # Quantas imagens tem por linha
                Layout2 += [line]
                line = []

        Layout2 += [line]
        Layout2 += [[sg.Frame('',buttonNextHint, pad=(0,20))]] # Adiciona o botao de nova dica

        # Abrindo uma nova janela -------------------------
        window = sg.Window(
            'GAME', Layout2, element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico', enable_close_attempted_event=True).Finalize()
        window.Maximize()

        # Ler os eventos ---------------------
        while True:
            eventos, valores = window.read()

            if eventos == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or eventos == 'Exit':
                if sg.popup_yes_no('Tem certeza que deseja sair do jogo? Seu progresso nessa partida não sera salvo.', title='Já vai?', font=fontPopUp) == 'Yes':
                    window.close()
                    self.mainMenu()
                    break

            if eventos == 'Proxima Dica >':
                # Atualizar a Pontuacao **

                # Selecionando uma nova dica
                hint = self.Gameboard.nextHint()

                if hint != None: 
                    # atualizando o elemento texto que representa a dica
                    window.Element('-textHint-').update(hint) 

            if eventos == '< Dica Anterior':
                # Atualizar a Pontuacao **

                # Selecionando uma nova dica
                hint = self.Gameboard.previousHint()

                if hint != None: 
                    window.Element('-textHint-').update(hint) 

            if eventos.startswith('-btnDesc'): # Descartar um filme
                # Verificando qual e o numero da alternativa que foi selecionada
                idImg = re.sub("[^0-9]", "", eventos)

                # Busca o indice do filme na lista de filmes
                index = 0
                for i in range(len(images)):
                    if images[i][0] == int(idImg):
                        index = i
                        break

                # Descolorindo a imagem referente a alternativa selecionada
                imgGray = self.decolorizeImage(images[index][1])

                # Determinando qual sera o nome da imagem
                imgName = "-img" + idImg + "-"

                if window[eventos].get_text() == 'Descartar':
                    # Atualizando a imagem do layout para a imagem em preto e branco
                    window[imgName].update(data=imgGray)
                    window[imgName].set_size((150,145))
                    window[eventos].update('Reverter')

                elif window[eventos].get_text() == 'Reverter':
                    # Atualizando a imagem do layout para a imagem original
                    window[imgName].update(images[index][1])
                    window[imgName].set_size((150,145))
                    window[eventos].update('Descartar')


            if eventos.startswith('-btnAdv'): # Tentar adivinhar um filme
                # Verificando qual e o numero da alternativa que foi selecionada
                idMovie = re.sub("[^0-9]", "", eventos)

                if self.Gameboard.getIdSelectedMovie() == int(idMovie):
                    sg.popup_no_titlebar(
                        'Parabens! Voce acertou o filme, vamos para a proxima rodada!', keep_on_top=True, background_color='black', font=fontPopUp)
                    self.Gameboard.increaseScore(250) # Atualizando pontuacao
                    self.increaseRounds() # Aumentando rounds

                    if self.getRounds() == 3:
                        level = self.user.increaseLevel()
                        if level == 3:
                            sg.popup_no_titlebar(
                                'Parabens! Voce passou de todos os níveis !! Sua pontuação foi de: ', keep_on_top=True, background_color='black', font=fontPopUp)
                            window.close()
                            self.mainMenu()
                            break
                        
                        sg.popup_no_titlebar(
                            'Parabens! Voce passou de nível, vamos dificultar um pouco mais 😈', keep_on_top=True, background_color='black', font=fontPopUp)
                        window.close()
                        self.setRounds() # reinicia a contagem das rodadas
                        self.newPhase()
                        break
                    else:
                        window.close()
                        self.newPhase() # reinicia jogo
                        break

                else: # Quando nao acerta o filme
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
            [sg.Image(nameImg, key=imgKey, size=(150,145))],
            [sg.Text(nameMovie, text_color=('white'), font=fontName, justification='center')],
            [sg.HorizontalSeparator()],
            [sg.Button('Descartar', key=btnKey, button_color=(
                'white', sg.theme_background_color()), font=fontHint, pad=(0,0), border_width=0)],
            [sg.Button('Adivinhar', key=btnGuessKey, button_color=(
                'white', sg.theme_background_color()), font=fontHint, pad=(0,0), border_width=0)]
        ]

        # ------------------- Window Creation -------------------
        return imgLayout

    def increaseRounds(self):
        self.rounds += 1

    def getRounds(self):
        return self.rounds
    
    def setRounds(self):
        self.rounds = 0
        self.alreadyDraw = list()
