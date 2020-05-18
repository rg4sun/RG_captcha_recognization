import os
import numpy as np 
import pandas as pd 
from cv2 import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt 

ROOT_DIR = os.getcwd()
DATA_DTR = os.path.join(ROOT_DIR, 'captcha_test_data')
CHARACTER_DIR = os.path.join(ROOT_DIR, 'character_test_data')

# 为了方便图片直接显示在jupyter中，cv的imshow不能直接在jupyter中显示
# 为了用matplotlib显示（ 不能用plt.show()，要用plt.imshow() ）
# 由于CV的通道是BGR顺序，而matpotlib是 RGB顺序，这里要做通道转换
# 方法一
def bgr2rgb_v2(img):
    # 用cv自带的分割和合并函数
    B,G,R = cv.split(img)
    return cv.merge([R,G,B])
# 方法二
def bgr2rgb(img):
    # 直接用python切片特性，[start: end: step], 这里start end为空，则默认遍历全部，step为-1则倒序遍历
    return img[:, :, ::-1]

def genNeedImg(img_path, img_type='binary', binary_therhold=127, 
               binary_reverse=False, size=None, save=False, path='./'):
    '''
    用于生成指定大小的灰度图或二值图, img_path为图像路径
    type为标志转换类型，默认为binary，可选的值为binary或gray
    binary_therhold为二值图划分阈值，默认127（即大于127的像素设置为255，否则置0）
    binary_reverse默认为False，True时黑白颠倒（即大于127的像素设置为0，否则置255）
    size为tuple类型，用于指定生成图像的尺寸, 如：(512,512)，默认为None表示输出原图像尺寸
    save为保存标志，默认为False，为true时将生成的图保存到path(默认为当前文件夹)
    '''
    img_raw = cv.imread(img_path)
    if size != None: # 调整图像尺寸
        img_raw= cv.resize(img_raw,size)
    img_gray = cv.cvtColor(img_raw,cv.COLOR_RGB2GRAY) # 转换颜色空间为灰度
    # Add some extra padding around the image
    # img_gray = cv.copyMakeBorder(img_gray, 8, 8, 8, 8, cv.BORDER_REPLICATE)
    img_name = img_path[9:].split('.')[0] # 获取图像原始名称
    if img_type == 'gray': # 生成灰度图
        if save:
            cv.imwrite(os.path.join(path,'{}_gray.bmp'.format(img_name)),img_gray)
            print('Gray image saved at {}'.format(os.path.join(path,'{}_gray.bmp'.format(img_name))))
        else:
            print('Gray image generated!')
            return img_gray
    else: # 生成二值图
        if binary_reverse:
            ret, img_binary = cv.threshold(img_gray,binary_therhold,255,cv.THRESH_BINARY_INV) #反二进制阈值化
        else:
            ret, img_binary = cv.threshold(img_gray,binary_therhold,255,cv.THRESH_BINARY)# 二进制阈值化
        if save:
            cv.imwrite(os.path.join(path,'{}_binary.bmp'.format(img_name)),img_binary)
            print('threshold:{}'.format(ret)) # 输出转换阈值
            print('Binary image savd at {}'.format(os.path.join(path,'{}_binary.bmp'.format(img_name))))
        else:
            print('Binary image generated!')
            print('threshold:{}'.format(ret)) # 输出转换阈值
            return img_binary

def captcha_character_detach(captcha_img_path, characters_save_path='./', captcha_len=4):
    captcha_img_basename = os.path.basename(captcha_img_path) # 从路径中提取带后缀文件名，如 '0415.png'
    captcha_text = os.path.splitext(captcha_img_basename)[0] # ['0415', 'png']
    img_gray = cv.imread(captcha_img_path, cv.IMREAD_GRAYSCALE) # 灰度图读入
    img_binary = genNeedImg(captcha_img_path, img_type='binary', binary_therhold=127, binary_reverse=True) # 直接调用genNeedImg生成二值图
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) # 划分字符轮廓
    # 由于直接划分的轮廓太多了（我换了字体后好像不会划分很多），这里考虑记录每个每个轮廓的数据，然后取 wxh （长x宽，即面积）的top4
    boundings = [cv.boundingRect(contour) for contour in contours] # 获取每个轮廓的信息，(x,y,width,height) x,y为轮廓最左上角坐标
    boundings.sort(key=lambda tuple_x: tuple_x[2]*tuple_x[3], reverse=True) # lamdba传入的就是计算每个轮廓的面积，然后按面积大小降序排序
    if len(boundings) < captcha_len: # 获取到的轮廓小于4，则说明没有把4个字符都区分开来
        print('Bondings less then 4, captcha discarded!')
        return # 直接结束，丢弃这个验证码样本
    '''
    # 下面开始画矩形分割框，这部分其实用不到，只是为了调试看画的样子
    # -----------------------------------------------------------------------------------------
    temp_img = cv.imread(captcha_img_path, cv.IMREAD_UNCHANGED) # 以原始格式读入图片
    temp_img = bgr2rgb(temp_img) # 通道转换
    for bounding in boundings[:4]: # 取面积最大的前4个轮廓
        x, y, width, height = bounding
        img_addBox = cv.rectangle(temp_img, (x,y), (x + width, y + height), (0, 255, 0), 1)
    plt.imshow(img_addBox, cmap='gray')
    # ------------------------------------------------------------------------------------------
    '''
    boundings_save = sorted(boundings[:captcha_len], key=lambda tuple_x: tuple_x[0]) # 按轮廓的x坐标大小排序，tuple_x=(x,y,width,height) 
    character_splited = []
    for character_bounding, character_text in zip(boundings_save, captcha_text):
        x, y, width, height = character_bounding
        margin = 2 # 提取单个字符的时候，在获取的轮廓拓宽margin个像素，因为findContours()的轮廓可能很紧凑
        character_img = img_gray[y - margin:y + height + margin, x - margin:x + width + margin]
        if not os.path.exists(characters_save_path): # 如果要保存的路径不存在就创建该路径目录
            os.makedirs(characters_save_path)
        character_path = os.path.join(characters_save_path, '{}_0.png'.format(character_text))
        i = 0
        while True:
            i += 1
            if os.path.exists(character_path): # 该字符已经有样本，则在正确标签后面加_i, i标记重复次数
                character_path = os.path.join(characters_save_path, '{}_{}.png'.format(character_text, i))
            else: # 不存在重名路径，则跳出
                break
        cv.imwrite(character_path, character_img)
        character_splited.append(character_img)
    print('Character detached from captcha, character has been saved at {}'.format(characters_save_path))
    return character_splited


captchas = [ os.path.join(DATA_DTR, img_name) for img_name in os.listdir(DATA_DTR)] 
captchas.sort() # 升序，注意不能 listA = listA.sort(), sort没有返回值
for captcha in captchas:
    captcha_character_detach(captcha, CHARACTER_DIR, captcha_len=4)