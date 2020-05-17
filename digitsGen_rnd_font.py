import os
import numpy as np 
import pandas as pd 
from cv2 import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt 
from PIL import Image, ImageDraw, ImageFont
import random
import string

ROOT_DIR = os.getcwd()
DATA_DIR = os.path.join(ROOT_DIR, 'fonts_data')
# FONTS = [ font for font in os.listdir('/System/Library/Fonts/')]
FONTS = [r'/System/Library/Fonts/Avenir Next.ttc', 
        '/System/Library/Fonts/NewYork.ttf',
        '/System/Library/Fonts/NewYorkItalic.ttf',
        '/System/Library/Fonts/SFCompactDisplay.ttf',
        '/System/Library/Fonts/ArialHB.ttc',
        '/System/Library/Fonts/Symbol.ttf',
        '/System/Library/Fonts/AquaKana.ttc',
        '/System/Library/Fonts/SFCompactTextItalic.ttf',
        r'/System/Library/Fonts/Avenir Next Condensed.ttc',
        '/System/Library/Fonts/Avenir.ttc',
        '/System/Library/Fonts/Kohinoor.ttc',
        '/System/Library/Fonts/Menlo.ttc',
        '/System/Library/Fonts/Noteworthy.ttc',
        '/System/Library/Fonts/Thonburi.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W1.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W2.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc',
        r'/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc',
        r'/System/Library/Fonts/ヒラギノ明朝 ProN.ttc',
        r'/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc',
] 

def background_rnd_fill(background_img, fill_range=(32,127)):
    '''
    将背景画布按像素随机填充颜色
    background_img: pillow的Image对象
    fill_range: tuple类型，每个像素的颜色范围0~255，默认(32,127)
    '''
    background_filled = background_img.copy() # 为了不破坏原背景，这里用copy
    drawer = ImageDraw.Draw(background_filled) # 在Image对象上创建画笔对象
    width, height = background_img.size # 获取背景画布的尺寸
    for x in range(width):
        for y in range(height):
            drawer.point( (x,y), fill=(
                random.randint(fill_range[0], fill_range[1]),
                random.randint(fill_range[0], fill_range[1]),
                random.randint(fill_range[0], fill_range[1])
            ) )# 每个像素填充随机颜色
    return background_filled

def draw_text(background_img, text='0123456789', font=None, fill=(255,0,0)):
    '''
    在背景画布上画图，我进行了位置计算，使得字符在画布中能居中显示
    background_img: pillow的Image对象
    text: 要画的字符
    font: str类型，字体路径，默认为None
    fill: 画的字符的填充色，默认为(255,0,0)=red
    '''
    width, height = background_img.size # 获取背景画布的尺寸
    img = background_img.copy() # 为了不破坏原背景，这里用copy
    drawer = ImageDraw.Draw(img) # 在Image对象上创建画笔对象
    drawer.text((10, (height - font.size - 8) // 2), text, fill=fill,font=font)
    return img

def captcha_generator(character_set:str, font_set=None, save_path='./', size=(150,60),
                         style=((255, 0, 0), (255, 255, 255), 40, False, (32,127)), captcha_len=4):
    '''
    R.G.的验证码生成器
    character_set: 用于生成验证码的字符集，字符集以str类型传入
    font_set: 字体集，str类型，本机的字体路径，如'path/to/font.ttf'
    save_path: 验证码图片的保存位置，默认为当前文件夹
    size: 生成验证码图片的尺寸，tuple类型，格式：（长，宽)，默认（150, 60）
    style: 生成验证码的样式，tuple类型，格式：(text_color, background_color, text_size, rnd_background, fill_range), 
            _color均为三元tuple, text_size为int, rnd_background为bool用于控制是否把背景随机填色，默认不随机填色
            fill_range: tuple类型，每个像素的颜色范围0~255，默认(32,127)【fill_range仅当rnd_background=True时起作用】
    captcha_len: 要生成的验证码长度，即验证码字符个数
    '''
    # captcha_text = ''.join(random.sample(character_set, captcha_len)) # 这样生成的验证码中不会出现相同字符
    # captcha_text = ''.join([ random.choice(character_set) for i in range(captcha_len)]) # 验证码中可能出现相同字符
    captcha_text = character_set
    background_img = Image.new('RGB', size, style[1]) # 创建一个Image对象，new(mode, size, color=0) 
    my_font = ImageFont.truetype(font=font_set, size=style[2]) # 创建字体对象
    # 注意一点，之前用captcha库时候，font传入的是list类型，而这里传入的要是一个str类型
    if style[3]:
        background_img = background_rnd_fill(background_img, fill_range=style[4])
    captcha_img = draw_text(background_img, captcha_text, font=my_font, fill=style[0])
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    captcha_save_path = os.path.join(save_path, '{}_0.png'.format(captcha_text))
    i = 0
    while True:
        i += 1
        if os.path.exists(captcha_save_path): # 已经有样本，则在正确标签后面加_i, i标记重复次数
            captcha_save_path = os.path.join(save_path, '{}_{}.png'.format(captcha_text, i))
        else: # 不存在重名路径，则跳出
            break
    captcha_img.save(captcha_save_path, 'png')
    print('{}\n{}'.format(captcha_save_path, font_set))
    print('Captcha {} generated!'.format(captcha_text))
    return captcha_text

for font in FONTS:
    captcha_generator('0123456789', font_set=font, save_path='./digits_img', 
    size=(350, 80), captcha_len=10,style=((255, 0, 0), (255, 255, 255), 40, False, (32,127))
    )

# i = int(input('i= '))
# f = FONTS[i]
# captcha_generator('0123456789', font_set=f, save_path='./digits_img', 
#     size=(350, 80), captcha_len=10,style=((255, 0, 0), (255, 255, 255), 40, False, (32,127))
#     )