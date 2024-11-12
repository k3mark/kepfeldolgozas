import cv2
import numpy as np

# Feladat: Képkinyerő rész implementálása

## A program a felhasználótól bekéri a szerkesztendő kép teljes elérési útvonalát, majd megnyitja ezt a képfájlt.
# path = input('Kép elérési útvonala: ')
path = "./img/virág.JPG"
img = cv2.imread(path, cv2.IMREAD_COLOR)
img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2) #downscale
cv2.imshow('Original', img)


## A program elvégzi automatikusan a szükséges képkorrekciós műveleteket.
### histogram equalization, elméletbe mehet bármikor
yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
img_equh = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
cv2.imshow('Equalized', img_equh)

### Elmosás, csak akkor ha zajos a kép
# img_blur = cv2.GaussianBlur(img, (3, 3), 0)
# img_blur = cv2.bilateralFilter(img, 9, 75, 75)
img_blur = cv2.medianBlur(img, 3)
cv2.imshow('Blured', img_blur)

### Élesítés, csak akkor ha homályos a kép
blur = cv2.GaussianBlur(img, (5, 5), 0)
img_sharp = cv2.addWeighted(img, 1.5, blur, -0.5, 0)
cv2.imshow('Sharp', img_sharp)


## A program a felhasználó által megadott érték alapján küszöbölést hajt végre.
## Kép típusa alaján kell eldönteni hogy H,S,V értékekre kell-e küszöbölni álltalába V az fasza
# threshold = int(input('Küszöbérték: '))
threshold = 80
temp = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(temp)
ret, mask = cv2.threshold(v, threshold, 255, cv2.THRESH_BINARY)
cv2.imshow('Thresholded Mask', mask)

## A program lehetőséget biztosít a felhasználó számára a kinyert rész színparamétereinek (színezet, színtelítettség és világosság) megadására.
# hueadd = int(input('Hue: '))
# satadd = int(input('Saturation: '))
# valadd = int(input('Value: '))
hueadd = 100
satadd = 50
valadd = 50
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
mask = mask == 255 # 255-ös értékeket True-ra, 0-ás értékeket False-ra állítja
h[mask] += np.uint8(hueadd)
s[mask] += np.uint8(satadd)
v[mask] += np.uint8(valadd)
hsv = cv2.merge([h, s, v])
img_final = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imshow('Final', img_final)

## A program eredményként kimenti a felhasználó által megadott elérési útvonalra a szerkesztett képet JPEG formátumban, 92%-os minőségi arányban.
# outpath = input('Kimeneti elérési útvonal: ')
outpath = "./img/virág_out.JPG"
cv2.imwrite(outpath, img_final, [int(cv2.IMWRITE_JPEG_QUALITY), 92])


cv2.waitKey(0)