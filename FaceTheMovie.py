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
import time

# Configuracoes de sLayout
# sg.theme('DefaultNoMoreNagging')
font = ("Arial", 40)
fontHint = ("Arial", 12)
fontScore = ("Arial", 15)
fontText = ("Arial", 10)
fontButton = ("Arial", 20)
fontButton2 = ("Arial", 13)
fontButton3 = ("Arial", 10)
fontPopUp = ("Arial", 15)
fontUserLayout = ("Helvetica", 15)
fontName = ("Helvetica", 10)
movies = []


class FaceTheMovie():
    
    # Construtor --------------------------
    def __init__(self):

        self.round = 0
        self.alreadyDraw = list()
        self.userWindow()
        self.paused = 0
        
    
    # Entrada do Usuario ------------------------------------------------
    def userWindow(self):
        UserLayout = [
            [sg.VPush()],
            [sg.Image("imagens\cinema.png")],
            [sg.Text('Insira aqui seu nome', text_color=(
                'white'), key='-text-', font=fontUserLayout)],
            [sg.InputText()],
            [sg.Button('Entrar', button_color=(
                'white', sg.theme_background_color()), font=fontButton, border_width=0)],
            [sg.VPush()]
        ]

        # Entrada e criacao do objeto User ------------------------------
        windowUser = sg.Window('BEM VINDO', UserLayout, size=(
            600, 400), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico')

        # Eventos da janela de usuario
        while True:
            eventos, valores = windowUser.read()
            if eventos == sg.WINDOW_CLOSED:
                break
            if eventos == 'Entrar':
                if valores[1] != '':  # Nao aceita nomes nulos

                    userName = valores[1]
                    self.user = User(userName)  # Criando o usuario
                    
                    # adiciona nome no csv para ranking
                    # linha teste

                    windowUser.close() # Fecha 

                    # Criando um novo jogo
                    self.mainMenu()

    # Menu Principal --------------------------------
    def mainMenu(self):

        # Intefaces ---------------------------------
        title = [
            [sg.Image("imagens/jogo_nome.png", pad=(10,0))],
        ]

        buttons = [
            [sg.Button('Jogar', button_color=(sg.theme_background_color(), sg.theme_background_color()), font=fontPopUp, image_filename='imagens/btn_fundo.png',  pad=(0,5), border_width=0)],
            [sg.Button('Ranking', button_color=(sg.theme_background_color(), sg.theme_background_color()), font=fontPopUp, image_filename='imagens/btn_fundo.png',  pad=(0,5), border_width=0)],
            [sg.Button('Como Jogar', button_color=(sg.theme_background_color(), sg.theme_background_color()), font=fontPopUp, image_filename='imagens/btn_fundo.png', pad=(0,5), border_width=0)],
            [sg.Button('Sair', button_color=(sg.theme_background_color(), sg.theme_background_color()), font=fontPopUp, image_filename='imagens/btn_fundo.png',  pad=(0,5), border_width=0)]
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
            level = 'Pipoca de Cinema'
        elif levelNumber == 2:
            level = 'Artista em cena'
        else:
            level = 'Cinéfilo'

        # Atualiza o menu com o nome do usuario
        NewLayout = [[sg.Text(f'Seu nome para ranking: {self.user.getName()} | Nivel: {level} | Score total: {self.user.getTotalScore()}', text_color=(
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
                self.gameModes()
                break
            if eventos == 'Ranking':
                window.close() # Fecha a janela de menu
                self.showRanking() # Mostra a janela de rank
                break
            if eventos == 'Como Jogar':
                window.close()
                self.howToPlay()

            if eventos == 'Sair':
                break
        window.close()

    def gameModes(self):
        # Layouts ------------------------

        howToPlayLayout = [
            [sg.Text('Modos de Jogo', text_color=('white'), key='-text-', font=font)],
            [sg.Button('> Normal', button_color=(sg.theme_background_color(), sg.theme_background_color()), font=fontPopUp, image_filename='imagens/btn_fundo.png',  pad=(0,5), border_width=0)],
            [sg.Button('> Temporizador',  button_color=(sg.theme_background_color(), sg.theme_background_color()), font=fontPopUp, image_filename='imagens/btn_fundo.png',  pad=(0,5), border_width=0)],
            [sg.Button('> Morte súbita',  button_color=(sg.theme_background_color(), sg.theme_background_color()), font=fontPopUp, image_filename='imagens/btn_fundo.png',  pad=(0,5), border_width=0)]
        ]
        
        # Janela de Modos de jogo ----------------------------------
        window = sg.Window('Modos de jogo', howToPlayLayout, size=(
            700, 300), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico')

        gameMode = 0

        # Ler os eventos
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                window.close()
                self.mainMenu()
                break

            if eventos == '> Normal':
                gameMode = 0
            if eventos == '> Temporizador':
                gameMode = 1
            if eventos == '> Morte súbita':
                gameMode = 2

            window.close()
            self.newGame(gameMode)
            break
    
    def howToPlay(self):
        # Layouts ------------------------
        howToPlay = self.wrapHint("Para jogar 'Face The Movie', não é necessário ser cinéfilo! Basta ficar bem atento(a) às informações apresentadas na sua telinha. Você terá até 10 dicas sobre um filme sorteado por nós para tentar acertá-lo, clicando em 'Adivinhar'' quando achar que o descobriu. Dessa forma, temos certeza de que você vai sair daqui sabendo muito mais sobre o mundo do Cinema!\n", 100)
        howToPlay +="\n"
        howToPlay += "• Níveis de jogo\n"
        howToPlay += self.wrapHint("\tApesar de não ser necessário ser um guru do cinema, o conhecimento do jogador é recompensado com mais pontos, possibilitando-o subir rapidamente de nível, começando no 1 (Pipoca de cinema), direcionando-se ao 2 (Artista em cena) e, finalmente, atingindo o 3 (Cinéfilo), a depender de sua pontuação conquistada. A cada nível, os filmes sorteados são repaginados e mais complicados.\n", 100)
        howToPlay +="\n"
        howToPlay += "• Dicas\n"
        howToPlay += self.wrapHint("\tSe estiver muito difícil de acertar, fique tranquilo(a). Você pode adquirir até 10 dicas sobre o filme sorteado. Porém, faça-o sabiamente, pois, a cada dica fornecida, o usuário perde 20 pontos da rodada (que inicialmente vale 200 pontos).\n", 100)
        howToPlay +="\n"
        howToPlay += self.wrapHint("\tAs possíveis dicas para o jogo, são: nota no IMDB, gênero do filme, diretor, ator/atriz principal, algum outro membro do elenco, classificação indicativa, curiosidade sobre o filme, duração, ano de lançamento, e se o filme escolhido já ganhou um Oscar ou não. A ordem das dicas é aleatória.\n", 100)
        howToPlay +="\n"
        howToPlay += "• Penalidades\n"
        howToPlay += self.wrapHint("\tO jogador perde pontos ao pedir dicas, ao reverter descartes de filme ou ao adivinhá-los incorretamente. É preciso pensar nas melhores escolhas para salvar o seu jogo a cada rodada, e atenção para não zerar a pontuação, o que causa FIM DE JOGO!\n", 100)
        howToPlay +="\n"
        howToPlay += "• Recuperando pontos\n"
        howToPlay += self.wrapHint("\tNem tudo está perdido! Caso você perca mais pontos que o esperado, pode descartar alguns filmes a partir das dicas que já tem. A cada filme desconsiderado, o jogador recupera 10 pontos!\n", 100)
        howToPlay +="\n"
        howToPlay += "• Revertendo o descarte\n"
        howToPlay += self.wrapHint("\tMuito cuidado com um movimento de descarte mal-pensado, pois, caso mude de ideia, o jogador perde 50 pontos para reativar a carta do filme.\n", 100)
        howToPlay +="\n"
        howToPlay += "• Adivinhando o filme errado\n"
        howToPlay += self.wrapHint("\tCaso o jogador tente 'Adivinhar' e falhe, ele sofrerá uma perda de pontos significativa. Então, tenha certeza dessa decisão.\n", 100)
        howToPlay +="\n"
        howToPlay += "• Ranking\n"
        howToPlay += self.wrapHint("\tOs cinco melhores jogadores ficam registrados nesta aba.\n", 100)
        howToPlay +="\n"
        howToPlay += "• Modos de jogo\n"
        howToPlay += self.wrapHint("\tO jogador pode treinar seus conhecimentos em Cinema de três formas:\n", 100)
        howToPlay +="\n"
        howToPlay += self.wrapHint("> Normal: jogo clássico. Há apenas controle de pontuação para cada rodada e para passar de níveis, até o terceiro. É possível finalizar o jogo e submeter pontuação de usuário;\n", 100)
        howToPlay +="\n"
        howToPlay += self.wrapHint("> Temporizador: há um timer no topo da tela de jogo e o jogador tem 1 minuto por rodada para adivinhar o filme; caso isso não ocorra, é fim de jogo;\n", 100)
        howToPlay +="\n"
        howToPlay += self.wrapHint("> Morte súbita: há apenas uma dica, a de curiosidade do filme. Caso o jogador, com essa informação, não adivinhe o filme sorteado, perde o jogo.\n", 100)
        howToPlay +="\n"
        howToPlay += self.wrapHint("O objetivo desses dois últimos modos é atingir a maior quantidade de rodadas completadas possível.\n", 100)
        howToPlay +="\n"
        howToPlay += "• Fim de jogo\n"
        howToPlay += self.wrapHint("\tPara terminar o jogo de verdade, o usuário deve atingir nível 3 - para isso, atingir uma pontuação específica para passar do nível 1 até o 2, e do 2 até o 3. A partir desse momento, adivinha 5 filmes até obter sua pontuação final.\n", 100)

        textLayout = [
            [sg.Text(howToPlay, text_color=('white'), key='-text-', font=("Arial", 13), justification='left')]
        ]
        howToPlayLayout = [
            [sg.Text('Como jogar', text_color=('white'), key='-text-', font=font)],
            [sg.Column(textLayout, scrollable=True, size=(850, 500), vertical_scroll_only=True)],
            [sg.Button('Voltar', button_color=('white', sg.theme_background_color()), font=fontButton, border_width=0)]
        ]
        
        # Janela de Como jogar ----------------------------------
        window = sg.Window('Como Jogar', howToPlayLayout, size=(
            850, 660), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico')

        # Ler os eventos
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                window.close()
                self.mainMenu()
                break
            if eventos == 'Voltar':
                window.close()

                # volta para o menu principal
                self.mainMenu()
                break
    
    # Mostrar Rank ---------------------------------------------
    def showRanking(self):
        userList = readRankingCSV()
        #------------interface grafica---------------------------------------
        RankLayout = [
            [sg.Image("imagens/coroa.png")],
            [sg.Text('MELHORES PONTUAÇÕES', text_color=(
                'white'), key='-text-', font=font)]
        ]
    
        scoreLayouts = []

        for i in range(len(userList)):
            #------------criando o layout de imagens---------------
            scoreLayout = self.makeScoreLayout(userList[i].getName(), userList[i].getTotalScore(), i + 1)

            #--adicionando o layout em uma coluna de tamanho fixo--
            # chamando a funcao de criacao de layout e adicionando na lista de layouts
            scoreLayouts.append(scoreLayout)

        # Scores
        line = []

        for i in range(len(userList)):
            line += [scoreLayouts[i],]
        
        
        RankLayout += [line]

        buttons = [
            [sg.Button('Voltar', button_color=(sg.theme_background_color(), sg.theme_background_color()), font=fontButton, image_filename='imagens/btn_ante_dica.png', border_width=0)]
        ]
        RankLayout += [
            [sg.Column(buttons, vertical_alignment="bottom",element_justification='center',expand_x=True)]
        ]

        window = sg.Window('Ranking', RankLayout, size=(
        900, 600), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico').Finalize()
        window.Maximize()

        #--------------------------------------------------------------------------------------

        # Ler os eventos
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                window.close()
                # volta para o menu principal
                self.mainMenu()
                break
            if eventos == 'Voltar':
                window.close()
                # volta para o menu principal
                self.mainMenu()
                break
            if eventos == 'Enviar Pontuação':
                window.close()
                if self.user.getTotalScore() > 0:
                    addUserNameCSV(self.user)

                # volta para o menu principal
                self.mainMenu()
                break
  
  

    def timer_count(self):
        return int(round(time.time() * 100))

    def newGame(self, gameMode):

        # Preencher lista de filmes com as informações do .csv
        self.allMovies = list()
        readMovieCSV(self.allMovies)

        # Chama nova fase
        self.newPhase(gameMode)

    # Nova fase --------------------------------------------------------
    def newPhase(self, gameMode):
        newHintCount = 0
        inGame = True

        #reiniciando timer
        if gameMode == 1:
            self.start_time = self.timer_count()
            self.paused = 0
            self.current_time = 0

        #incrementando o numero de rounds
        self.round += 1

        # Cria o objeto 'Tabuleiro' de uma partida -----------------
        level = self.user.getLevel()
        self.gameboard = Gameboard(200, self.allMovies, 16, level)

        #Verif. se o jogo ja deve acabar
        if level == 3 and self.round > 5:
            self.showEndingScreen(1)
        else:
            #continua o jogo
            # Sorteando um filme para ser adivinhado ----------------
            self.gameboard.drawSelectedMovie()

            # Verificando se o filme já não foi sorteado nas rodadas passadas
            added = 0
            while added == 0:
                if self.alreadyDraw.count(self.gameboard.getIdSelectedMovie()) == 0:
                    self.alreadyDraw.append(self.gameboard.getIdSelectedMovie())
                    added = 1
                else: self.gameboard.drawSelectedMovie()        
            
            # Sorteando as dicas do filme selecionado ---------------
            self.gameboard.drawHints(gameModeHint = gameMode)

            newHint = self.gameboard.getActualHint() # selecionando uma dica
            hint  = self.wrapHint(newHint, 129)

            self.gameboard.shuffleMovies()

            # Interface ----------------------------------------

            buttonNextHint = [
                [sg.Button('Dica Anterior', button_color=(
                    sg.theme_background_color(), sg.theme_background_color()), font=fontButton2, image_filename='imagens/btn_ante_dica.png', border_width=0), 
                sg.Button('Próxima Dica', button_color=(
                    sg.theme_background_color(), sg.theme_background_color()), font=fontButton2, image_filename='imagens/btn_prox_dica.png', border_width=0)]
            ]
            
            # Lista com nomes das imagens e dos filmes que serao as alternativas
            images = []
            names = []

            self.gameboard.loadImagesAndNames(images, names)
            try:
                # Adicionando as imagens no layout
                imgLayouts = []

                for i in range(self.gameboard.getNumMovies()):

                    # definindo as 'keys' das imagens e dos botoes
                    imgKey = "-img" + str(images[i][0]) + "-"
                    btnKey = "-btnDesc" + str(images[i][0]) + "-"
                    btnGuessKey = "-btnAdv" + str(images[i][0]) + "-"

                    # chamando a funcao de criacao de layout e adicionando na lista de layouts
                    imgLayout = self.makeImageLayout(
                                images[i][1], imgKey, names[i], btnKey, btnGuessKey)

                    #adicionando o layout em uma coluna de tamanho fixo
                    imgCol = sg.Col((imgLayout), size = (130,300))
                    # chamando a funcao de criacao de layout e adicionando na lista de layouts
                    imgLayouts.append(imgCol)

            except:
                print("Não foi possível encontrar as imagens!")

            # layout da Pagina
            if gameMode == 1:
                Layout2 = [
                    [sg.Text(hint, key='-textHint-', font=fontHint, pad=(30,20), justification='center'),
                    sg.Text('', font=fontText, justification='left', key='timer', pad=(0,0)),
                    sg.Text(str(self.gameboard.getScore()) + " pontos", font=fontText, justification='left', key='score', pad=(0,0))]
                ]
            else:
                Layout2 = [
                    [sg.Text(hint, key='-textHint-', font=fontHint, pad=(30,20), justification='center'), sg.Text(str(self.gameboard.getScore()) + " pontos", font=fontText, justification='left', key='score', pad=(0,0))],
                ]

            # Adicionando as imagens no layout
            line = []

            for i in range(len(imgLayouts)):
                line += [imgLayouts[i],]
                #garantindo que cada linha tera 8 filmes
                if ((i+1) % 8) == 0:
                    Layout2 += [line],
                    line = []

            Layout2 += [line]

            if gameMode != 2: Layout2 += [buttonNextHint] # Adiciona o botao de nova dica

            # Abrindo uma nova janela -------------------------
            window = sg.Window(
                'GAME', Layout2, element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico', enable_close_attempted_event=True).Finalize()
            window.Maximize()

            # Ler os eventos ---------------------
            while True:
                if gameMode == 1 and not self.paused:
                    eventos, values = window.read(timeout=10)
                    self.current_time = self.timer_count() - self.start_time
                    if ((self.current_time // 100) // 60) == 5:
                        sg.popup_no_titlebar(
                            'ACABOU O TEMPO', keep_on_top=True, background_color='black', font=fontPopUp)
                        window.close()
                        self.mainMenu()
                        break
                else:
                    eventos, valores = window.read()

                if eventos == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or eventos == 'Exit':
                    self.paused = 1
                    if sg.popup_yes_no('Tem certeza que deseja sair do jogo? Seu progresso nessa partida não sera salvo.', title='Já vai?', font=fontPopUp) == 'Yes':
                        window.close()
                        self.mainMenu()
                        break
                    else:
                        self.paused = 0

                if eventos == 'Próxima Dica':
                    # Atualizar a Pontuacao **
                    if newHintCount < 9:
                        if self.gameboard.decreaseScore(20) == 0: inGame = False
                        window.Element('score').update(self.gameboard.getScore()) 
                        newHintCount += 1

                    # Selecionando uma nova dica
                    newHint = self.gameboard.nextHint()
                    hint  = self.wrapHint(newHint, 129)

                    if hint != None: 
                        # atualizando o elemento texto que representa a dica
                        window.Element('-textHint-').update(hint) 

                if eventos == 'Dica Anterior':
                    # Atualizar a Pontuacao **

                    # Selecionando uma nova dica
                    newHint = self.gameboard.previousHint()
                    hint  = self.wrapHint(newHint,129)

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
                        self.gameboard.increaseScore(10)
                        window.Element('score').update(self.gameboard.getScore()) 

                        window[imgName].update(data=imgGray)
                        window[eventos].update('Reverter')

                    elif window[eventos].get_text() == 'Reverter':
                        # Atualizando a imagem do layout para a imagem original
                        if self.gameboard.decreaseScore(50) == 0: inGame = False
                        window.Element('score').update(self.gameboard.getScore()) 

                        window[imgName].update(images[index][1])
                        window[eventos].update('Descartar')

                if eventos.startswith('-btnAdv'): # Tentar adivinhar um filme
                    # Verificando qual e o numero da alternativa que foi selecionada
                    idMovie = re.sub("[^0-9]", "", eventos)
                    buttonValue = window["-btnDesc" + str(idMovie) + "-"].get_text()

                    return_value = 'Yes' 
                    if gameMode == 2:
                        return_value = sg.popup_yes_no('Tem certeza da sua escolha? Lembre-se se você errar não terá a chance de tentar novamente.', title='Certeza?', font=fontPopUp)
                    
                    if buttonValue != 'Reverter' and return_value == 'Yes':
                        
                        if self.gameboard.getIdSelectedMovie() == int(idMovie):
                            sg.popup_no_titlebar(
                                f'Parabens! Voce acertou o filme, vamos para a próxima rodada! Voce ganhou com {self.gameboard.getScore()} pontos!', keep_on_top=True, background_color='black', font=fontPopUp)
                            self.gameboard.increaseScore(1.45) # Atualizando pontuacao

                            before = self.user.getTotalScore() 
                            self.user.increaseTotalScore(self.gameboard.getScore())
                        
                            if before < 1000 and self.user.getTotalScore() >= 1000: # Passou de nivel
                                self.user.increaseLevel()
                                #contagem de rounds nessa fase
                                self.round = 0
                                sg.popup_no_titlebar('Parabéns! Você passou para o próximo nível: Artista em cena', keep_on_top=True, background_color='black', font=fontPopUp)

                            elif before < 2500 and self.user.getTotalScore() >= 2500: # Passou de nivel
                                self.user.increaseLevel()
                                #contagem de rounds nessa fase
                                self.round = 0
                                sg.popup_no_titlebar('Parabéns! Você passou para o próximo nível: Cinéfilo', keep_on_top=True, background_color='black', font=fontPopUp)
                            

                            if before < 1000 and self.user.getTotalScore() < 1000:
                                left = 1000 - self.user.getTotalScore()
                                
                                message = f"Faltam {left} para o nivel 2"
                                sg.popup_no_titlebar(
                                    message, keep_on_top=True, background_color='black', font=fontPopUp)
                                
                            elif before < 2500 and self.user.getTotalScore() < 2500:
                                left = 2500 - self.user.getTotalScore()
                                
                                message = f"Faltam {left} para o nivel 3"
                                sg.popup_no_titlebar(
                                    message, keep_on_top=True, background_color='black', font=fontPopUp)

                            window.close()
                            self.newPhase(gameMode)
                            break

                        else: # Quando nao acerta o filme
                            if self.gameboard.penaltyScore(0.4) == 0: inGame = False
                            window.Element('score').update(self.gameboard.getScore()) 

                            if gameMode == 2:
                                sg.popup_no_titlebar('Você Errou!! Boa sorte da próxima vez >:)', font=fontPopUp , keep_on_top=True, background_color='black')
                                window.close()
                                self.mainMenu()
                                break
                            else:
                                sg.popup_no_titlebar('ERROU', keep_on_top=True, background_color='black')
                
                if not inGame:
                    sg.popup_no_titlebar('Sua pontuação chegou a zero! Você Perdeu! ', keep_on_top=True, background_color='black')
                    window.close()
                    self.showEndingScreen(0)
                    break
                if gameMode == 1:
                    window['timer'].update('{:02d}:{:02d}'.format((self.current_time // 100) // 60,
                                                                (self.current_time // 100) % 60))
    def showEndingScreen(self, type):
    
        score = self.user.getTotalScore()
        text = ""
        imgName = ""
        #usuario chegou ao final
        if type == 1:
            text = "Parabens! Voce chegou ao final!"
            imgName = "imagens/imgVitoria.png"

        else:
            text = "Voce perdeu :("
            imgName = "imagens/imgDerrota.png"

        layoutEndScreen = [
            [sg.Image(imgName)],
            [sg.Text(text, text_color=('white'), key='-text-', font=font)],
            [sg.Text(str(score) + " pontos.", text_color=('white'), key='-text-', font=font)],
            [sg.Button('Enviar Pontuação', button_color=(sg.theme_background_color(), sg.theme_background_color()),
                font=fontButton2, image_filename='imagens/btn_fundo2.png', border_width=0),
             sg.Button('Voltar', button_color=(sg.theme_background_color(), sg.theme_background_color()),
                font=fontButton2, image_filename='imagens/btn_ante_dica.png', border_width=0)]
        ]
        window = sg.Window('Fim de Jogo', layoutEndScreen, size=(
        900, 600), element_justification='c', use_default_focus=False, icon = './imagens/cinema.ico')


        #--------------------------------------------------------------------------------------

        # Ler os eventos
        while True:
            eventos, valores = window.read()
            if eventos == sg.WINDOW_CLOSED:
                window.close()
                # volta para o menu principal
                self.mainMenu()
                break
            if eventos == 'Voltar':
                window.close()
                # volta para o menu principal
                self.mainMenu()
                break
            if eventos == 'Enviar Pontuação':
                if self.user.getTotalScore() > 0:
                    addUserNameCSV(self.user)
                    # volta para o menu principal
                    self.mainMenu()
                break

        


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
        #colocando o titulo do filme dentro de uma coluna de tamanho fixo
        titleLayout = [[sg.Text(nameMovie, text_color=('white'), font=fontName)]]
        titleCol = sg.Col((titleLayout), size = (150,60), pad=(0,0))

        # ------------------- Layout Definition -------------------
        imgLayout = [
            [sg.Image(nameImg, key=imgKey)],
            [titleCol],
            [sg.Button('Descartar', key=btnKey, button_color=(
                "white", sg.theme_background_color()),  image_filename='imagens/btn_descartar.png', font=fontButton3, border_width=0)],
            [sg.Button('Adivinhar', key=btnGuessKey, button_color=(
                "white", sg.theme_background_color()), image_filename='imagens/btn_adivinhar.png', font=fontButton3, border_width=0)]
        ]


        return imgLayout



    def wrapHint(self, newHint, value):
        if newHint != None:
            # pegando os nomes dos filmes e adicionando quebra de linha
            hintPieces = textwrap.wrap(newHint, value, break_long_words=True, break_on_hyphens=True)
            hint = ""
            for i in range(len(hintPieces)):
                hint += hintPieces[i]
                if i < (len(hintPieces) - 1):
                    hint += "\n"
            return hint

    
    def makeScoreLayout(self, name, score, pos):
        #colocando o nome do usuario dentro de uma coluna de tamanho fixo
        text = name + " " + str(score) + " pontos"
        nameImg = ""
        if pos == 1:
            nameImg = "imagens/medal1.png"
        elif pos == 2:
            nameImg = "imagens/medal2.png"
        elif pos == 3:
            nameImg = "imagens/medal3.png"

        scoreLayout = [[sg.Image(nameImg), sg.Text(text, text_color=('white'), font=fontScore)], 
        [sg.Text("_______________________________________", text_color=('white'), font=fontScore)]]
        return scoreLayout