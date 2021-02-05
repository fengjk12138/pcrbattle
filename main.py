import json
import copy
import os
import box
from timeline import get_timeline
from box import get_box
from liner_pro import slove
from chara import list_to_string

boss_volume = [6000000, 8000000, 10000000, 12000000, 20000000]

homework = []
able_matrix = []
boxtable = get_box("box表.xlsx")
timeline = get_timeline("轴表.xlsx")


def check_char(now_work):
    global able_matrix
    global homework
    global boxtable
    is_work = False
    for x in now_work[0]["borrow"]:
        for y in now_work[1]["borrow"]:
            for z in now_work[2]["borrow"]:
                tmp = {}
                for t in now_work[0]["chara"]:
                    if t != x:
                        tmp[t] = 1 if t not in tmp else tmp[t] + 1
                for t in now_work[1]["chara"]:
                    if t != y:
                        tmp[t] = 1 if t not in tmp else tmp[t] + 1
                for t in now_work[2]["chara"]:
                    if t != z:
                        tmp[t] = 1 if t not in tmp else tmp[t] + 1
                is_next = False
                for key in tmp:
                    if tmp[key] >= 2:
                        is_next = True
                        break
                if is_next:
                    continue
                if not is_work:
                    homework.append(copy.deepcopy(now_work))
                    is_work = True
                    able_matrix.append([0 for _ in range(30)])
                for i, name in enumerate(boxtable):
                    if able_matrix[len(homework) - 1][i] == 0:
                        can_use = True
                        for key in tmp:
                            if key not in boxtable[name]:
                                can_use = False
                                break
                        if can_use:
                            able_matrix[len(homework) - 1][i] = 1
    return is_work


def dfs(last, now_dict, now_work):
    if last >= len(now_dict):
        return
    for x in range(last, len(now_dict)):
        now_work.append(now_dict[x])
        if len(now_work) == 3 and check_char(now_work):
            pass
        else:
            dfs(x + 1, now_dict, now_work)
        now_work.pop()


def homework_to_string(homework):
    out_str = ""
    cnt = 0
    for x in homework:
        cnt += 1
        out_str += "套餐" + str(cnt) + ": \n" + \
                   x[0]["boss"] + " " + list_to_string(x[0]["chara"]) + " " + str(x[0]["soccer"]) + "w\n" + \
                   x[1]["boss"] + " " + list_to_string(x[1]["chara"]) + " " + str(x[1]["soccer"]) + "w\n" + \
                   x[2]["boss"] + " " + list_to_string(x[2]["chara"]) + " " + str(x[2]["soccer"]) + "w\n"
    return out_str


def gen_homework(timeline):
    dfs(0, timeline, [])


if __name__ == "__main__":
    gen_homework(timeline)
    print(len(homework))
    slove(able_matrix, homework, boxtable)
