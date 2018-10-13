# importare la librerie di python di OpenCV
import cv2

# np e un alias che punta alla libreria numpy
import numpy as np

# from sklearn.cluster import MiniBatchKMeans

# cattura fotogrammi dalla fotocamera
# cap = cv2.VideoCapture(0)
cap = cv2.imread("1.jpg")
# il ciclo viene eseguito se la cattura e stata inizializzata

# applica edge detaction
ris = cv2.Canny(cap, 100, 200)

# creo un array vuoto che mi serve per le altezze
misura = np.array([])

# prendo le misure del fotogramma
height, width = ris.shape

# creo una copia del fotogramma
ris1 = ris.copy()

# ciclo per larghezza e altezza per cercare il pixel del contorno
for x in range(width - 1):
    for h in range(height - 1):
        # indice del fotogramma e il primo pixel in alto a destra quindi devo ragionare al contrario
        # mi calcolo altezza del pixel dal basso e non dal alto
        hei = height - h - 1
        # cerco il pixel di contorno che e di colore bianco
        if ris1[hei, x] == 255:
            # riempio l'array vuoto con l'altezza del pixel che ho trovato
            misura = np.append(misura, int(hei))
            break
        else:
            # coloro i pixel che non sono di contorno fino al contorno
            ris1.itemset((hei, x), 50)
# genero 3 array (sinistro centrale destro)
misura = np.split(misura, [90, 220])

# calcolo le medie
media_sinistra = np.median(misura[0])
media_centrale = np.median(misura[1])
media_destra = np.median(misura[2])

# stampo le medie che ho trovato
print(media_sinistra, media_centrale, media_destra)

# stampa il suggerimento con l'altezza del pixel medio
if media_sinistra < media_centrale:
    if (media_sinistra < media_destra):
        print("vai a sinistra: ", media_sinistra)
    else:
        print("vai a destra: ", media_destra)
elif media_centrale < media_destra:
    print("continua dritto: ", media_centrale)
else:
    print("vai a destra: ", media_destra)

while (1):
    # legge i fotogrammi da una fotocamera
    # ret, frame = cap.read()

    # Mostra un'immagine originale catturata
    cv2.imshow('Original', cap)

    # Mostra un'immagine originale catturata
    cv2.imshow('ris', ris)

    cv2.imshow('ris1', ris1)

    # Attendi che il tasto Esc venga premuto per uscire
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
