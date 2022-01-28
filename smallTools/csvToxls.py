# _*_ coding = utf-8 _*_
# @Date : 2021/8/2
# @Time : 16:35
# @NAME ：molin
from io import StringIO
import csv
import pandas as pd

c_path = r"C:\Users\molin\Desktop\公安井盖.csv"
x_path = r"C:\Users\molin\Desktop\公安井盖.xls"  # 路径中的xls文件在调用to_excel时会自动创建


def csv_to_xls(csv_path, xls_path):
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
    data_file = StringIO(data)
    print(data_file)
    csv_reader = csv.reader(data_file)
    list_csv = []
    for row in csv_reader:
        list_csv.append(row)
    df_csv = pd.DataFrame(list_csv).applymap(str)
    '''
    这部分是不将csv装换为xls，而是过滤后再写入csv文件
    df_csv = df_csv[(df_csv[4] == '') | (df_csv[4] == 'name')]      # 过滤出第四列包含空值和name的数据
    df_csv.to_csv(csv_path, index=0, header=0, encoding='gb18030')  # 写入csv文件中
    '''
    writer = pd.ExcelWriter(xls_path)
    # 写入Excel
    df_csv.to_excel(
        excel_writer=writer,
        index=False,
        header=False
    )

    writer.save()
    # 删除csv文件
    # os.remove(c_path)


csv_to_xls(c_path, x_path)