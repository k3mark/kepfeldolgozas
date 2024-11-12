import cv2
import numpy as np
import random

# képmanipulációs rész implementálása

## A program a felhasználótól bekéri a kép teljes elérési útvonalát
# path = input('Kép elérési útvonala: ')
path = "./img/virág.JPG"
img = cv2.imread(path, cv2.IMREAD_COLOR)
img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2) #downscale
cv2.imshow('Original', img)
copy = img.copy()

## A program bekér a felhasználótól egy küszöbértéket, és a küszöbölést* követően első lépésként kimaszkolja azokat a részeket a szerkesztendő képről, amelyek az alábbi kritériumnak megfelelnek
# threshold = int(input('Küszöbérték: '))
threshold = 80
temp = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(temp)
ret, mask = cv2.threshold(h, threshold, 255, cv2.THRESH_BINARY)
mask = mask == 255

## Az adott pixelérték színértéke a küszöbérték kétszeresét nem haladja meg,
m1 = h < threshold * 2

## Az adott pixelérték szaturációs értéke a 50 és 170-as sávba
m2 = (s > 50) & (s < 170)

## Az adott pixelérték világossági értéke a 100 és 200-as sávba esik.
m3 = (v > 100) & (v < 200)

mask = mask & m1 & m2 & m3

## Fontos rész, hogy a maszkolás mellett ezeket a pixeleknek az indexeit is tárolja a program tetszőlegesen megválasztott adatstruktúrában (tömb, verem, stb.)
indexes = []
for i in range(len(mask)):
    for j in range(len(mask[i])):
        if mask[i][j]:
            indexes.append((i, j))


img[~mask] = [0, 0, 0]


## A program a törölt képrészeket feltölti a felhasználó által megadott háttérszín értékeivel.
# r = int(input('Red: '))
# g = int(input('Green: '))
# b = int(input('Blue: '))
r = 255
g = 0
b = 0

for i in range(0,img.shape[0]):
    for j in range(0,img.shape[1]):
        if np.array_equal(img[i,j,:],np.array([0,0,0])):
            img[i, j, :] = np.array([r,g,b])


for x,y in indexes:
    rand = random.random()
    if rand > 0.4:
        img[x, y] = copy[x, y]


# A program a maszkrégió alapján kiszámolja az első kép kontúrjait.
# XD


## A program lehetőséget biztosít az átmásolt pixelek és a kimaszkolt régiókon kívül eső pixelek értékeinek világosítására, és szaturációs értékeinek kompenzációjára, amelyet a felhasználótól olvas be
# satadd = int(input('Saturation: '))
# valadd = int(input('Value: '))
satadd = 100
valadd = 100
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
s[~mask] += np.uint8(satadd)
v[~mask] += np.uint8(valadd)
hsv = cv2.merge([h, s, v])
img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


cv2.imshow('Final', img)
cv2.waitKey(0)