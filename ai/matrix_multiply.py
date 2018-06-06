# coding=utf-8

"""
filename : tutorial_example_4_matrix_multiply.py
author: hu@daonao.com QQ: 443089607 weixin: huzhenghui weibo: http://weibo.com/443089607
category : tensorflow
title : python tensorflow学习笔记（四）矩阵乘法
csdn blog url :
weibo article url :
weibo message url :
为了清晰直观展现python严格要求的缩进，请访问博客上博文
详细说明见源代码中的注释
"""

import logging
import random

import tensorflow

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('start tensorflow tutorial example 4 matrix multiply')

# 定义一个1x2的矩阵常量
MATRIX_LEFT = tensorflow.constant([[random.random(), random.random()]])
# 定义一个2x1的矩阵常量
MATRIX_RIGHT = tensorflow.constant([[random.random()],
                                    [random.random()]])

# 1x2的矩阵乘2x1的矩阵
PRODUCT_LEFT_RIGHT = tensorflow.matmul(MATRIX_LEFT, MATRIX_RIGHT)
# 2x1的矩阵乘1x2的矩阵
PRODUCT_RIGHT_LEFT = tensorflow.matmul(MATRIX_RIGHT, MATRIX_LEFT)
# 创建一个会话
SESSION = tensorflow.Session()
# 显示1x2矩阵
logging.debug('MATRIX_LEFT : \n%s', SESSION.run(MATRIX_LEFT))
# 显示2x1矩阵
logging.debug('MATRIX_RIGHT : \n%s', SESSION.run(MATRIX_RIGHT))
# 显示1x2的矩阵乘2x1的矩阵的结果，是1x1矩阵
logging.debug('MATRIX_LEFT x MATRIX_RIGHT : \n%s', SESSION.run(PRODUCT_LEFT_RIGHT))
# 显示2x1的矩阵乘1x2的矩阵的结果，是2x2矩阵
logging.debug('MATRIX_RIGHT x MATRIX_LEFT : \n%s', SESSION.run(PRODUCT_RIGHT_LEFT))
# end of file

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('start tensorflow tutorial example 5 matrix multiply operation')

# 定义一个占位符矩阵，类型为float64，尺寸为一行两列
PLACEHOLDER_A = tensorflow.placeholder(tensorflow.float64, [1, 2])
# 定义一个占位符矩阵，类型为float64，尺寸为两行一列
PLACEHOLDER_B = tensorflow.placeholder(tensorflow.float64, [2, 1])
# 定义一个矩阵乘法运算，左A右B
OPERATION_MATMUL_A_B = tensorflow.matmul(PLACEHOLDER_A, PLACEHOLDER_B)
# 定义一个矩阵乘法运算，左B右A
OPERATION_MATMUL_B_A = tensorflow.matmul(PLACEHOLDER_B, PLACEHOLDER_A)
# 创建一个会话
SESSION = tensorflow.Session()
# 一个尺寸为一行两列的矩阵
MATRIX_A = [[random.random(), random.random()]]
# 一个尺寸为两行一列的矩阵
MATRIX_B = [[random.random()],
            [random.random()]]
# 显示尺寸为一行两列的矩阵的值
logging.debug('MATRIX_A : \n%s', MATRIX_A)
# 显示尺寸为两行一列的矩阵的值
logging.debug('MATRIX_B : \n%s', MATRIX_B)
# 运行左A右B的矩阵乘法运算，结果是1x1矩阵
logging.debug('OPERATION_MATMUL_A_B(PLACEHOLDER_A, PLACEHOLDER_B) : \n%s',
              SESSION.run(OPERATION_MATMUL_A_B, feed_dict={PLACEHOLDER_A: MATRIX_A, PLACEHOLDER_B: MATRIX_B}))
# 运行左B右A的矩阵乘法运算，结果是2x2矩阵
logging.debug('OPERATION_MATMUL_B_A(PLACEHOLDER_A, PLACEHOLDER_B) : \n%s',
              SESSION.run(OPERATION_MATMUL_B_A, feed_dict={PLACEHOLDER_A: MATRIX_A, PLACEHOLDER_B: MATRIX_B}))
# end of file
