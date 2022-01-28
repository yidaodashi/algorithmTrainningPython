# _*_ coding:utf-8 _*_
# Created by lzl
# TIME: 2021/2/20 16:33

import pygame
import sys
import random
#全局定义
SCREEN_X = 600
SCREEN_Y = 600

# 蛇类
# 点以25为单位

class Snake(object):
    # 初始化各种需要的属性 （开始时默认向右、身体块x5)
    def __init__(self):
        self.dirction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.addnode()

            # 无论何时 都是在前端增加蛇蛇块
    def addnode(self):
        left, top = (0,0)
        if self.body:
            left,top = (self.body[0].left,self.body[0].top)
        node = pygame.Rect(left,top,25,25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)

    # 删除最后一个块
    def delnode(self):
        self.body.pop()
    # 死亡判断
    def isdead(self):
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
            # 撞自己
        if self.body[0] in self.body[1:]:
            return True
        return False
    # 移动
    def move(self):
        self.addnode()
        self.delnode()

        # 改变方向 但是左右、上下不能被逆向改变

    def changedirection(self, curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if curkey in LR + UD:
            if (curkey in LR) and (self.dirction in LR):
                return
            if (curkey in UD) and (self.dirction in UD):
                return
            self.dirction = curkey


def main():
    pass

if __name__ == '__main__':
    main()