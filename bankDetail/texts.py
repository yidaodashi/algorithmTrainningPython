# _*_ coding:utf-8 _*_
# Created by lzl
# TIME: 2021/2/8 11:37

# 写入excel文件的库
import xlwt

input_txt = r'D:\learn\personalPrograms\algorithmTrainningPython\bankDetail\bankTotal\BOCDZ_52210151_20210317.txt'
output_excel = r'D:\learn\personalPrograms\algorithmTrainningPython\bankDetail\bankTotal\BOCDZ_52210151_20210317.xls'
sheetName = 'Sheet1'
start_row = 0
start_col = 0

wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet(sheetName)

f = open(input_txt, encoding='utf-8')

row_excel = start_row
for line in f:
    line = line.strip('\n')
    line = line.split('|')

    print(line)

    col_excel = start_col
    len_line = len(line)
    for j in range(len_line):
        print(line[j])
        ws.write(row_excel, col_excel, line[j])
        col_excel += 1
        wb.save(output_excel)

    row_excel += 1

f.close

