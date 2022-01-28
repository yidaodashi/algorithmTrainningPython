# _*_ coding = utf-8 _*_
# @Date : 2021/4/22
# @Time : 16:15
# @NAME ：molin
import os
import shutil
import cv2
import datetime
from tqdm import tqdm
'''
    实现：
    1、比较原文件夹A中图片和剪切后文件夹B的图片，将B中没有存在A的的图片单独保存到一个新文件夹C（做测试集用）
    2、对文件夹B中的图片统一大小，图片最大边和最小边比例控制在1-1.33，并且满足最小边的长度大于350，然后缩放图片，控制最大边等于500
'''


# 1、比较原文件夹A中图片和剪切后文件夹B的图片，将B中没有存在A的的图片单独保存到一个新文件夹C（做测试集用）
def saveCutImgleft(sourcePath, cutPath, savePath):
    # 获取源文件夹图片、剪切文件夹图片所有名称
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    source_img_name_list = os.listdir(sourcePath)
    cut_img_name_list = os.listdir(cutPath)

    for img_name in tqdm(source_img_name_list):
        if img_name not in cut_img_name_list:
            sourceimg_path = os.path.join(sourcePath, img_name)
            shutil.copy(sourceimg_path, savePath)
        # print("未剪切的图片：{}".format(source))


# 2、对文件夹B中的图片统一大小，图片最大边和最小边比例控制在1-1.33，并且满足最小边的长度大于350，然后缩放图片，控制最大边等于500
def convertCutImgToUnified(cutPath, saveUnifiedPath, ununifiedPath):
    img_name_list = os.listdir(cutPath)
    print('列表长度{}：'.format(len(img_name_list)))
    if not os.path.exists(saveUnifiedPath):
        os.makedirs(saveUnifiedPath)
    if not os.path.exists(ununifiedPath):
        os.makedirs(ununifiedPath)
    start_time = datetime.datetime.now()
    for img_name in tqdm(img_name_list):
        ext = os.path.splitext(img_name)
        if str(ext[1]).lower() not in ['.jpg', '.png']:
            print(img_name)
            continue
        img_path = os.path.join(cutPath, img_name)
        file_unified_path = os.path.join(saveUnifiedPath, img_name)
        unuified_path = os.path.join(ununifiedPath, img_name)
        img_file = cv2.imread(img_path)
        # 获取图片宽高
        h, w, _ = img_file.shape
        x_max = max(h, w)
        x_min = min(h, w)
        rate = float('%.2f' %(x_max / x_min))
        if 1 <= rate <= 1.33 and x_min >= 350:
            resize_image(img_file, 500/x_max, file_unified_path)
        else:
            move_ununified(img_path,unuified_path)
    end_time = datetime.datetime.now()
    print("缩放图片耗时：{}".format((end_time - start_time)))


# 将统一规格的图片移到save_unified_path路径下的文件夹
def resize_image(img, rate, filePath):
    img = cv2.resize(img, (0, 0), fx=rate, fy=rate)
    cv2.imwrite(filePath, img)

# 将没有统一规格的图片移到save_ununified_path路径下的文件夹
def move_ununified(unusedFilePath,filePath):
    shutil.copy(unusedFilePath, filePath)


if __name__ == '__main__':
    source_path = r'D:\work\ubilink\AIVideoIdentification\bxp\legacy_data\1'
    cut_path = r'D:\work\ubilink\AIVideoIdentification\bxp\legacy_data_cut_v1\1'
    save_path = r'D:\work\ubilink\AIVideoIdentification\bxp\legacy_data_processed\1\bxp_save_left'
    save_unified_path = r'D:\work\ubilink\AIVideoIdentification\bxp\legacy_data_processed\1\bxp_save_unified'
    save_ununified_path = r'D:\work\ubilink\AIVideoIdentification\bxp\legacy_data_processed\1\bxp_save_ununified'

    saveCutImgleft(source_path, cut_path, save_path)

    convertCutImgToUnified(cut_path, save_unified_path, save_ununified_path)
