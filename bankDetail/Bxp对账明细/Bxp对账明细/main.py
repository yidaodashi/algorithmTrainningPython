import xlrd, xlwt
import datetime


sql_user_info = "UPDATE cm_reward_user_info SET bonus = bonus+10 where user_name ='{}'"
sql_areaplate_info = "UPDATE cm_reward_areaplate_info SET areaplate_money = areaplate_money-10 WHERE areaplate_acount ='{}'"
sql_bank_statement = "DELETE FROM cm_reward_bank_statement WHERE case_id = '{}' LIMIT 1"


def order_by_time(element):
    return datetime.datetime.strptime(element["time"], "%Y-%m-%d %H:%M:%S")


def get_bxp_case_num(bxp_mx_path):
    bxp_total_num = 0
    bxp_case_info = {}
    bxpworkbook = xlrd.open_workbook(bxp_mx_path)
    bxpsheet = bxpworkbook.sheet_by_index(0)
    for i in range(bxpsheet.nrows):
        if i < 3: continue
        bxp_total_num += 1
        value = bxpsheet.row_values(i)
        vdic = {
            "case_id": value[0],
            "case_num": value[1],
            "user_name": value[5],
            "areaplate_code": value[4],
            "time": value[-1]
        }

        if value[1] not in bxp_case_info.keys():
            bxp_case_info[value[1]] = [vdic]
        else:
            bxp_case_info[value[1]].append(vdic)
    return bxp_case_info, bxp_total_num


def get_bank_case_num(bank_mx_path):
    bank_case_num = []
    bank_total_num = 0
    workbook = xlrd.open_workbook(bank_mx_path)
    sheet = workbook.sheet_by_index(0)
    for i in range(sheet.nrows):
        value = sheet.row_values(i)
        if i == 0:
            bank_total_num = value[1]
            continue

        bank_case_num.append(value[3])
    return bank_case_num, bank_total_num


def compare_case(bank_mx_path, bxp_mx_path):
    sql_list = []
    bank_case_num, bank_total_num = get_bank_case_num(bank_mx_path)
    bxp_case_info, bxp_total_num = get_bxp_case_num(bxp_mx_path)

    print("银行记录数：{}，百姓拍记录数：{}".format(bank_total_num, bxp_total_num))
    for casenum in bank_case_num:
        tag_value = bxp_case_info.get(casenum)
        if tag_value is None:
            print("百姓拍系统缺少一条银行提现记录：{}".format(casenum))
        else:
            if len(tag_value) > 1:
                print("=======> 百姓拍系统出现多条重复提现记录:")
                tag_value.sort(key=order_by_time, reverse=True)
                tag_value.pop(-1)
                for dic in tag_value:
                    user_name = dic.get("user_name")
                    case_id = dic.get("case_id")
                    areaplate_code = dic.get("areaplate_code")
                    sql_list.append(sql_user_info.format(user_name))
                    sql_list.append(sql_areaplate_info.format(areaplate_code))
                    sql_list.append(sql_bank_statement.format(case_id))

                    print("案件号：{}，用户名：{}，提现时间：{}，平台账户：{}".format(
                        dic.get("case_num"),
                        user_name,
                        dic.get("time"),
                        areaplate_code))
            else:
                continue

    for casenum in bxp_case_info.keys():
        if casenum not in bank_case_num:
            print("百姓拍系统存在一条提现记录不在银行提现明细中：/n", bxp_case_info.get(casenum))

    print(len(sql_list)/3)
    for sql in sql_list:
        print(sql, ";")


if __name__ == '__main__':
    num = 218
    bank_mx_path = r"E:\Python_worksapce_local\ExperimentDemos\Bxp对账明细\银行明细209-218\BOCDZ_52210151_20210{}.xls".format(num)
    bxp_mx_path = r"E:\Python_worksapce_local\ExperimentDemos\Bxp对账明细\银行明细209-218\银行流水明细表{}.xls".format(num)
    compare_case(bank_mx_path, bxp_mx_path)