# coding=utf-8
import os
import shutil
import datetime

#目标文件夹，此处为相对路径，也可以改为绝对路径
determination = r'D:/work/ubilink/AIVideoIdentification/tupianbianli3/'
if not os.path.exists(determination):
    os.makedirs(determination)

#源文件夹路径
path = r'D:/work/ubilink/AIVideoIdentification/AITestData2'
folders = os.listdir(path)
starttime = datetime.datetime.now()
for first in folders:
    dirs = path + '/' + str(first)
    sources = os.listdir(dirs)
    for second in sources:
        files = dirs + '/' + str(second)
        imgs = os.listdir(files)
        for img in imgs:
            source = files + '/' + str(img)
            deter = determination + '/' + str(img)
            shutil.copyfile(source, deter)
endtime = datetime.datetime.now()
print(endtime - starttime)
print("保存完毕！")

