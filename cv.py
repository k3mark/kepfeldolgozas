import cv2
import numpy as np
from matplotlib import pyplot as plt

inputPath = "./test.webp"
img = cv2.imread(inputPath)
# img =cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5) #downscale the image by half

## Színes kép szürkeárnyalatosra konvertálása
def feladat1():
    imgColor = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Colored', imgColor)
    cv2.imshow('Gray', imgGray) 


## Piros-50 Zöld=10 Kék*2
def feladat2():
    imgColor = img.copy()
    imgColor[:, :, 0] = imgColor[:, :, 0] - 50
    imgColor[:, :, 1] = 10
    imgColor[:, :, 2] = imgColor[:, :, 2] * 2
    cv2.imshow('Color Image', imgColor)

## Szürkeárnyalatos kép első 10 sorának értékei és gyakorisága
def feladat3():
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    firstTenRows = imgGray[0:10, :]
    grascaleValues = firstTenRows.flatten()
    grayscaleMap = {}
    for value in grascaleValues:
        if value in grayscaleMap:
            grayscaleMap[value] += 1
        else:
            grayscaleMap[value] = 1

    for key, value in grayscaleMap.items():
        print(f'{key} : {value}')
    cv2.imshow('Gray Image', imgGray)

## HSV konverzió
def feladat4():
    imgColor = img.copy()
    imgHSVColor = cv2.cvtColor(imgColor, cv2.COLOR_RGB2HSV)
    cv2.imshow('HSV Image', imgHSVColor)

## Kép mentése PNG tömörítéssel 
def feladat5():
    imgColor = img.copy()
    cv2.imwrite('color.png', imgColor, [cv2.IMWRITE_PNG_COMPRESSION, 9])

## Piros elemek maszkolása és eltolása
def feladat6():
    imgColor = img.copy()
    imgHSV = cv2.cvtColor(imgColor, cv2.COLOR_RGB2HSV)
    channels = list(cv2.split(imgHSV))
    hue = channels[0]
    
    h1 = hue >= 100
    h2 = hue <= 120
    mask = h1 & h2

    hue[mask] += 40

    channels[0] = hue
    out = cv2.merge(channels)
    out = cv2.cvtColor(out, cv2.COLOR_HSV2RGB)
    cv2.imshow('Red Image', out)

## Histogram normalizálás és hisztogramok megjelenítése
def feladat7():
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.subplot(121)
    plt.hist(imgGray.ravel(),256,[0,256])
    imgGray = cv2.equalizeHist(imgGray)
    plt.subplot(122)
    plt.hist(imgGray.ravel(),256,[0,256])
    plt.show()

## Histogram normalizálás
def feladat8():
    imgColor = img.copy()
    imgHSV = cv2.cvtColor(imgColor, cv2.COLOR_RGB2HSV)
    channels = list(cv2.split(imgHSV))
    value = channels[2]
    cv2.equalizeHist(value, value)
    out = cv2.merge(channels)
    out = cv2.cvtColor(out, cv2.COLOR_HSV2RGB)
    cv2.imshow('Equalized Image', out)


## Piros és zöld csatorna felcserélése
def feladat9():
    imgColor = img.copy()
    red = imgColor[:, :, 2].copy()
    green = imgColor[:, :, 1].copy()
    imgColor[:, :, 1] = red*0.7
    imgColor[:, :, 2] = green
    cv2.imshow('Swapped Image', imgColor)


## Zászló élesítése és háttér elhomályosítása
def feladat10():
    img = cv2.imread("./flag.jpg")
    imgHSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h,s,v = cv2.split(imgHSV)

    ## create mask for green colors
    mask = (h>=30)&(h<=80)
    invertedMask = ~mask

    ## show mask
    maskShow = mask.astype(np.uint8)*255
    cv2.imshow('Mask', maskShow)
    
    ## Create blured and sharpened images
    blurred = cv2.GaussianBlur(img, (15, 15), 0)
    sharpened = cv2.addWeighted(img, 2, blurred, -1, 0)

    ## Apply blurred version on the mask
    final = img.copy()
    final[mask] = sharpened[mask]
    final[invertedMask] = blurred[invertedMask]
    cv2.imshow('Original Image', img)
    cv2.imshow('Final Image', final)

def feladat11():
    ## CT kép globalis küszöbölése
    imgCT = cv2.imread("./ct.png")
    imgGray = cv2.cvtColor(imgCT, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(imgGray, 92, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('Thresholded Image', thresh)

    ## adaptív küszöbölés
    imgText = cv2.imread("./text.png")
    imgGray = cv2.cvtColor(imgText, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow('Adaptive Thresholded Image', thresh)


if __name__ == '__main__':
    feladat1()
    feladat2()
    feladat3()
    feladat4()
    feladat5()
    feladat6()
    feladat7()
    feladat8()
    feladat9()
    feladat10()
    feladat11()
    cv2.waitKey(0)
    cv2.destroyAllWindows()