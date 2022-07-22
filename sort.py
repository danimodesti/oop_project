from UserGame import *

def insertion_sort(list):

    # Do segundo elemento da list ate o ultimo
    for i in range(1, len(list)):
        # Queremos posicionar a chave no lugar correto da list
        key = list[i]

        # Para testar posicao anterior a da chave atual
        j = i - 1

        # Procurando posicao correta do elemento chave atual,
        # verificando se a chave eh menor que o elemento mais 
        # a esquerda
        while j >= 0 and key > list[j]:
            # Se entrou aqui, trocar posicoes, pois a 
            # comparacao mostrou que a chave eh menor que 
            # o valor na posicao j
            list[j + 1] = list[j]
            j -= 1

        # Agora a chave esta na posicao correta
        list[j + 1] = key

    return list