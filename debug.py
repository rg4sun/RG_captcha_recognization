import os
import numpy as np 
import pandas as pd 
from cv2 import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split

ROOT_DIR = os.getcwd()
# IMG_DTR = os.path.join(ROOT_DIR, 'images')
DATA = os.path.join(ROOT_DIR, 'characters')

target_imgs = [ os.path.join(DATA, img_name) for img_name in os.listdir(DATA)] 
target_imgs.sort() # 升序，注意不能 listA = listA.sort(), sort没有返回值

def gen_data_set(captcha_imgs_folder):
    '''
    此函数用于创建 样本集和对应标签集合,返回的数据集是list类型
    '''
    target_imgs = [ os.path.join(captcha_imgs_folder, img_name) 
                    for img_name in os.listdir(captcha_imgs_folder)] 
    target_imgs.sort() # 升序，注意不能 listA = listA.sort(), sort没有返回值
    data_set, label_set = [], []
    for captcha in target_imgs:
        img = cv.imread(captcha, cv.IMREAD_GRAYSCALE) # 以灰度图读入验证码/单个字符的图
        img = cv.resize(img, (20,20)) # 调整尺寸到20x20
        img = img.reshape(400,)  # reshape成一维数组（sklearn用kNN时需要的格式）
        data_set.append(img)
        label_set.append(os.path.basename(captcha)[0])
    # return np.array(data_set), np.array(label_set)
    # 不返回np数组是因为，np数组索引是跟随的，就是说用了之后的split数据集后，索引并不重置顺序，测试见后一个cell
    return data_set, label_set

data_set, label_set = gen_data_set(DATA)


X_train, X_test, y_train, y_test = train_test_split(data_set, label_set, test_size=0.25, random_state=40)

def RG_kNN_classifier(feature_set_train, label_set_train, feature_set_test, k=3):
    '''
    所有的feature集合中的图像矩阵需要reshape成一维数组（传入前特征工程需要把图像先resize成20x20再reshape成（400,））
    feature_set_train, label_set_train, feature_set_test都必须是np.array
    '''
    distances = []
    for test_feature in feature_set_test:
        for train_feature in feature_set_train:
            distances.append(
                np.sqrt(np.sum(np.square(test_feature - train_feature)))
            )
    topK = np.argsort(distances)[-k:][::-1] # [-k:]是提取最后k个（因为argsort是升序排序）,[::-1]则是将其反序
    return label_set_train[list(topK)] # 返回最接近的k个预测值

print(RG_kNN_classifier(X_train,y_train,X_test, k=3))