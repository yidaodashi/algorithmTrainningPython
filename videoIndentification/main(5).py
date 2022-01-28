import os, sys
import shutil
import cv2
from PIL import Image
import numpy as np


def get_pHash(file_path):
    """
    @:param file_path 图片文件地址
    @:return hash value 返回计算得到的Phash值
    """
    img = cv2.imread(file_path, 0)
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)

    h, w = img.shape[0:2]
    vis0 = np.zeros((h, w), dtype=np.float32)
    vis0[:h, :w] = img

    # 二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    vis1.resize(32, 32)

    # 计算均值
    avg = sum(sum(vis1)) * 1. / (vis1.shape[0]*vis1.shape[1])
    avg_list = ['0' if i < avg else '1' for row in vis1 for i in row]

    # 得到哈希值
    return ''.join(['%x' % int(''.join(avg_list[x:x + 4]), 2) for x in range(0, 32 * 32, 4)])


def find_repeat_pics(file_dir, show_flag = True):
    """
    :param file_dir: 需要去重处理的图片文件夹路径
    :param show_flag: 是否需要开启图像对比查看
    :return: None
    """
    if not os.path.isdir(file_dir): return
    repeat_num = 0
    res_dict = {}
    for file_name in os.listdir(file_dir):
        del_falg = False
        file_path = os.path.join(file_dir, file_name)
        try:
            hash_value = get_pHash(file_path)
        except:
            print("err:", file_path)
            continue
        for hash in res_dict.keys():
            distencce = sum([0 if ai == bi else 1 for ai, bi in zip(hash_value, hash)])
            if distencce <= 6:  # 如果哈希值距离小于6，认为图片重复可能性超过90%直接删除处理
                del_falg = True
                last_path = res_dict.get(hash)
                res_dict[hash] = file_path
                os.remove(last_path)
                repeat_num += 1
                print("{}：欧式距离 {}，移除 {}".format(repeat_num, distencce, last_path))
                break
            elif distencce<15:  # 如果哈希值距离大于6小于15需要人工查看，手动确认是否删除，按 'd' 键删除
                last_path = res_dict.get(hash)
                show_flag = True
                if show_flag:
                    img_new = cv2.imread(file_path)
                    img_old = cv2.imread(last_path)

                    h_new, w_new, _ = img_new.shape
                    h_old, w_old, _ = img_old.shape
                    img = np.zeros((max(h_new, h_old), w_new + w_old, 3), dtype=np.uint8)
                    img[0:h_new, 0:w_new, :] = img_new
                    img[0:h_old, w_new:, :] = img_old
                    rate = 1
                    if max(h_new, h_old, (w_new + w_old)) > 1080:
                        rate = 1080 / max(h_new, h_old, (w_new + w_old))
                    img = cv2.resize(img, (0, 0), fx=rate, fy=rate)
                    cv2.imshow("new_old_hash_{}".format(distencce), img)
                    key = cv2.waitKey(0) & 0xFF
                    if key == ord("d"):
                        res_dict[hash] = file_path
                        os.remove(last_path)
                        repeat_num += 1
                        print("{}：欧式距离 {}，移除 {}".format(repeat_num, distencce, last_path))
                    cv2.destroyAllWindows()
                break
        res_dict[hash_value] = file_path

    print("重复图片数量：", repeat_num)


def del_lowdpi_pics(org_dir, tag_dir, current_index=0):
    file_list = os.listdir(org_dir)
    del_list = []
    while (current_index < len(file_list)):
        file_name = file_list[current_index]
        name, ext = os.path.splitext(file_name)
        org_path = os.path.join(org_dir, file_name)
        if ext.lower() not in (".jpg", ".png"):
            current_index += 1
            continue
        try:
            image = Image.open(org_path)
            image = np.array(image)[:, :, [2, 1, 0]]
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
        if key == ord("d"):
            del_list.append(org_path)
        elif key == ord("f"):
            if current_index > 0:
                current_index -= 1
                continue
        elif key == ord("q"):
            break
        else:
            if org_path in del_list:
                del_list.remove(org_path)
        current_index += 1

    move_to_tag_dir(del_list, tag_dir, mode="move")

    return current_index - len(del_list)


def find_files_in_dir(dir):
    """
    查找文件夹下面的所有文件路径
    :param dir: 文件根目录
    :return: 所有文件列表
    """
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
    """
    将文件拷贝或者移动到目标文件夹
    :param file_list: 文件列表
    :param tag_dir: 目标文件夹
    :param mode: 操作模式 copy 拷贝模式，move 移动模式
    :return: None
    """
    for org_path in file_list:
        if not os.path.exists(org_path):
            continue
        _, file_name = os.path.split(org_path)
        tag_path = os.path.join(tag_dir, file_name)
        if mode=="move":
            shutil.move(org_path, tag_path)
            print("移动文件：{} -> {}".format(org_path, tag_path))
        else:
            shutil.copy(org_path, tag_path)


def filtrate_image(org_dir, tag_dir, current_index=0):
    print("（按 s 进行保存, f 查看上一张图，否则跳过）")

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
        elif key == ord("f"):
            if current_index > 0:
                current_index -= 1
                continue
        elif key == ord("q"):
            break
        current_index += 1
    return current_index


if __name__ == '__main__':
    import yaml
    yaml_file_path = "config.yml"
    yaml_file = open(yaml_file_path, 'r', encoding='utf-8')
    conf = yaml.load(yaml_file.read(), yaml.BaseLoader)

    while(True):
        print("1.整理图片（将图片文件移动到指定文件夹下）\n"
              "2.筛选图片（逐个筛选有用图片）\n"
              "3.查找重复图片\n"
              "4.筛除低质量图片\n"
              "5:退出程序")
        command = input("输入功能选项：")
        if command == "1":
            org_path = input("输入图片源文件夹地址：")
            tag_path = input("输入图片目标存放地址：")


            if os.path.isdir(r"{}".format(org_path)) and os.path.isdir(r"{}".format(tag_path)):
                result_list = find_files_in_dir(r"{}".format(org_path))
                move_to_tag_dir(result_list, r"{}".format(tag_path))
                print("文件整理完成：{}".format(tag_path))
            else:
                print("文件夹路径不正确")

        elif command == "2":
            org_path = input("待筛选图片存放地址：")
            tag_path = input("筛出图片保存地址：")

            if not os.path.isdir(r"{}".format(org_path)):
                org_path = conf['pic_org_path']
            else:
                conf['pic_org_path'] = org_path

            if not os.path.isdir(r"{}".format(tag_path)):
                tag_path = conf['pic_save_path']
            else:
                conf['pic_save_path'] = tag_path

            current_index = input("输入筛选序号：")
            if current_index.strip() != "":
                try:
                    current_index = int(current_index)
                except:
                    current_index = 0
            else:
                current_index = int(conf['current_index'])
            if os.path.isdir(r"{}".format(org_path)) and os.path.isdir(r"{}".format(tag_path)):
                conf['current_index'] = filtrate_image(r"{}".format(org_path), r"{}".format(tag_path), current_index)
        elif command == "3":
            save_path = input("图片存放地址：")
            if not os.path.isdir(r"{}".format(save_path)):
                org_path = conf['pic_save_path']
            find_repeat_pics(save_path)
        elif command == "4":
            org_path = input("图片源地址：")
            save_path = input("移除图片存放地址：")
            if not os.path.isdir(r"{}".format(org_path)):
                org_path = conf['pic_org_path']
            if not os.path.isdir(r"{}".format(save_path)):
                save_path = conf['pic_save_path']
            current_index = int(conf['current_index'])
            conf['current_index'] = del_lowdpi_pics(org_path, save_path, current_index)
        elif command == "5":
            break
        with open(yaml_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(conf, f)