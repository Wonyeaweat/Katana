import cv2
import numpy as np
import math
import sys
import os
import pytesseract

def init(inputImg):
    if(not os.path.exists('./Analyze')):
        os.mkdir('./Analyze')
    img = inputImg
    grayImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 将输入图片转成灰度图
    ret, binaryImage = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)  # 将灰度图二值化

    x_avg = np.mean(binaryImage, 1)  # 压缩列，对每行求平均值
    y_avg = np.mean(binaryImage, 0)  # 压缩行，对每列求平均值

    x = list()
    y = list()
    # x,y两个list用于记录原图像素中哪些行/列是一整条直线

    for i in range(len(x_avg)):
        if x_avg[i] > 100:
            x_avg[i] = 255
        elif abs(x_avg[i] - x_avg[i - 1]) > 100:
            x.append([i, x_avg[i]])
    for i in range(len(y_avg)):
        if y_avg[i] > 100:
            y_avg[i] = 255
        elif abs(y_avg[i] - y_avg[i - 1]) > 100:
            y.append([i, y_avg[i]])
    begX = 2
    begY = 2
    # 计算从哪行哪列开始出现数字

    while begX < len(x) and abs(x[begX][1] - x[begX - 1][1]) < 20:
        begX += 1
    if begX >= len(x):
        begX = 1
    while begY < len(y) and abs(y[begY][1] - y[begY - 1][1]) < 20:
        begY += 1
    if begY >= len(y):
        begY = 1

    dataAnalyze = open("./Analyze/data.dat", "w")
    dataAnalyze.write(str(len(x) - begX - 1) + ' ' + str(len(y) - begY - 1) + '\n')
    # 输出棋盘大小 几行几列

    for i in range(begX, len(x) - 1):
        outputX = list()
        for j in range(begY):
            tmpImg = binaryImage[
                     x[i][0] + math.ceil((x[i + 1][0] - x[i][0]) / 10.0):x[i + 1][0],
                     y[j][0] + math.ceil((y[j + 1][0] - y[j][0]) / 10.0):y[j + 1][0]]
            # 去掉黑边，采用-10%的方法
            fileName = "./Analyze/X-" + str(i - begX + 1) + "-" + str(j + 1) + ".png"
            cv2.imwrite(fileName, tmpImg)
            text = str.strip(
                pytesseract.image_to_string(fileName, config='--psm 10 -c tessedit_char_whitelist=0123456789'))+' '
            # --psm 10 指将图片识别成单个字符 后面白名单也有助于提升识别率
            if(text != ' '):
                outputX.append(text)
            # 存在空白图片，识别出来为空，需要特殊判断
        dataAnalyze.write(str(len(outputX))+' ')
        dataAnalyze.writelines(outputX)
        dataAnalyze.write('\n')
    # 每行先输出当前行的数字个数，接着空格隔开，从左至右输出数字

    for j in range(begY, len(y) - 1):
        outputY = list()
        for i in range(begX):
            tmpImg = binaryImage[
                     x[i][0] + math.ceil((x[i + 1][0] - x[i][0]) / 10.0):x[i + 1][0],
                     y[j][0] + math.ceil((y[j + 1][0] - y[j][0]) / 10.0):y[j + 1][0]]
            fileName = "./Analyze/Y-" + str(j - begY + 1) + "-" + str(i + 1) + ".png"
            cv2.imwrite(fileName, tmpImg)
            text = str.strip(
                pytesseract.image_to_string(fileName, config='--psm 10 -c tessedit_char_whitelist=0123456789'))+' '
            if(text!=' '):
                outputY.append(text)
        dataAnalyze.write(str(len(outputY)) + ' ')
        dataAnalyze.writelines(outputY)
        dataAnalyze.write('\n')
    # 每行先输出当前列的数字个数，接着空格隔开，从上至下输出数字
    print ('Finished.')


if __name__ == '__main__':
    filePath = './test_images/test_1.PNG'
    img = cv2.imread(filePath)
    init(img)