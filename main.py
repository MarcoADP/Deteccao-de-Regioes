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


def get_vizinhos_4(coordenada):
    lista = []
    lista.insert(0, [coordenada[0], coordenada[1]-1])
    lista.insert(0, [coordenada[0]+1, coordenada[1]])
    lista.insert(0, [coordenada[0], coordenada[1]+1])
    lista.insert(0, [coordenada[0]-1, coordenada[1]])
    #[4,5]
    #[ponto[0] + i, ponto[1]+j]
    return lista


def get_vizinhos_8(coordenada):
    lista = []
    lista.insert(0, [coordenada[0]-1, coordenada[1]-1])
    lista.insert(0, [coordenada[0], coordenada[1]-1])
    lista.insert(0, [coordenada[0]+1, coordenada[1]-1])
    lista.insert(0, [coordenada[0]+1, coordenada[1]])
    lista.insert(0, [coordenada[0]+1, coordenada[1]+1])
    lista.insert(0, [coordenada[0], coordenada[1]+1])
    lista.insert(0, [coordenada[0]-1, coordenada[1]+1])
    lista.insert(0, [coordenada[0]-1, coordenada[1]])

    #[4,5]
    #[ponto[0] + i, ponto[1]+j]
    return lista


def busca_largura(coordenada, img, img2, vizinhanca, fundo):
    fila = queue.Queue()
    fila.put(coordenada)
    #print(fila)
    while not fila.empty():
        atual = fila.get()
        #print(atual)
        if atual[0] < 0 or atual[0] > img.shape[0]-1 or atual[1] < 0 or atual[1] > img.shape[1]-1 or is_fundo(img[atual[0]][atual[1]], fundo) or not is_fundo(img2[atual[0]][atual[1]], fundo):
            print("falha :> " + str(atual))
            continue
        print("ok :> " + str(atual))
        if vizinhanca == 4:
            vizinhos = get_vizinhos_4(atual)
        elif vizinhanca == 8:
            vizinhos = get_vizinhos_8(atual)

        for vizinho in vizinhos:
            fila.put(vizinho)

        img2[atual[0]][atual[1]] = img[atual[0]][atual[1]]

    return img2


def main(file='ex1.png', fundo=0, vizinhanca=4):
    img = read_image(file)
    #img2 = np.full(img.shape, fundo)
    #img2 = np.zeros(img.shape)
    img2 = np.zeros(img.shape, np.uint8)

    regiao = 0

    for linha in range(img.shape[0]):
        for coluna in range(img.shape[1]):
            if img[linha][coluna][0] > 0 :
                if (not is_fundo(img[linha][coluna], fundo)) and (is_fundo(img2[linha][coluna], fundo)):
                    img2 = busca_largura([linha, coluna], img, img2, vizinhanca, fundo)
                    regiao = regiao + 1
                    show_imagem(img2)

    print("regioes => " + str(regiao))
    show_imagem(img2)


main()
