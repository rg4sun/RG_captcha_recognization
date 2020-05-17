import os
import numpy as np 
import pandas as pd 
from cv2 import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt 
from captcha.image import ImageCaptcha # 验证码生成库
import random
import string
from PIL import Image, ImageDraw, ImageFont

def genNeedImg(img_path, img_type='binary', binary_therhold=127, size=None, save=False, path='./'):
    '''
    用于生成指定大小的灰度图或二值图, img_path为图像路径
    type为标志转换类型，默认为binary，可选的值为binary或gray
    binary_therhold为二值图划分阈值，默认127（即大于127的像素设置为255，否则置0）
    size为tuple类型，用于指定生成图像的尺寸, 如：(512,512)，默认为None表示输出原图像尺寸
    save为保存标志，默认为False，为true时将生成的图保存到path(默认为当前文件夹)
    '''
    img_raw = cv.imread(img_path)
    if size != None: # 调整图像尺寸
        img_raw= cv.resize(img_raw,size)
    img_gray = cv.cvtColor(img_raw,cv.COLOR_RGB2GRAY) # 转换颜色空间为灰度
    img_name = img_path[9:].split('.')[0] # 获取图像原始名称
    if img_type == 'gray': # 生成灰度图
        if save:
            cv.imwrite(os.path.join(path,'{}_gray.bmp'.format(img_name)),img_gray)
        else:
            return img_gray
        print('Gray image generated!')
    else: # 生成二值图
        ret, img_binary = cv.threshold(img_gray,127,255,cv.THRESH_BINARY)
        if save:
            cv.imwrite(os.path.join(path,'{}_binary.bmp'.format(img_name)),img_binary)
        else:
            return img_binary
        print('Binary image generated!')
        print('threshold:{}'.format(ret)) # 输出转换阈值

image = Image.new('RGB', (300,150), 'black')
drawer = ImageDraw.Draw(image)
drawer.text()
