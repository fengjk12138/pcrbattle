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
    boxtable = get_box("box表.xlsx")
    timeline = get_timeline("轴表.xlsx")
    borrow = []
except:
    traceback.print_exc()
    c = input("出现错误，可能是你的错误或者软件错误，输入回车结束")
    exit(0)


def check_char(now_work):
    # 判断一个套餐是否可行，并且更新各个人是否能打这个套餐，屎山
    global able_matrix
    global homework
    global boxtable
    global borrow
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
                    able_matrix.append([0 for _ in range(get_person_num())])
                    borrow.append([[] for _ in range(get_person_num())])

                for i, name in enumerate(boxtable):
                    if able_matrix[len(homework) - 1][i] == 0:
                        can_use = True
                        for key in tmp:
                            if key not in boxtable[name]:
                                can_use = False
                                break
                            if key in tot_limit and boxtable[name][key] not in tot_limit[key]:
                                can_use = False
                                break
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
    # a = "2021-02-18 10:00:00"
    # begintime = time.mktime(time.strptime(a, "%Y-%m-%d %H:%M:%S"))
    # if time.time() - begintime > 60 * 60 * 72:
    #     print("软件过期")
    #     exit(0)
    try:
        gen_homework(timeline)
        print("当前轴所能组合的分刀数量：", len(homework))
        with open("./进度.txt", "r") as pf:
            need_to_defeat = json.load(pf)
        print("请耐心等待10~20min，如果超过20min，一般为无解，请调整轴，box，或者进度，求解时间跟分刀可能数正相关")
        slove(able_matrix, homework, boxtable, copy.deepcopy(need_to_defeat), borrow)
        c = input("输入回车结束")
    except:
        traceback.print_exc()
        c = input("出现错误，可能是你的错误或者软件错误，输入回车结束")
