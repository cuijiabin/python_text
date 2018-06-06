# coding=utf-8
"""
为了清晰直观展现python严格要求的缩进及数学公式，请访问博客上博文
详细说明见源代码中的注释

# 源代码
"""
# standard import
import logging
import os

import numpy

import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('start tensorflow tutorial example 6 least squares')
STR_SCRIPT_DIR, STR_SCRIPT_FILE = os.path.split(__file__)
logging.debug('STR_SCRIPT_DIR : %s', STR_SCRIPT_DIR)
logging.debug('STR_SCRIPT_FILE : %s', STR_SCRIPT_FILE)
STR_SCRIPT_PREFIX = os.path.splitext(STR_SCRIPT_FILE)[0]
logging.debug('STR_SCRIPT_PREFIX : %s', STR_SCRIPT_PREFIX)
# os.path.join(STR_SCRIPT_DIR, STR_SCRIPT_PREFIX + '.ext')
# 样本x
sample_x = numpy.asarray([474.7, 479.9, 488.1, 509.6, 576.4, 654.7, 755.6,
                          798.6, 815.4, 718.4, 767.2, 759.5, 820.3, 849.8,
                          974.7, 1041.0, 1099.3, 1186.1, 1252.5])
logging.debug('样本x : \n%s', sample_x)
# 样本y
sample_y = numpy.asarray([526.9, 532.7, 566.8, 591.2, 700.0, 744.1, 851.2,
                          884.4, 847.3, 821.0, 884.2, 903.7, 984.1, 1035.3,
                          1200.9, 1289.8, 1432.9, 1539.0, 1663.6])
logging.debug('样本y : \n%s', sample_y)
# 样本数量
n_samples = sample_x.shape[0]
logging.debug('样本数量 : %d', n_samples)
# 样本x的平均值
mean_x = sum(sample_x) / n_samples
logging.debug('样本x的平均值 : %f', mean_x)
# 样本y的平均值
mean_y = sum(sample_y) / n_samples
logging.debug('样本y的平均值 : %f', mean_y)
# 权重
weight = ((sum(sample_x[i] * sample_y[i] for i in range(n_samples)) - n_samples * mean_x * mean_y) /
          sum((sample_x[i] - mean_x) * (sample_x[i] - mean_x) for i in range(n_samples)))
logging.debug('权重 : %f', weight)
# 偏置
bias = mean_y - weight * mean_x
logging.debug('BIAS : %f', bias)
# 绘制样本
plt.plot(sample_x, sample_y, 'ro', label='样本')
# 绘制拟合直线
plt.plot(sample_x, sample_x * weight + bias, label='拟合')
# 显示图例
plt.legend()
# 保存图片
plt.savefig(os.path.join(STR_SCRIPT_DIR, STR_SCRIPT_PREFIX + '.png'))
# 显示图片
plt.show()
# end of file
