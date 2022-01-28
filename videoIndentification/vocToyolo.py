# _*_ coding:utf-8 _*_
# created by lzl on 2021-04-14

import xml.etree.ElementTree as xee
import os
import cv2
'''
1.将xml文件转换未label文件，包含标签的宽高，目标位置信息
2.通过将其进行归一化操作，转换成对应的比例值
3.最后将归一化后的数据保存到txt格式中，每一个目标对应一条记录
'''

# 1.获取xml内部标签, 3.保存归一化后的数据
def vocConverToyolo(filepath,xmlname):
    # 读取xmls文件夹下的xml文件并将需要的字段经过归一化处理存储到txt文件中
    xmlpath = filepath + '/xmls'
    xmlfile = os.path.join(xmlpath,xmlname)

    with open(xmlfile,'r') as in_file:
        txtname = xmlname[:-4]+'.txt'
        txtpath = filepath + '/txt'
        if not os.path.exists(txtpath):
            os.makedirs(txtpath)
        txtfile = os.path.join(txtpath,txtname)
        with open(txtfile,'w+') as out_file:
            txttree = xee.parse(in_file)
            txtroot = txttree.getroot()
            txtsize = txtroot.find('size')
            txtfilename = txtroot.find('filename').text

            # print('当前图片名称',txtfilename)
            w = int(txtsize.find('width').text)
            h = int(txtsize.find('height').text)
            out_file.truncate()
            for obj in txtroot.iter('object'):
                objdifficult = obj.find('difficult').text
                objname = obj.find('name').text
                if objname not in classes or int(objdifficult) == 1:
                    continue
                objname_id = classes.index(objname)
                xmlbndbox = obj.find('bndbox')
                bndbox = (float(xmlbndbox.find('xmin').text),float(xmlbndbox.find('ymin').text),float(xmlbndbox.find('xmax').text),float(xmlbndbox.find('ymax').text))
                bndToyolo = converToNormal([w,h],bndbox,txtfilename)
                out_file.write(str(objname_id) + " " +" ".join([str(loc) for loc in bndToyolo]) + '\n')

# 2.归一化操作
def converToNormal(size,bndbox,txtfilename):
    if(size[0] == 0 or size[1] == 0):
        # 去找对应图片，获取图片本身的宽高，替换当前size的值
        imgpath = filepath + '/'+txtfilename
        img = cv2.imread(imgpath)
        imgsp = img.shape
        # 通过shape获取图片的宽高，对应的分别是shape[1],shape[0]
        size[0] = list(imgsp)[1]
        size[1] = list(imgsp)[0]
    dw = 1 / (size[0])
    dh = 1 / (size[1])
    x = (bndbox[0] + bndbox[2]) / 2 - 1
    y = (bndbox[1] + bndbox[3]) / 2 - 1
    w = bndbox[2] - bndbox[0]
    h = bndbox[3] - bndbox[1]
    lastx = x * dw
    lasty = y * dh
    lastw = w * dw
    lasth = h * dh
    return (lastx,lasty,lastw,lasth)

def classesSave(classespath,filepath):
    # 读classes内容并保存到classes列表中
    classes_path = classespath +'/predefined_classes.txt'
    for line in open(classes_path,'r'):
        line = line.strip('\n')
        classes.append(line)
    print(classes)

    # 先把classes保存到classes.txt文件中
    out_classes_path = filepath + '/txt'
    # 打开文件夹
    os.chdir(out_classes_path)
    if not os.path.exists(out_classes_path):
        os.makedirs(out_classes_path)
    with open('classes.txt','w') as out_classes:
        for line in classes:
            out_classes.write(line+'\n')
    out_classes.close()
    print("所有类已写入classess.txt文件")

if __name__ == '__main__':
    filepath = r'D:\work\ubilink\AIVideoIdentification\AItestDataTotal\total_zdjy\ZdjyTotal'  #文件根目录
    input_classes_path = r'D:\work\ubilink\AIVideoIdentification\labelImg-master\labelImg-master\data' # 目标类路径
    classes = [] #定义一个classes列表

    # 读取目标类txt，并写入每个文件夹中
    classesSave(input_classes_path,filepath)

    # 读取xml文件转yolo格式
    xmlpath = filepath + '/xmls'
    list_1 = os.listdir(xmlpath)
    total = 0
    for i in range(0,len(list_1)):
        path = os.path.join(xmlpath,list_1[i])
        if ('.xml' in path) or ('.XML' in path):
            vocConverToyolo(filepath,list_1[i])
            total = total + 1
        else:
            print('第',i,'条不是xml格式文件')
    print('yolo格式文件共计', total, '条')
