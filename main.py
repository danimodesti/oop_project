#
# Ana Cristina Silva de Oliveira — 11965630
# Danielle Modesti — 12543544
# Laura Ferré Scotelari — 12543436
# Rebeca Vieira Carvalho — 12543530
# 
# POO — 3o semestre — Professor Delamaro
# 
# Projeto Final - POO

from face_the_movie import *
from webbrowser import BackgroundBrowser
from PySimpleGUI import PySimpleGUI as sg
from Movie import *
from readCSV import *
import random
import textwrap

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

def main():
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
            newGame()

        if eventos == 'Sair' :
            break

def newGame():
    #preencher lista de filmes com as informações do .csv
    readCSV(movies)

    #Teste - printando os filmes lidos 
    for i in range(len(movies)):
        print(movies[i])

    newPhase()

def newPhase():

    #preparando o ambiente grafico ----------------

    #lista com nomes das imagens e dos filmes que serao as alternativas
    images = []
    names = []

    for i in range(len(movies)):
        #pegando os nomes das imagens
        images.append(movies[i].imgName)

        #pegando os nomes dos filmes e adicionando quebra de linha
        namePieces = textwrap.wrap(movies[i].name,20)
        for i in range(len(namePieces) - 1):
            namePieces[0] = namePieces[i] + "\n" + namePieces[i+1]

        #adicionando os nomes com quebra de linha na lista de nomes
        names.append(namePieces[0])
    #-----------------------------------------------

    try:
        #adicionando as imagens na tela
        imagem1 = [[sg.Image(images[0])], [sg.Text(names[0], text_color=('white'), font=fontName)]]
        imagem2 = [[sg.Image(images[1])], [sg.Text(names[1], text_color=('white'), font=fontName)]]
        imagem3 = [[sg.Image(images[2])], [sg.Text(names[2], text_color=('white'), font=fontName)]]
        imagem4 = [[sg.Image(images[3])], [sg.Text(names[3], text_color=('white'), font=fontName)]]
        imagem5 = [[sg.Image(images[4])], [sg.Text(names[4], text_color=('white'), font=fontName)]]
        imagem6 = [[sg.Image(images[5])], [sg.Text(names[5], text_color=('white'), font=fontName)]]
        imagem7 = [[sg.Image(images[6])], [sg.Text(names[6], text_color=('white'), font=fontName)]]
        imagem8 = [[sg.Image(images[7])], [sg.Text(names[7], text_color=('white'), font=fontName)]]
        imagem9 = [[sg.Image(images[8])], [sg.Text(names[8], text_color=('white'), font=fontName)]]
        imagem10 =[[sg.Image(images[9])], [sg.Text(names[9], text_color=('white'), font=fontName)]]
    except:
        print("Não foi possível encontrar as imagens!")

    # sorteando um filme para ser adivinhado
    selectedMovie = shuffleMovies()
    possibleHints = [1, 2, 3, 4, 5, 6]

    # selecionando uma dica
    hint = newHint(selectedMovie, possibleHints)
    
    #layout da pagina
    Layout2 = [
        #Elementos da pagina
        [sg.Text('PREPARAR', key='-text-', font=font)],
        [sg.Text(hint, key='-textHint-', font=fontHint)],
        [sg.Column(imagem1) , sg.Column(imagem2), sg.Column(imagem3), sg.Column(imagem4), sg.Column(imagem5)],
        [sg.Column(imagem6) , sg.Column(imagem7), sg.Column(imagem8), sg.Column(imagem9), sg.Column(imagem10)],
        [sg.Column(buttonNextHint)]
    ]

    #abrindo uma nova janela
    janela = sg.Window('OPA', Layout2, size=(900,600), element_justification = 'c', use_default_focus=False)

    # Ler os eventos
    while True:
        eventos, valores = janela.read()
        #Fechando o programa
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Proxima Dica':
            # selecionando uma nova dica
            hint = newHint(selectedMovie, possibleHints)
            #atualizando o elemento texto que representa a dica
            janela.Element('-textHint-').update(hint)


def shuffleMovies():
    #sorteando um filme e retirando ele da lista
    random.shuffle(movies)

    return movies.pop()

def newHint(selectedMovie, possibleHints):

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


main()