# _*_ coding:utf-8 _*_
# Created by lzl
# 数组算法训练创建类
# TIME: 2021/2/4 13:06
import collections

class Solution:
    # 数组重复数字返回
    def duplicate(self,numbers,duplication):
        #  方法一 排序后遍历 时间O(n*logn) 空间O(1)
        # if(not numbers)&len(numbers) == 1:
        #     return False
        # numbers.sort()
        # temp = numbers[0]
        # for i in range(1,len(numbers)):
        #     if temp == numbers[i]:
        #         duplication[0] = temp
        #         print(duplication[0])
        #         return True
        #     temp = numbers[i]
        # return False
        # 方法二 哈希表 时间O(1)  空间O(n)
        # dic = {}
        # for i in numbers:
        #     if i in dic and dic[i] == 1:
        #         duplication[0] = i
        #         print(duplication[0])
        #         return True
        #     dic[i] = 1
        # return False
        #  方法三 下标定位法 时间O(n) 空间O(1)
        for i in range(len(numbers)):
            while i != numbers[i]:
                if numbers[i] == numbers[numbers[i]]:
                    duplication[0] = numbers[i]
                    print(duplication[0])
                    return True
                temp = numbers[i]
                numbers[i] = numbers[temp]
                numbers[temp] =temp
        return False
        # 方法四 内置函数
        # if len(numbers) == len(set(numbers)):
        #     return False
        # duplication[0]  = collections.Counter(numbers).most_common(1)[0][0]
        # print(duplication[0])
        # return True


numbers = [2, 3, 1, 0, 2, 5, 3]
duplication = {}
Solution.duplicate(super,numbers,duplication)
