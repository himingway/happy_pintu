#!/usr/bin/env python
# Power by himingway
# 2018-1-7 18:24:34

import cv2
from operator import itemgetter
import sys
import tkinter as tk


def read_pic(img_path,match_path):
    img = cv2.imread(img_path)
    match = cv2.imread(match_path)
    info = tk.Tk()
    screen_height = info.winfo_screenheight()
    while (img.shape[0] > screen_height-50):
        img = cv2.resize(img, (0, 0), fx=0.8, fy=0.8)
        match = cv2.resize(match, (0, 0), fx=0.8, fy=0.8)
    return img, match


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        point.pop(0)
        point.append((x, y))
        print('point' + ':', point[0], point[1])


#
def cal_lenth(p, num):
    lenth = p[1][0] - p[0][0]
    width = p[1][1] - p[0][1]
    lenth = lenth / num
    width = width / num
    return (lenth + width) / 2


def sort_result(l,num):
    result_index = []
    for i in range(1, num+1):
        for j in range(1, num+1):
            result_index.append((i, j))
    # print(result_index)
    for i in range(len(l) - 1):
        min_index = i
        for j in range(i + 1, len(l)):
            if (l[min_index] > l[j]):
                min_index = j
        l[i], l[min_index] = l[min_index], l[i]
        print('第 %2d 次循环' % (i + 1), '：', result_index[i], '与', result_index[min_index], '互换')

def main(img,match,num):
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse)
    cv2.imshow('image', img)
    print('请点击拼图区的左上角和右下角，按任意键结束!')
    cv2.waitKey()
    lenth = int(cal_lenth(point, num)) + 1
    x = point[0][0]
    y = point[0][1]
    n = 0
    result = []
    for i in range(num):
        for j in range(num):
            n = n + 1
            img2 = img[y + i * lenth + 3: y + (i + 1) * lenth - 3, x + j * lenth + 3: x + (j + 1) * lenth - 3]
            res = cv2.matchTemplate(img2, match, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            top_left = max_loc
            result.append((n, top_left[0], top_left[1]))
            cv2.putText(match, str(n), (top_left[0] + int(lenth / 2), top_left[1] + int(lenth / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #cv2.imwrite("%d.png" % n, img2)
    result = sorted(result, key=itemgetter(2, 1))
    for i in range(num):
        result[i * num:(i + 1) * num] = sorted(result[i * num:(i + 1) * num], key=itemgetter(1))
    result_sort = [x[0] for x in result]
    sort_result(result_sort,num)
    cv2.imshow('image', match)
    print('按任意键关闭')
    cv2.waitKey()
    cv2.destroyWindow('image')


if __name__ == '__main__':
    global point
    point = [(0, 0), (0, 0)]
    if len(sys.argv) != 4:
        print ('Usage: python origin_picture disorder_picture num_of_line')
        exit(1)
    img, match = read_pic(sys.argv[1],sys.argv[2])
    main(img,match,int(sys.argv[3]))
