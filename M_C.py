# -*- coding: utf-8 -*-
import operator

__metaclass__ = type

M = 5  # 传教士
C = 5  # 野人
K = 3  # 每船乘坐人数
ss = []  # ss用来存所有的子类
open_list = []  # open表
closed_list = []  # closed表


class State:
    def __init__(self, m, c, b):
        self.m = m
        self.c = c
        self.b = b  # b = 1: 船在左岸；b = 0: 船在右岸
        self.g = 0
        self.f = 0
        self.father = None
        self.node = [m, c, b]

init = State(M, C, 1)  # 初始节点
goal = State(0, 0, 0)  # 目标


def safe(s):
    if s.m > M or s.m < 0 or s.c > C or s.c < 0 or (s.m != 0 and s.m < s.c) or (s.m != M and M - s.m < C - s.c):
        return False
    else:
        return True


# 启发函数
def h(s):
    return s.m + s.c - K * s.b
    # return M - s.m + C - s.c

def equal(a, b):
    if a.node == b.node:
        return True


def back(new, s):  # 判断s.father是否与new重复
    if s.father is None:
        return False
    return equal(new, s.father)


def open_sort(l):
    the_key = operator.attrgetter('f')  # 指定属性排序的key
    l.sort(key=the_key)


# 扩展节点时在open表和closed表中找原来是否存在相同mcb属性的节点
def in_list(new, l):
    for item in l:
        if new.node == item.node:
            return True, item
    return False, None


def A_star(s):
    global open_list, closed_list
    open_list = [s]
    closed_list = []
    # print 'open list:'
    # print 'closed list:'  # 选择打印open表或closed表变化过程
    print s.node
    while open_list:  # open表非空
        get = open_list[0]  # 取出open表第一个元素get
        if get.node == goal.node:  # 判断是否为目标节点
            return get
        open_list.remove(get)  # 将get从open表移出
        closed_list.append(get)  # 将get加入closed表

        # 以下得到一个get的新子节点new并考虑是否放入openlist
        for i in xrange(M):  # 上船传教士
            for j in xrange(C):  # 上船野人
                # 船上非法情况
                if i + j == 0 or i + j > K or (i != 0 and i < j):
                    continue
                if get.b == 1:  # 船在左岸
                    new = State(get.m - i, get.c - j, 0)
                    ss.append(new)
                else:  # 船在右岸
                    new = State(get.m + i, get.c + j, 1)
                    ss.append(new)

                if not safe(new) or back(new, get):  # 状态非法或new折返了
                    ss.pop()
                else:
                    new.father = get
                    new.g = get.g + 1
                    new.f = get.g + h(get)  # f = g + h

                    # 如果new在open表中(只关注m,c,b的值)
                    if in_list(new, open_list)[0]:
                        old = in_list(new, open_list)[1]
                        if new.f < old.f:  # new的f<open表相同状态的f
                            open_list.remove(old)
                            open_list.append(new)
                            open_sort(open_list)
                        else:
                            pass

                    # 继续，如果new在closed表中
                    elif in_list(new, closed_list)[0]:
                        old = in_list(new, closed_list)[1]
                        if new.f < old.f:
                            # 将old从closed删除，并重新加入open
                            closed_list.remove(old)
                            open_list.append(new)
                            open_sort(open_list)
                        else:
                            pass
                    else:
                        open_list.append(new)
                        open_sort(open_list)
                        # 打印open表或closed表
                        for o in open_list:
                        # for o in closed_list:
                            print o.node,
                        print


def printPath(f):
    if f is None:
        return
    printPath(f.father)
    print f.node  


if __name__ == '__main__':
    print '有%d个传教士，%d个野人，船容量:%d' % (M, C, K)
    final = A_star(init)
    if final:
        print '有解，解为：'
        printPath(final)
    else:
        print '无解！'
