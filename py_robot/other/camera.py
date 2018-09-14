#############################################################################
#############################################################################
###                                                                       ###
### Programma OpenCV per eseguire il rilevamento dei bordi in tempo reale ###
###                                                                       ###
#############################################################################
#############################################################################
#!/usr/bin/env python

# importare la librerie di python di OpenCV
import cv2

# np è un alias che punta alla libreria numpy
import numpy as np

# cattura fotogrammi dalla fotocamera
cap = cv2.VideoCapture(0)

# il ciclo viene eseguito se la cattura è stata inizializzata
while (1):

    # legge i fotogrammi da una fotocamera
    ret, frame = cap.read()

    # convertire BGR in HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # definire l'intervallo di colore rosso in HSV
    lower_red = np.array([30, 150, 50])
    upper_red = np.array([255, 255, 180])

    # creare un bordo colore rosso HSV e un immagine HSV di soglia
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Maschera bitwise e immagine originale
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Mostra un'immagine originale catturata
    cv2.imshow('Original', frame)

    # trova i bordi nell'immagine dell'immagine di input e
    # li contrassegna nei bordi della mappa di output
    edges = cv2.Canny(frame, 100, 200)

    # Mostra i bordi in una cornice
    cv2.imshow('Edges', edges)

    # Attendi che il tasto Esc venga premuto per uscire
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# Chiudi la finestra
cap.release()

# Disabilita l'eventuale utilizzo della memoria associata
cv2.destroyAllWindows()