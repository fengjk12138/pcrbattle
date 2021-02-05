from pulp import *
import xlwt
from chara import list_to_string

problem = LpProblem("Ads Optimization", LpMaximize)
boss_name = ['1', '2', '3', '4', '5']
boss_status = ['a', 'b', 'c']


def slove(able_matrix, homework, box):
    global problem
    var_matrix = []
    for i in range(len(able_matrix)):
        tmp_list = []
        for j in range(30):
            tmp_list.append(
                LpVariable(f"{str(i)} {str(j)}", lowBound=0, upBound=able_matrix[i][j], cat='Binary', e=None))
        var_matrix.append(tmp_list)
    for j in range(30):
        tmp_dinner = var_matrix[0][j]
        for i in range(1, len(able_matrix)):
            tmp_dinner = tmp_dinner + var_matrix[i][j]
        problem += tmp_dinner <= 1  # 这个人至少(可能)出1个套餐
    need_to_defeat = {
        'a1': 600 * 3,
        'a2': 800 * 3,
        'a3': 1000 * 3,
        'a4': 1200 * 3,
        'a5': 2000 * 3,
        'b1': 600 * 1,
        'b2': 800 * 1,
        'b3': 1000 * 1,
        'b4': 1200 * 1,
        'b5': 2000 * 0.7,
        'c1': 0,
        'c2': 0,
        'c3': 0,
        'c4': 0,
        'c5': 0,
        'last': 'b3'
    }
    plan_to_defeat = {
        'a1': None,
        'a2': None,
        'a3': None,
        'a4': None,
        'a5': None,
        'b1': None,
        'b2': None,
        'b3': None,
        'b4': None,
        'b5': None,
        'c1': None,
        'c2': None,
        'c3': None,
        'c4': None,
        'c5': None,
    }

    obj = None
    for i in range(len(able_matrix)):
        for j in range(30):
            if able_matrix[i][j]:
                for y in homework[i]:
                    # if y['boss'] == need_to_defeat['last']:
                    #     if obj is None:
                    #         obj = y["soccer"] * var_matrix[i][j]
                    #     else:
                    #         obj = y["soccer"] * var_matrix[i][j] + obj
                    if plan_to_defeat[y["boss"]] is not None:
                        plan_to_defeat[y["boss"]] = y["soccer"] * var_matrix[i][j] + plan_to_defeat[y["boss"]]
                    else:
                        plan_to_defeat[y["boss"]] = y["soccer"] * var_matrix[i][j]
    for x in plan_to_defeat:
        if plan_to_defeat[x] is not None and need_to_defeat[x] != 0:
            problem += plan_to_defeat[x] >= need_to_defeat[x]
            # problem += plan_to_defeat[x] <= need_to_defeat[x] + 2?\000
    # problem += obj
    # print(obj)
    # obj = None
    # for i in range(len(able_matrix)):
    #     for j in range(30):
    #         if able_matrix[i][j] != 0:
    #             if obj is None:
    #                 obj = var_matrix[i][j] * (
    #                         homework[i][0]["soccer"] + homework[i][1]["soccer"] + homework[i][2]["soccer"])
    #             else:
    #                 obj = var_matrix[i][j] * (
    #                         homework[i][0]["soccer"] + homework[i][1]["soccer"] + homework[i][2]["soccer"]) + obj
    # problem += obj

    obj = None
    for i in range(len(able_matrix)):
        for j in range(30):
            if obj is None:
                obj = var_matrix[i][j]
            else:
                obj = var_matrix[i][j] + obj
    problem += obj

    # obj = None
    # for i in range(len(able_matrix)):
    #     for j in range(30):
    #         if obj is None:
    #             obj = var_matrix[i][j]
    #         else:
    #             obj = var_matrix[i][j] + obj
    # problem += obj

    can_solve = problem.solve()
    print(can_solve)
    if can_solve == 1:
        tot = 0
        for i in range(len(able_matrix)):
            for j in range(30):
                tot += int(var_matrix[i][j].varValue)
        print("出刀人数：", tot)
        print("最后一个王可造成伤害：", int(value(problem.objective)))
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

        # 写入excel
        # 参数对应 行, 列, 值
        name_list = []
        for key in box:
            name_list.append(key)
        output = 0
        for i in range(30):
            worksheet.write(i * 3, 0, label=name_list[i])
            worksheet.write(i * 3, 1, label='待定')
            worksheet.write(i * 3 + 1, 1, label='待定')
            worksheet.write(i * 3 + 2, 1, label='待定')
            for j in range(len(able_matrix)):
                if int(var_matrix[j][i].varValue) == 1:
                    for u in range(3):
                        if need_to_defeat[homework[j][u]["boss"]] >= 0 or \
                                homework[j][u]["boss"] == need_to_defeat['last']:
                            worksheet.write(i * 3 + u, 1, label=list_to_string(homework[j][u]["chara"]))
                            output += 1
                            worksheet.write(i * 3 + u, 2, label=homework[j][u]["boss"])
                            worksheet.write(i * 3 + u, 3, label=str(homework[j][u]["soccer"]))
                            need_to_defeat[homework[j][u]["boss"]] -= homework[j][u]["soccer"]
        # 保存
        workbook.save('排刀表.xls')
        print("出刀数: ", output)
