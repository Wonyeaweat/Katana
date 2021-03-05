import cv2
import numpy as np
import math
import sys
import os
import pytesseract


def imageOptimize(inputImg):
    flag = True
    img = np.array(cv2.resize(inputImg, (100, 100), cv2.INTER_CUBIC))  # 图片修改成100*100 px
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # 将灰度图二值化
    x1, x2, y1, y2 = 0, 99, 0, 99
    while sum(img[x1]) < 255 * 30:  # 黑色像素>70个
        x1 += 1
    while sum(img[x2]) < 255 * 30:  # 黑色像素>70个
        x2 -= 1
    while sum(i[y1] for i in img) < 255 * 30:  # 黑色像素>70个
        y1 += 1
    while sum(i[y2] for i in img) < 255 * 30:  # 黑色像素>70个
        y2 -= 1
    img = cv2.resize(img[x1:x2, y1:y2], (100, 100), cv2.INTER_CUBIC)
    cnt = sum([sum(i) for i in img])
    if cnt > 2540000:
        flag = False
    # img = cv2.resize(img, (100, 100))  # 图片修改成100*100 px
    return flag, img


'''
图片调整为100*100px后，如果某行的像素黑色数量超过70 认为是尚未去除干净的直线
去除后，重新调整为100*100px 统计全部像素灰度值之和 如果超过2540000 认为是全白图片
'''


def solve(inputImg):
    if not os.path.exists('./Analyze'):
        os.mkdir('./Analyze')
    img = inputImg
    grayImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 将输入图片转成灰度图
    ret, binaryImage = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)  # 将灰度图二值化

    x_avg = np.mean(binaryImage, 1)  # 压缩列，对每行求平均值
    y_avg = np.mean(binaryImage, 0)  # 压缩行，对每列求平均值
    '''
    对二值化后的图片而言，黑色直线表现为：灰度值接近0 其他空白处灰度值接近255
    所以，对每行每列求平均值，如果平均值大，说明直线长度短，反之说明长
    可以根据这个规律 判断出图片哪些位置有直线，直线的长度是多少
    利用这个规律可以找到棋盘与方格的边界，统计出对应的数据
    '''

    x = list()
    y = list()
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
    '''
    遍历图片的每一行每一列，我们认为当该行/列 的平均灰度值大于100时，不是直线
    反之，如果该行恰好是经过了棋盘左方或上方的数字，其平均灰度值也会较小，但并不是直线
    所以，增加额外的判定条件：与上一行/列 的平均灰度值差值超过100，才是直线
    并按 (像素坐标位置，平均灰度值) 的格式加入到x,y 两个list中
    '''

    begX = 2
    begY = 2
    while begX < len(x) and abs(x[begX][1] - x[begX - 1][1]) < 20:
        begX += 1
    if begX >= len(x):
        begX = 1
    while begY < len(y) and abs(y[begY][1] - y[begY - 1][1]) < 20:
        begY += 1
    if begY >= len(y):
        begY = 1
    '''
    Katana的棋盘左上方是预览区，所以经过预览区的直线比其他直线稍短，等价于平均灰度值有所提升
    遍历x,y两个list，找到灰度值下降的第一条直线，其对应位置就是有数字开始的直线位置
    分别将其对应的编号 保存在begX与begY中
    存在一种特殊情况，即数字区只有一行/列，导致没有经过预览区的直线，全部直线都是一样长，
    此时需要特殊判断处理
    '''

    dataAnalyze = open("./Analyze/data.dat", "w")
    height = len(x) - begX - 1
    width = len(y) - begY - 1
    dataAnalyze.write(str(height) + ' ' + str(width) + '\n')
    '''
    将分析结果保存在 /Analyze/data.dat 文件下。该文件第一行两个数字即棋盘大小（格子数*格子数）
    '''

    for i in range(begX, len(x) - 1):
        outputX = list()
        for j in range(begY):
            tmpImg = binaryImage[x[i][0]:x[i + 1][0], y[j][0]:y[j + 1][0]]  # 截取了一个方格的图片
            flag, tmpImg = imageOptimize(tmpImg)  # 判断图片是否有数字（可能为空），处理后的图片
            if (flag):  # 有数字
                fileName = "./Analyze/X-" + str(i - begX + 1) + "-" + str(j + 1) + ".png"
                cv2.imwrite(fileName, tmpImg)
                text = str.strip(
                    pytesseract.image_to_string(fileName, config='--psm 7 -c tessedit_char_whitelist=0123456789')) + ' '
                outputX.append(text)
                print('X', i - begX + 1, j + 1, text)
            # 存在空白图片，识别出来为空，需要特殊判断
        dataAnalyze.write(str(len(outputX)) + ' ')
        dataAnalyze.writelines(outputX)
        dataAnalyze.write('\n')
    # 每行先输出当前行的数字个数，接着空格隔开，从左至右输出数字
    '''
    将数字区进行分割，交给tesseract 进行数字识别。利用之前统计的直线数据，可以很方便截取一个个方格。
    这段程序是分割图片左侧的数字区域，for i 枚举的是每行的上方直线，for j枚举的是每列的左侧直线
    tmpImg截取后交由 imageOptimize 进行处理（判断有无数字，去掉边框等）
    '''

    for j in range(begY, len(y) - 1):
        outputY = list()
        for i in range(begX):
            tmpImg = binaryImage[x[i][0]:x[i + 1][0], y[j][0]:y[j + 1][0]]
            flag, tmpImg = imageOptimize(tmpImg)
            if flag:
                fileName = "./Analyze/Y-" + str(j - begY + 1) + "-" + str(i + 1) + ".png"
                cv2.imwrite(fileName, tmpImg)
                text = str.strip(
                    pytesseract.image_to_string(fileName, config='--psm 7 -c tessedit_char_whitelist=0123456789')) + ' '
                outputY.append(text)
                print('Y', j - begY + 1, i + 1, text)
        dataAnalyze.write(str(len(outputY)) + ' ')
        dataAnalyze.writelines(outputY)
        dataAnalyze.write('\n')
    # 每行先输出当前列的数字个数，接着空格隔开，从上至下输出数字
    print('Solving...')
    os.system('solve.exe')
    res = list()
    with open('./Analyze/result.dat', 'r') as file:
        lines = file.readlines()
        for i in lines:
            res.append(list(filter(None, i.split(" "))))
    img = inputImg
    for i in range(height):
        for j in range(width):
            if res[i][j]=='1':
                img[x[begX+i][0]:x[begX+i+1][0],y[begY+j][0]:y[begY+j+1][0]] = [0,0,0]
    cv2.imwrite('./Analyze/result.png',img)


if __name__ == '__main__':
    filePath = './test_images/test_2.PNG'
    img = cv2.imread(filePath)
    solve(img)
