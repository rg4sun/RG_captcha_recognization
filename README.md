## 项目工程文件介绍

注：所有带`pre`的notebook都是同名无`pre`的详细未整理版，是边思考边调试写的笔记文件，无`pre`的是该名字最终整理版；此外，同名`.py`文件内容和notebook一致，只是跑`.py`文件比跑notebook比较舒服【因此我的习惯是，notebook用于展示代码思路，脚本文件用于正式运行】

### 文件介绍

+ `captcha_dataGen.ipynb`: 使用captcha库来生成验证码，正式实验抛弃使用这个文件；`data_via_captcha文件夹`由本文件生成
+ `captcha_dataGen_RG.ipynb`: 用pillow直接自己验证码，默认生成工整排列的4位数字验证码，便于用cv分割；`data_via_RG文件夹`由此文件生成
+ `digitsGen_rnd_font.ipynb`: 基于上述文件，遍历本机字体，生成不同字体的`0123456789`样本，由于有些字体是没有数字或者数字是奇怪形状，因此生成之后，要手动删掉这些样本；`digits_img文件夹`由本文件生成
+ `captcha_detach.ipynb`：将验证码中的每个字符分割提取，并形成每个字符的打标数据集。（注：当提取对象是由`digitsGen_rnd_font.ipynb`生成的数字图像时，代码有些许调整，调整见脚本`digits_detach.py`);`characters文件夹`由此notebook生成，`digits_data文件夹`由`digits_detach.py`生成
+ `debug.py`、`test.py`分别是调试和测试部分代码时用的，不对工程主体产生影响
+ `captcha_recognization.ipynb`: 验证码识别的notebook，是最终的文件，识别的时候分了两次，第一次是将所有验证码打散成单个字符得到字符测试集，然后对测试集进行识别并计算正确率；第二次，是对每个4位数的验证码进行直接识别，并计算所有验证码的识别率（判断对了几个验证码）



### 其余文件夹介绍

+ `data_old`：没有调整过字体的时候，直接用captcha库默认函数生成的4位数字验证码，会有倾斜和连体（两个字符凑在一起），由于倾斜和字符连体增加了分割难度，故暂时我没处理这种情况
+ `character_old`：由调整了字体后，用captcha库生成的验证码detach出的各个字符样本，由于生成的验证码有倾斜和连体，故这里提取出来会有 标签不对、同意字符样本中出现多个连体字符等错误样本，所以为了简化分割和识别难度，我才弃用captcha库，自己写验证码生成代码
+ `imgaes`：老师给的几个验证码图片和我自己增加的一些验证码

###  快速上手

由于我写这个工程文件是不断整理思路、不断调试的过程，因此产生了很多文件。有些文件可能对工程本身不是很重要，但是记录了我一个学习和思考的过程，因此，我并没有删除这些文件。考虑到未来某一天可能有人会查阅此工程（maybe吧，希望这个工程文件能对查阅者起到一定帮助），为了便于查阅者快速上手，这里简要讲一下，这些文件的阅读顺序：

+ 所有的pre文件都比较乱，可以直接阅读不带pre的同名文件
+ Step1: 用 [digitsGen_rnd_font.py](./digitsGen_rnd_font.py) or [digitsGen_rnd_font.ipynb](./digitsGen_rnd_font.ipynb) 生成不同字体的数字序列样本（0-9，一串字符），所有的数字序列图片保存在 digits_img 文件夹
+ Step2: 用 [digits_detach.py](./digits_detach.py) 遍历 digits_img文件夹，将所有数字序列图分割提取出每个单个字符，以此生成训练集，保存在digits_data文件夹
+ Step3: 用 [captcha_dataGen_RG.py](./captcha_dataGen_RG.py) 生成四位数的验证码集（待识别的），保存在captcha_test_data文件夹，用作测试集
+ Step4: 用 [captcha_detach.py](./captcha_detach.py) 对step3中的每个验证码进行单个字符的分割，此分割其实对识别验证码不是必须的，只是下一步的文件中对单个字符的识别率计算有用
+ Step5: 用 [captcha_recognization.ipynb](./captcha_recognization.ipynb) 对Step3中的验证码进行识别

### 注：

captcha_recognization_image.ipynb识别率不高，其实很正常，因为这些图有很多噪点并且分割之后的大小不一致（就是字符的边缘可能会有很多误差），并且最本质的问题是，这些提供的图不具有明显的格式特征（比如一个网站的验证码应该会有明显的某种格式特征），因此会导致识别效果不好

但是，如果是针对 “验证码识别“ 这个问题背景，我觉得一个比较好的思路是：

+ 先大量获取该网站的验证码，得到一个训练集
+ 然后对该训练集进行训练
+ 再对该网站的验证码进行测试

这样，训练会更加有针对性，即对该网站的验证码格式进行训练，而非拿别的和该网站验证码格式、字体千差万别的数据进行训练

所以，我的captcha_recognization.ipynb文件，就是按以上思路来模拟验证码打码