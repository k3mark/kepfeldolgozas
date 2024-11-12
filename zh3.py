import cv2
import numpy as np

# Feladat: Képkinyerő rész implementálása

## A program a felhasználótól bekéri a szerkesztendő kép teljes elérési útvonalát, majd megnyitja ezt a képfájlt.
# path = input('Kép elérési útvonala: ')
path = "./text.png"
img = cv2.imread(path, cv2.IMREAD_COLOR)
img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4) #downscale
cv2.imshow('Original', img)


## A program elvégzi automatikusan a szükséges képkorrekciós műveleteket.
blur = cv2.GaussianBlur(img, (5, 5), 0)
img_sharp = cv2.addWeighted(img, 1.5, blur, -0.5, 0)
cv2.imshow('Sharp', img_sharp)

## adaptív küszöbölés
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 4)
cv2.imshow('Adaptive Thresholded Image', thresh)

## A program lehetőséget biztosít a felhasználó számára a kinyert szöveg színének** megadására.
# r = int(input('Red: '))
# g = int(input('Green: '))
# b = int(input('Blue: '))
r = 255
g = 0
b = 0
img[thresh == 0] = [b, g, r]
cv2.imshow('Final Image', img)

##  A program eredményként kimenti a felhasználó által megadott elérési útvonalra a szerkesztett képet JPEG formátumban, 92%-os minőségi arányban.
# outpath = input('Kimeneti elérési útvonal: ')
outpath = "./text_out.png"
cv2.imwrite(outpath, img, [int(cv2.IMWRITE_JPEG_QUALITY), 92])




cv2.waitKey(0)