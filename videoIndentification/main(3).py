import os, sys
import shutil
import cv2
from PIL import Image
import numpy as np
import datetime


def find_files_in_dir(dir):
    result_file_list = []
    if os.path.isdir(dir):
        file_list = os.listdir(dir)
        for file_name in file_list:
            file_path = os.path.join(dir, file_name)
            result_file_list.extend(find_files_in_dir(file_path))
        return result_file_list
    elif os.path.isfile(dir):
        return [dir]


def move_to_tag_dir(file_list, tag_dir, mode="copy"):
    for org_path in file_list:
        _, file_name = os.path.split(org_path)
        tag_path = os.path.join(tag_dir, file_name)
        if mode=="move":
            shutil.move(org_path, tag_path)
        else:
            shutil.copy(org_path, tag_path)


def filtrate_image(org_dir, tag_dir, current_index=0):
    print("（按 s 进行保存，否则跳过）")

    file_list = os.listdir(org_dir)
    while(current_index < len(file_list)):
        file_name = file_list[current_index]
        name, ext = os.path.splitext(file_name)
        org_path = os.path.join(org_dir, file_name)
        tag_path = os.path.join(tag_dir, file_name)
        if ext.lower() not in (".jpg", ".png"):
            current_index += 1
            continue
        try:
            image = Image.open(org_path)
            image = np.array(image)[:, :, ::-1]
        except:
            current_index += 1
            continue
        h, w, _ = image.shape
        rate = 1
        if max(h, w) > 1080:
            rate = 1080 / max(h, w)
        image = cv2.resize(image, (0, 0), fx=rate, fy=rate)
        win_name = "_{}_".format(current_index)
        cv2.namedWindow(win_name, 0)
        cv2.imshow(win_name, image)
        cv2.resizeWindow(win_name, image.shape[1], image.shape[0])
        cv2.moveWindow(win_name, 100, 1)
        key = cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        if key == ord("s"):
            shutil.copy(org_path, tag_path)
        elif key == ord("l"):
            if current_index > 0:
                current_index -= 1
                continue
        elif key == ord("q"):
            break
        current_index += 1


if __name__ == '__main__':
    while(True):
        print("1.整理图片（将图片文件移动到指定文件夹下）\n"
              "2.筛选图片（逐个筛选有用图片）\n"
              "3:退出程序")
        command = input("输入功能选项：")
        if command == "1":
            org_path = input("输入图片源文件夹地址：")
            tag_path = input("输入图片目标存放地址：")

            if os.path.isdir(r"{}".format(org_path)) and os.path.isdir(r"{}".format(tag_path)):
                starttime = datetime.datetime.now()
                result_list = find_files_in_dir(r"{}".format(org_path))
                move_to_tag_dir(result_list, r"{}".format(tag_path))
                endtime = datetime.datetime.now()
                print("文件整理完成：{}".format(tag_path))
                print(endtime - starttime)
            else:
                print("文件夹路径不正确")
        elif command == "2":
            org_path = input("待筛选图片存放地址：")
            tag_path = input("筛出图片保存地址：")
            current_index = input("输入筛选序号：")
            if current_index.strip() != "":
                try:
                    current_index = int(current_index)
                except:
                    current_index = 0
            else:
                current_index = 0
            if os.path.isdir(r"{}".format(org_path)) and os.path.isdir(r"{}".format(tag_path)):
                filtrate_image(r"{}".format(org_path), r"{}".format(tag_path), current_index)
        elif command == "3":
            break
