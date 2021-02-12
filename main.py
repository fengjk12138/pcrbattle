import json
import copy
import os
import box
from timeline import get_timeline
from box import get_box
from liner_pro import slove
from chara import list_to_string
from box import person_num

boss_volume = [600, 800, 1000, 1200, 2000]

homework = []
able_matrix = []
boxtable = get_box("box表.xlsx")
timeline = get_timeline("轴表.xlsx")
borrow = []


def check_char(now_work):
    # 判断一个套餐是否可行，并且更新各个人是否能打这个套餐，屎山
    global able_matrix
    global homework
    global boxtable
    global borrow
    global person_num
    is_work = False

    for x in now_work[0]["borrow"]:
        for y in now_work[1]["borrow"]:
            for z in now_work[2]["borrow"]:
                tmp = []
                tot_limit = {}
                for t in now_work[0]["chara"]:
                    if t != x:
                        tmp.append(t)
                        if t in now_work[0]["limited"]:
                            tot_limit[t] = now_work[0]["limited"][t]
                for t in now_work[1]["chara"]:
                    if t != y:
                        tmp.append(t)
                        if t in now_work[1]["limited"]:
                            tot_limit[t] = now_work[1]["limited"][t]
                for t in now_work[2]["chara"]:
                    if t != z:
                        tmp.append(t)
                        if t in now_work[2]["limited"]:
                            tot_limit[t] = now_work[2]["limited"][t]
                is_next = False
                tmp.sort()
                for j in range(len(tmp) - 1):
                    if tmp[j] == tmp[j + 1]:
                        is_next = True
                        break
                if is_next:
                    continue
                if not is_work:
                    homework.append(copy.deepcopy(now_work))
                    is_work = True
                    able_matrix.append([0 for _ in range(person_num)])
                    borrow.append([[] for _ in range(person_num)])

                for i, name in enumerate(boxtable):
                    if able_matrix[len(homework) - 1][i] == 0:
                        can_use = True
                        for key in tmp:
                            if key not in boxtable[name]:
                                can_use = False
                                break
                            # if key in tot_limit and boxtable[name][key] not in tot_limit[key]:
                            #     can_use = False
                            #     break
                        if can_use:
                            able_matrix[len(homework) - 1][i] = 1
                            borrow[len(homework) - 1][i].append(
                                x if x not in now_work[0]["limited"] else x + list_to_string(now_work[0]["limited"][x]))
                            borrow[len(homework) - 1][i].append(
                                y if y not in now_work[1]["limited"] else y + list_to_string(now_work[1]["limited"][y]))
                            borrow[len(homework) - 1][i].append(
                                z if z not in now_work[2]["limited"] else z + list_to_string(now_work[2]["limited"][z]))
    return is_work


def dfs():
    global timeline
    for i in range(len(timeline)):
        for j in range(i + 1, len(timeline)):
            for k in range(j + 1, len(timeline)):
                now_work = [timeline[i], timeline[j], timeline[k]]
                check_char(now_work)


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
    dfs()


def gen_next_defeat(need_to_defeat):
    global boss_volume
    stat = int(need_to_defeat['now'].split('-')[0])
    boss = int(need_to_defeat['now'].split('-')[1])
    if boss <= 4:
        boss += 1
        need_to_defeat[str(f'{stat}-{boss}')] += boss_volume[boss]


if __name__ == "__main__":
    gen_homework(timeline)
    print(len(homework))
    need_to_defeat = {
        'a1': 0,
        'a2': 0,
        'a3': 0,
        'a4': 0,
        'a5': 0,
        'b1': 0,
        'b2': 0,
        'b3': 0,
        'b4': 0,
        'b5': 0,
        'c1': 600 * 3,
        'c2': 800 * 3,
        'c3': 1000 * 3,
        'c4': 1200 * 3,
        'c5': 2000 * 3,
        'd1': 0, 'd2': 0, 'd3': 0, 'd4': 0, 'd5': 0,
    }
    # print(len(boxtable))
    can_solve = slove(able_matrix, homework, boxtable, copy.deepcopy(need_to_defeat), borrow, 0)
    if can_solve != -1:
        slove(able_matrix, homework, boxtable, copy.deepcopy(need_to_defeat), borrow, can_solve)
    else:
        print("无解")
