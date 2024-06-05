import numpy as np
import cv2
from PIL import Image

def preprocess_image(img):
    #! Converts the image to grayscale image
    gray = cv2.cvtColor(src=np.array(img), code=cv2.COLOR_BGR2GRAY)
    #! Resizes the image
    resized = cv2.resize(src=gray, dsize=None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    #! Now apply adaptive thresholding which we testing in cv_concepts.ipynb
    processed_image = cv2.adaptiveThreshold(src=resized, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=61, C=11)
    
    return processed_image