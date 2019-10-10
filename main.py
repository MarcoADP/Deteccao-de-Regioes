import cv2
import numpy as np
import queue


def read_image(file):
    return cv2.imread(file)


def show_imagem(img, title='Imagem Resultante'):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def is_fundo(ponto, fundo):
    return all(ponto == fundo)


def get_vizinho(coordenada, linha, coluna):
    return [coordenada[0] + linha, coordenada[1]+coluna]


def get_vizinhos_4(coordenada):
    lista = []
    lista.insert(0, get_vizinho(coordenada, 0, -1))
    lista.insert(0, get_vizinho(coordenada, 1, 0))
    lista.insert(0, get_vizinho(coordenada, 0, 1))
    lista.insert(0, get_vizinho(coordenada, -1, 0))
    return lista


def get_vizinhos_8(coordenada):
    lista = []
    lista.insert(0, get_vizinho(coordenada, -1, -1))
    lista.insert(0, get_vizinho(coordenada, 0, -1))
    lista.insert(0, get_vizinho(coordenada, 1, -1))
    lista.insert(0, get_vizinho(coordenada, 1, 0))
    lista.insert(0, get_vizinho(coordenada, 1, 1))
    lista.insert(0, get_vizinho(coordenada, 0, 1))
    lista.insert(0, get_vizinho(coordenada, -1, 1))
    lista.insert(0, get_vizinho(coordenada, -1, 0))

    return lista


def outside_image(coordenada, altura, largura):
    coordenada[0] < 0 or coordenada[0] > altura - 1 or coordenada[1] < 0 or coordenada[1] > largura - 1


def pixel_inutil(ponto_img1, ponto_img2, fundo):
    return is_fundo(ponto_img1, fundo) or not is_fundo(ponto_img2, fundo)

def busca_largura(coordenada, img, img2, vizinhanca, fundo):
    fila = queue.Queue()
    fila.put(coordenada)
    while not fila.empty():
        atual = fila.get()
        if outside_image(atual, img.shape[0], img.shape[1]) or pixel_inutil(img[atual[0]][atual[1]], img2[atual[0]][atual[1]], fundo):
            continue
        if vizinhanca == 4:
            vizinhos = get_vizinhos_4(atual)
        elif vizinhanca == 8:
            vizinhos = get_vizinhos_8(atual)

        for vizinho in vizinhos:
            fila.put(vizinho)

        img2[atual[0]][atual[1]] = img[atual[0]][atual[1]]

    return img2


def main(file='ex1.png', vizinhanca=4, fundo=0):
    img = read_image(file)
    img2 = np.zeros(img.shape, np.uint8)

    regiao = 0

    for linha in range(img.shape[0]):
        for coluna in range(img.shape[1]):
            if img[linha][coluna][0] > 0 :
                if (not is_fundo(img[linha][coluna], fundo)) and (is_fundo(img2[linha][coluna], fundo)):
                    img2 = busca_largura([linha, coluna], img, img2, vizinhanca, fundo)
                    regiao = regiao + 1
                    show_imagem(img2, "regioes: " + str(regiao))

    print("regioes => " + str(regiao))
    show_imagem(img2, "Total de " + str(regiao) + " regioes")


main(file='ex_diagonal.png', vizinhanca=4)
