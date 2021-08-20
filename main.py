import copy
from timeline import get_timeline
from box import get_box
from liner_pro import slove
from chara import list_to_string
from box import get_person_num
import time
import traceback
import json

boss_volume = [600, 800, 1000, 1200, 2000]
try:
    homework = []
    able_matrix = []
    boxtable, dao = get_box("box表.xlsx")
    timeline = get_timeline("轴表.xlsx")
    borrow = []
except:
    traceback.print_exc()
    c = input("出现错误，可能是你的错误或者软件错误，输入回车结束")
    exit(0)

this_work_can_use = 0


def check_without_conflict(now_work, now_brrow):
    # 判断套餐是否冲突，如果不冲突则加入列表
    global dao
    global borrow
    tmp = []
    tot_limit = {}
    for tot in range(len(now_brrow)):
        for t in now_work[tot]["chara"]:
            if t != now_brrow[tot]:
                tmp.append(t)
                if t in now_work[tot]["limited"]:
                    tot_limit[t] = now_work[tot]["limited"][t]
    tmp.sort()
    for j in range(len(tmp) - 1):
        if tmp[j] == tmp[j + 1]:
            return 0

    if this_work_can_use == 0:
        homework.append(copy.deepcopy(now_work))
        able_matrix.append([0] * get_person_num())
        borrow.append([[] for _ in range(get_person_num())])

    for i, name in enumerate(boxtable):
        if able_matrix[-1][i] == 0 and len(now_brrow) <= dao[i]:
            can_use = True
            for key in tmp:
                if key not in boxtable[name]:
                    can_use = False
                    break
                if key in tot_limit and boxtable[name][key] not in tot_limit[key]:
                    can_use = False
                    break
            if can_use:
                able_matrix[-1][i] = 1
                for t in range(len(now_brrow)):
                    borrow[-1][i].append(
                        now_brrow[t] if now_brrow[t] not in now_work[t]["limited"] else
                        now_brrow[t] + ' ' + list_to_string(now_work[t]["limited"][now_brrow[t]])
                    )

    return 1


def check_char(now_work):
    # 枚举每个套餐的借人情况，判断是否冲突
    global able_matrix
    global homework
    global boxtable
    global borrow
    global this_work_can_use
    this_work_can_use = 0

    for x in now_work[0]["borrow"]:
        if len(now_work) >= 2:
            for y in now_work[1]["borrow"]:
                if len(now_work) >= 3:
                    for z in now_work[2]["borrow"]:
                        this_work_can_use += check_without_conflict(now_work, [x, y, z])
                else:
                    this_work_can_use += check_without_conflict(now_work, [x, y])
        else:
            this_work_can_use += check_without_conflict(now_work, [x])


def dfs():
    global timeline
    for i in range(len(timeline)):
        now_work = [timeline[i]]
        check_char(now_work)
        for j in range(i + 1, len(timeline)):
            now_work = [timeline[i], timeline[j]]
            check_char(now_work)
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
    # a = "2021-02-18 10:00:00"
    # begintime = time.mktime(time.strptime(a, "%Y-%m-%d %H:%M:%S"))
    # if time.time() - begintime > 60 * 60 * 72:
    #     print("软件过期")
    #     exit(0)
    try:
        gen_homework(timeline)
        print("当前轴所能组合的分刀数量：", len(homework))
        with open("./进度.txt", "r", encoding='utf-8') as pf:
            need_to_defeat = json.load(pf)
        slove(able_matrix, homework, boxtable, copy.deepcopy(need_to_defeat), borrow)
        c = input("输入回车结束")
    except:
        traceback.print_exc()
        c = input("出现错误，可能是你的输入错误或者软件错误，输入回车结束")
