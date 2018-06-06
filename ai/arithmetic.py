# coding=utf-8
"""
filename : tutorial_example_2_arithmetic.py
author: hu@daonao.com QQ: 443089607 weixin: huzhenghui weibo: http://weibo.com/443089607
category : tensorflow
title : python tensorflow学习笔记（二）算数
csdn blog url :
weibo article url :
weibo message url :
为了清晰直观展现python严格要求的缩进，请访问博客上博文
详细说明见源代码中的注释
"""

# standard import
import logging
import random

import tensorflow

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('start')

# 定义一个常数 CONSTANT_A
CONSTANT_A = tensorflow.constant(random.randint(-100, 100))
# 定义一个常数 CONSTANT_B
CONSTANT_B = tensorflow.constant(random.randint(-100, 100))
# 创建一个回话
SESSION = tensorflow.Session()
# 输出 CONSTANT_A
logging.debug('CONSTANT_A = %s', SESSION.run(CONSTANT_A))
# 输出 CONSTANT_B
logging.debug('CONSTANT_B = %s', SESSION.run(CONSTANT_B))
# 计算 CONSTANT_A + CONSTANT_B
logging.debug('CONSTANT_A + CONSTANT_B = %s', SESSION.run(CONSTANT_A + CONSTANT_B))
# 计算 CONSTANT_A * CONSTANT_B
logging.debug('CONSTANT_A * CONSTANT_B = %s', SESSION.run(CONSTANT_A * CONSTANT_B))
#end of file