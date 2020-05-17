## 项目工程文件介绍

注：所有带`pre`的notebook都是同名无`pre`的详细未整理版，是边思考边调试写的笔记文件，无`pre`的是改名字最终整理版；此外，同名`.py`文件内容和notebook一致，只是跑`.py`文件比跑notebook比较舒服【因此我的习惯是，notebook用于展示代码思路，脚本文件用于正式运行】

### 文件介绍

+ `captcha_dataGen.ipynb`: 使用captcha库来生成验证码，正式实验抛弃使用这个文件；`data_via_captcha文件夹`由本文件生成
+ `captcha_dataGen_RG.ipynb`: 用pillow直接自己验证码，默认生成工整排列的4位数字验证码，便于用cv分割；`data_via_RG文件夹`由此文件生成
+ `digitsGen_rnd_font.ipynb`: 基于上述文件，遍历本机字体，生成不同字体的`0123456789`样本，由于有些字体是没有数字或者数字是奇怪形状，因此生成之后，要手动删掉这些样本；`digits_img文件夹`由本文件生成
+ `captcha_detach.ipynb`：将验证码中的每个字符分割提取，并形成每个字符的打标数据集。（注：当提取对象是由`digitsGen_rnd_font.ipynb`生成的数字图像时，代码有些许调整，调整见脚本`digits_detach.py`);`characters文件夹`由此notebook生成，`digits_data文件夹`由`digits_detach.py`生成
+ `debug.py`、`test.py`分别是调试和测试部分代码时用的，不对工程主体产生影响



### 其余文件夹介绍

+ `data_old`：没有调整过字体的时候，直接用captcha库默认函数生成的4位数字验证码，会有倾斜和连体（两个字符凑在一起），由于倾斜和字符连体增加了分割难度，故暂时我没处理这种情况
+ `character_old`：由调整了字体后，用captcha库生成的验证码detach出的各个字符样本，由于生成的验证码有倾斜和连体，故这里提取出来会有 标签不对、同意字符样本中出现多个连体字符等错误样本，所以为了简化分割和识别难度，我才弃用captcha库，自己写验证码生成代码

+ `imgaes`：老师给的几个验证码图片和我自己增加的一些验证码