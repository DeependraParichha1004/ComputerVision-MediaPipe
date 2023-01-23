import cv2
import time
import os
import numpy as np
import handdetectormodule as htm

wCam, hCam = 640, 480
folder='images'
list=os.listdir(folder)
print(list)
# cap = cv2.VideoCapture(0)
for i in range(6):
    img=cv2.imread(f'{folder}/{list[i]}')

    print(np.array(img).shape)