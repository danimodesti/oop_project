#
# Ana Cristina Silva de Oliveira — 11965630
# Danielle Modesti — 12543544
# Laura Ferré Scotelari — 12543436
# Rebeca Vieira Carvalho — 12543530
# 
# POO — 3o semestre — Professor Delamaro
# 
# Projeto Final - POO
# Leitura dos atributos de um filme atraves de um arquivo .csv
import csv
import pandas as pd
import glob
import os

from movie import *

def readCSV(movies):
    #Lendo os arquivos de grupos
    path = os.getcwd()
    filenames = glob.glob(os.path.join(path, "*.csv"))

    print(path)

    #percorrendo os arquivos .csv de definicao de grupos
    for file in filenames:
        try:
            # lendo arquivos .csv
            df = pd.read_csv(file)
            print(df)
            try:
                #percorrendo as colunas
                id = pd.read_csv(file).columns[0]
                name = pd.read_csv(file).columns[1]
                director = pd.read_csv(file).columns[2]
                actor = pd.read_csv(file).columns[3]
                supporting = pd.read_csv(file).columns[4]
                genre = pd.read_csv(file).columns[5]
                year = pd.read_csv(file).columns[6]
                imdbScore = pd.read_csv(file).columns[7]
                imgName = pd.read_csv(file).columns[8]
                newMovie = movie(id, name, director, actor, supporting, genre, year, imdbScore, imgName)
                print(newMovie)
                movies.append(newMovie)

                for j in range(len(df)):
                    id = df.iloc[j, 0]
                    name = df.iloc[j, 1]
                    director = df.iloc[j, 2]
                    actor = df.iloc[j, 3]
                    supporting = df.iloc[j, 4]
                    genre = df.iloc[j, 5]
                    year = df.iloc[j, 6]
                    imdbScore = df.iloc[j, 7]
                    imgName = df.iloc[j, 8]

                    newMovie = movie(id, name, director, actor, supporting, genre, year, imdbScore, imgName)

                    movies.append(newMovie)

            except:
                print("Nao foi possivel ler as informacoes do filme")
        except:
            print("Nao foi possivel ler o arquivo")


