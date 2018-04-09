#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
功能：通过打开一个文件对话窗口来选择文件，获得文件路径（包含文件名和后缀）
时间：2017年3月10日 15:40:06
"""
import matplotlib.image as mpimg
import os
import tkFileDialog
class readfile(object):
    def __init__(self):
        self.default_dir = r"C:\Users\lenovo\Desktop"  # 设置默认打开目录

    def read(self):
        try:
            fname = tkFileDialog.askopenfilename(title=u"选择文件", initialdir=(os.path.expanduser(self.default_dir)))
        except :
            print "没有选择文件"
        else:
            return fname  # 返回文件全路径


if __name__ == '__main__':
    r1 = readfile()
    img = mpimg.imread(r1.read())
    print img.shape
    # restore img into array
    img_1 = img[:, :, 0]
    print img_1
