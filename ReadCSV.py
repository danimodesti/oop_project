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
from MovieGame import *
from UserGame import User
from sort import *

RANKING_LEN = 5

def readMovieCSV(movies):
    #Lendo os arquivos de grupos
    path = os.getcwd()
    filenames = glob.glob(os.path.join(path, "*.csv"))

    #percorrendo os arquivos .csv de definicao de grupos
    for file in filenames:
        try:
            # lendo arquivos .csv
            df = pd.read_csv(file)
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
                curiosity = pd.read_csv(file).columns[9]
                runTime = pd.read_csv(file).columns[10] # duracao
                rating = pd.read_csv(file).columns[11] # classificacao indicativa
                oscar = pd.read_csv(file).columns[12]
                level = pd.read_csv(file).columns[13]
                newMovie = Movie(id, name, director, actor, supporting, genre, year, imdbScore, imgName, curiosity, runTime, rating, oscar, level)
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
                    curiosity = df.iloc[j, 9]
                    runTime = df.iloc[j, 10]
                    rating = df.iloc[j, 11]
                    oscar = df.iloc[j, 12]
                    level = df.iloc[j, 13]

                    newMovie = Movie(id, name, director, actor, supporting, genre, year, imdbScore, imgName, curiosity, runTime, rating, oscar, level)

                    movies.append(newMovie)

            except:
                print("Nao foi possível ler as informações do filme")
        except:
            print("Nao foi possível ler o arquivo")

def addUserNameCSV(user):
    if type(user) is User:
        rankingList = readRankingCSV()
        csv_size = len(rankingList)

        if len(rankingList) != 0:
            last_user = rankingList.pop() # Retira o ultimo lugar para comparar
            
            if csv_size < RANKING_LEN:
                rankingList.append(last_user)

        if csv_size < RANKING_LEN or (len(rankingList) != 0 and int(last_user.getTotalScore()) < int(user.getTotalScore())): # Se o ultimo lugar for Menor que o novo usuario
            rankingList.append(user)
            insertion_sort(rankingList)
                    
            with open('ranking/ranking.csv', 'w', newline='\n', encoding='UTF8') as f:
                writer = csv.writer(f)

                for userR in rankingList:

                    name = userR.getName()
                    score = userR.getTotalScore()
                    rankingName = [name,score]
                    # escreve nome do usuario e seu respectivo score no csv de ranking
                    writer.writerow(rankingName)
            
            f.close()
        
       
def readRankingCSV():
    f = open("ranking/ranking.csv", "r")
    content = f.readlines()
    l = []
    if len(content) != 0:
        for i in range(len(content)):
            s = content[i].split(',')

            readUser = User(name = s[0], totalScore = s[1].replace('\n',''))
            l.append(readUser)

    f.close()
    return l
