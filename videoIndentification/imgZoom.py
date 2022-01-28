# _*_ coding:utf-8 _*_
# created by lzl on 2021-04-15
import os
import cv2
import datetime

'''
    该文件主要是用来实现图片指定缩放，若图片宽高最大值小于600像素，则将最大值扩大到600，另一个等比缩放，
    若图片宽高最小值大于1080像素，则将最大值缩小到1080，另一个值等比缩放
'''
# 去除重复图片（图片去重）,两种方法，一种md5,另一种计算相似度
def imgDelSame(filepath, savepath):
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    pass


# 方法1：使用md5比较图片
def getmd5(imgpath):
    pass

# 方法2：计算相似度
def getssim(imgpath):
    pass


# 图片缩放，图片宽高最小值都大于1080的使最大值等于1080，图片宽高最大值小于600的使最大值等于600
def imgScale(filepath, tagpath):
    if not os.path.exists(tagpath):
        os.makedirs(tagpath)
    starttime = datetime.datetime.now()
    for file_name in os.listdir(filepath):
        file_org_path = os.path.join(filepath, file_name)
        file_tag_path = os.path.join(tagpath, file_name)
        img = cv2.imread(file_org_path)
        h, w, _ = img.shape

        if max(h, w) <= 600:
            rate = 600/max(h, w)
            resize_image(img, rate, file_tag_path)
            continue

        if min(h, w) >= 1080:
            rate = 1080/max(h, w)
            resize_image(img, rate, file_tag_path)
            continue
        resize_image(img,rate,file_tag_path)
    endtime = datetime.datetime.now()
    print("耗时：",(endtime - starttime))
    print("所有图片替换成功")


def resize_image(img, rate, tag_path):
    img = cv2.resize(img, (0, 0), fx=rate, fy=rate)
    cv2.imwrite(tag_path, img)


if __name__ == '__main__':
    file_path = r'D:\work\ubilink\AIVideoIdentification\tupianbianlialltype'
    tag_path = r'D:\work\ubilink\AIVideoIdentification\tupiansuofang'
    imgScale(file_path,tag_path)