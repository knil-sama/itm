import typing
import numpy as np
from PIL import
import backend
from path

def grayscale(context):
    list_gray_filepath = []
    for in:
        list_gray_filepath.append()

def img_to_gray(filepath:str):
    #https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
    img = Image.open(filepath,'r')
    rgb = np.nparray(img)
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = np.mean([r,g,b],axis=0)
    # fromarray(gray, "L") not working
    gray_img = Image.fromarray(gray)
    gray_img=gray_img.convert("L")
    gray.save(os.pathformat="png")
    return gray_filepath

