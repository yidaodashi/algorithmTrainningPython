# _*_ coding = utf-8 _*_
# @Date : 2021/5/20
# @Time : 17:09
# @NAME ：molin
# @function ： 测试xlwt处理Excel的功能，设置单元格字体样式、边框、背景等等

import xlwt
import patterns as patterns
import time
import xlrd
from datetime import date,datetime

def createNumberSheet():
    # 定义workbook
    workbook = xlwt.Workbook()

    # 添加sheet,这个sheet的名字叫xlwtTest
    sheet = workbook.add_sheet('xlwtTest')

    # 写入数据
    row = 0
    column = 0
    for i in range(72):
        sheet.write(row, column, i)
        column += 1
        if column > 8:
            column = 0
            row += 1
    # 定义保存excel的位置和文件名，默认在一个目录下
    workbook.save('xlwtTest.xls')

def settingNumberStyle():
    # 设置字体、居中、边框和背景

    i = 0
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('xlwtBackground', cell_overwrite_ok=True)
    '''
        重复操作一个单元格导致的
    '''
    while i < 64:
        # 为样式创建字体
        font = xlwt.Font()
        # 字体类型
        font.name = 'name Times New Roman'

        # 字体颜色
        font.colour_index = i
        # 字体大小，11为字号，20为衡量单位
        font.height = 20 * 11
        # 字体加粗
        font.bold = False
        # 下划线
        font.underline = True
        # 斜体字
        font.italic = True

        # 设置单元格对齐方式
        alignment = xlwt.Alignment()
        # 0x01 左端对齐  0x02 水平向上居中对齐 0x03 右端对齐
        alignment.horz = 0x02
        #0x00 上端对齐 0x01 垂直向上居中对齐 0x02 底端对齐
        alignment.vert = 0x01

        # 设置自动换行
        alignment.wrap = 1
        # 设置边框
        borders = xlwt.Borders()
        # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
        # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
        borders.left = 1
        borders.right = 2
        borders.top = 3
        borders.bottom = 4
        borders.left_colour = i
        borders.right_colour = i
        borders.top_colour = i
        borders.bottom_colour = i

        # 设置列宽，一个中文等于两个英文，11为字符数，256为衡量单位
        sheet.col(1).width = 11 * 256
        # 设置背景颜色
        pattern = xlwt.Pattern()
        # 设置背景颜色的模式
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        # 背景颜色
        pattern.pattern_fore_colour = i

        # 初始化样式
        style0 = xlwt.XFStyle()
        style0.font = font

        style1 = xlwt.XFStyle()
        style1.pattern = pattern

        style2 = xlwt.XFStyle()
        style2.alignment = alignment

        style3 = xlwt.XFStyle()
        style3.borders = borders

        # 设置文字模式
        font.num_format_str = '#,##0.00'

        sheet.write(i, 0, u'字体', style0)
        sheet.write(i, 1, u'背景', style1)
        sheet.write(i, 2, u'对齐方式', style2)
        sheet.write(i, 3, u'边框', style3)

        # 合并单元格，合并第2行到第4行的第4列到第5列
        sheet.write_merge(2, 4, 4, 5, u'合并')
        i = i + 1
    book.save(time.strftime("%Y%m%d%H%M%S")+'.xls')

def readExcel():
    # 打开文件
    workbook = xlrd.open_workbook(r'./lzl.xls')
    # 获取所有sheet
    print(workbook.sheet_names())
    sheet_name = workbook.sheet_names()[0]
    sheet_name1 = workbook.sheet_names()[1]
    print(sheet_name)
    print("第三个表名：", workbook.sheet_names()[2])

    # 根据sheet索引或者名称获取sheet内容
    sheetContent = workbook.sheet_by_index(0) #从索引0开始
    sheetContent1 = workbook.sheet_by_name(sheet_name1) #从表格名称开始
    sheetContent2 = workbook.sheet_by_name(workbook.sheet_names()[2])

    #打印表格的名称，行数和列数
    print("按索引打印：", sheetContent.name, sheetContent.nrows, sheetContent.ncols)
    print("按名称打印：", sheetContent1.name, sheetContent1.nrows, sheetContent1.ncols)
    print("第三个表打印：", sheetContent2.name, sheetContent2.nrows, sheetContent2.ncols)

    # 获取行和列的值
    rows = sheetContent.row_values(0)
    cols = sheetContent.col_values(0, 1)

    rows1 = sheetContent1.row_values(0)
    cols1 = sheetContent1.col_values(0, 1)
    # print(rows, '\n', cols)
    # print(rows1, '\n', cols1)

    # 获取单元格
    print("{}单元格内容是：".format(sheet_name), sheetContent.cell(2, 1).value)
    print("{}单元格内容是：".format(sheet_name1), sheetContent1.cell_value(2, 1))
    # print("{}单元格内容是: ".format(workbook.sheet_names()[2]), workbook.sheet_by_name(workbook.sheet_names()[2]).cell(2, 1))

if __name__ == '__main__':
    # createNumberSheet()
    # settingNumberStyle()
    readExcel()