# _*_ coding:utf-8 _*_
# Created by lzl
# TIME: 2021/3/4 11:48

'''
    功能介绍：将每月银行明细表按照每天进行分表，然后按照区域平台统计提现金额
    先把整个月份的提现按照提现时间排序(删除前两行，排序，Excel处理完后)

    python工作：
    第一步：将处理后的表按照每天进行分表，表命名：时间.xls
    第二步：然后根据区号名称进行统计，同时统计数目，然后计算金额（数目*10）
'''
import pandas as pd
data = pd.read_excel('C:/Users/molin/Desktop/3月份/银行流水明细表3月.xls')
rows = data.shape[0]  #获取行数，shape[1]获取列数
day_list = [] #天列表
bank_get_count = [] #银行提现条数列表
defaultUrl = r"D:\learn\personalPrograms\algorithmTrainningPython\bankDetail\3月份"

# 按照各个区汇总每月提现金额
def divedeRegion():
    month_df_size = data.groupby(['区级平台名称'],as_index=False).size().to_frame('提现金额')
    out_month_path = pd.ExcelWriter(r""+defaultUrl+"\各区每月提现汇总.xls")
    (month_df_size*10).to_excel(out_month_path)
    out_month_path.save()
    out_month_path.close()
    print("各区每月提现统计完成")

# 按照每天明细和每天汇总进行汇总
def divideSheet():
    for i in range(rows):
        temp = data['提现时间'][i]
        temp_day = temp[5:10]
        if temp_day not in day_list:
            day_list.append(temp_day) #将几月几号保存到list中
    print(day_list)
    for day in day_list:
        new_df = pd.DataFrame()
        for i in range(0,rows):
            if data['提现时间'][i][5:10] == day:
                new_df = pd.concat([new_df,data.iloc[[i],:]],axis = 0,ignore_index=True)
        new_df.to_excel(defaultUrl+"\每天明细\\"+str(day)+".xls",sheet_name=day,index=False)

        day_cash_path = defaultUrl+"\每天明细\{}.xls".format(day)
        print(day_cash_path)
        # 按区域统计每张表的金额
        out_cash_path = pd.ExcelWriter(defaultUrl+"\每天汇总\{}统计.xls".format(day))
        day_df = pd.read_excel(day_cash_path) #读取每一天提现表格

        day_df_size = day_df.groupby(['区级平台名称'],as_index=False).size().to_frame('提现金额')
        #对区域列进行分类汇总计数
        # day_df_size = day_df.groupby(['区级平台名称'],as_index=False).size() #对区域列进行分类汇总计数
        print(day_df_size)
        (day_df_size*10).to_excel(out_cash_path)
        out_cash_path.save()
        out_cash_path.close()

        # # 每个表最下放加上总计并统计
        # statistic_num_path = r"D:\learn\personalPrograms\algorithmTrainningPython\bankDetail\3月份\{}统计.xls".format(day)

# 按照银行数据进行统计，显示结果
def bank_month_cash(bank_input):
    f = open(bank_input, encoding='utf-8')
    line = f.readlines()[0].split('|')
    print(line[1])
    bank_get_count.append(int(line[1]))

# 统计每月每天的提现汇总



if __name__ == '__main__':
    for num in range(301,332,1):
        bank_input = r"D:\learn\personalPrograms\algorithmTrainningPython\bankDetail\bankTotal\BOCDZ_52210151_20210{}.txt".format(num)
        bank_month_cash(bank_input)
    print(bank_get_count)
    total = 0
    for i in range(0,len(bank_get_count)):
        total += bank_get_count[i]
    print("银行日常提现条数统计：" + str(total))
    divedeRegion()
    divideSheet()
