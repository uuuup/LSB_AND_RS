# -*- coding: utf-8 -*-
'''
'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from Tkinter import *
from LSB_RSAnalysis import LSB_steg_RS
from ReadBmp import readfile

def read_bmp():
    r1 = readfile()
    return r1.read()

def select( text, x):
    import sys
    reload(sys)
    sys.setdefaultencoding('gbk')

    img = mpimg.imread(read_bmp())
    lsb_rs = LSB_steg_RS(img, 8)
    plt.subplot(121)
    plt.imshow(img)  # show img
    # print img
    plt.axis('off')  # no axis
    print str(img.shape)
    text.insert( END, str(img.shape)+"\n")
    text.update()

    # restore img into array
    img_1 = img[:, :, 0]
    print str(img_1)
    text.insert( END, str(img_1))
    text.update()

    imgR = np.array(img_1)
    # before LSB steg, we calculate the correlation of img
    Rm, Sm, R_m, S_m = lsb_rs.imgTotal_correlation(imgR)
    print ("Rm = %d, Sm = %d, R_m = %d, S_m = %d" % (Rm, Sm, R_m, S_m))
    text.insert( END, "\nRm = %d, Sm = %d, R_m = %d, S_m = %d\n" % (Rm, Sm, R_m, S_m))
    text.update()

    # after LSB steg, we calculate the correlation of img
    rate = 0.1
    rm = np.zeros(11)
    sm = np.zeros(11)
    r_m = np.zeros(11)
    s_m = np.zeros(11)
    index = 0
    rm[index] = Rm
    sm[index] = Sm
    r_m[index] = R_m
    s_m[index] = S_m
    imgshow = np.zeros((512, 512, 3), np.uint8)

    while (rate <= 1.0):
        if (x == 1):
            imgR = lsb_rs.LSB(imgR, rate)
        elif (x == 2):
            imgR = lsb_rs.LSB_improve(imgR, rate) #抗rs分析
        Rm, Sm, R_m, S_m = lsb_rs.imgTotal_correlation(imgR)
        print ("Rm = %d, Sm = %d, R_m = %d, S_m = %d" % (Rm, Sm, R_m, S_m))
        text.insert(END, "Rm = %d, Sm = %d, R_m = %d, S_m = %d\n" % (Rm, Sm, R_m, S_m))
        text.update()

        rate += 0.1
        index += 1
        rm[index] = Rm
        sm[index] = Sm
        r_m[index] = R_m
        s_m[index] = S_m

    rate = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    #plt.show()
    plt.subplot(122)
    plt.plot(rate, rm/((lsb_rs.height / lsb_rs.size)*(lsb_rs.width / lsb_rs.size)), label='Rm')
    plt.plot(rate, sm/((lsb_rs.height / lsb_rs.size)*(lsb_rs.width / lsb_rs.size)), label='Sm')
    plt.plot(rate, r_m/((lsb_rs.height / lsb_rs.size)*(lsb_rs.width / lsb_rs.size)), label='R_m')
    plt.plot(rate, s_m/((lsb_rs.height / lsb_rs.size)*(lsb_rs.width / lsb_rs.size)), label='S_m')

    plt.legend(['Rm', 'Sm', 'R_m', 'S_m'], loc='upper right')
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    if (x == 1):
        plt.savefig("result1.png")
    elif (x == 2):
        plt.savefig("result2.png")
    plt.show()

if __name__ == '__main__':
    global window
    window = Tk()

    # 创建两个按钮
    global text
    text = Text( window, width = 100, height = 30)

    bt_LSB = Button( window, text="LSB", width=50,command = lambda : select( text, 1))
    bt_LSB_improve = Button( window, text="LSB_improve", width=50, command = lambda : select( text, 2))
    # 将按钮置在窗口上
    text.grid( row=0, columnspan = 2)#columnspan代表占据多少个单元格
    bt_LSB.grid( row=1, column=0)
    bt_LSB_improve.grid( row=1, column=1)
    # 创建一个事件循环，监测事件发生，直到窗口关闭
    window.mainloop()