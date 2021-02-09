from pulp import *
import xlwt
from chara import list_to_string
from box import person_num


def slove(able_matrix, homework, box, need_to_defeat, borrow):
    problem = LpProblem("Ads Optimization", LpMinimize)
    var_matrix = []
    for i in range(len(able_matrix)):
        tmp_list = []
        for j in range(person_num):
            tmp_list.append(
                LpVariable(f"{str(i)} {str(j)}", lowBound=0, upBound=able_matrix[i][j], cat='Binary', e=None))
        var_matrix.append(tmp_list)
    for j in range(person_num):
        tmp_dinner = var_matrix[0][j]
        for i in range(1, len(able_matrix)):
            tmp_dinner = tmp_dinner + var_matrix[i][j]
        problem += tmp_dinner <= 1  # 这个人至少(可能)出1个套餐
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
        'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None,
    }

    obj = None
    for i in range(len(able_matrix)):
        for j in range(person_num):
            if able_matrix[i][j]:
                for y in homework[i]:
                    if y['boss'][0] != 'd':
                        if obj is None:
                            obj = var_matrix[i][j]
                        else:
                            obj = obj + var_matrix[i][j]
                    if plan_to_defeat[y["boss"]] is not None:
                        plan_to_defeat[y["boss"]] = y["soccer"] * var_matrix[i][j] + plan_to_defeat[y["boss"]]
                    else:
                        plan_to_defeat[y["boss"]] = y["soccer"] * var_matrix[i][j]

    for x in plan_to_defeat:
        if plan_to_defeat[x] is not None and need_to_defeat[x] != 0:
            problem += plan_to_defeat[x] >= need_to_defeat[x]
            # problem += plan_to_defeat[x] <= need_to_defeat[x] + 150
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

    # obj = None
    # for i in range(len(able_matrix)):
    #     for j in range(person_num):
    #         if obj is None:
    #             obj = var_matrix[i][j]
    #         else:
    #             obj = var_matrix[i][j] + obj
    # problem += obj

    # obj = None
    # for i in range(len(able_matrix)):
    #     for j in range(person_num):
    #         if obj is None:
    #             obj = var_matrix[i][j]
    #         else:
    #             obj = var_matrix[i][j] + obj
    problem += obj
    # solver = CPLEX_CMD()
    can_solve = problem.solve()
    print(can_solve)
    if can_solve == 1:
        tot = 0
        for i in range(len(able_matrix)):
            for j in range(person_num):
                tot += int(var_matrix[i][j].varValue)
        print("出刀人数：", tot)
        # print("完整刀伤害人数：", int(value(problem.objective)))
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
        for i in range(person_num):
            worksheet.write(i * 3, 0, label=name_list[i])
            worksheet.write(i * 3, 1, label='待定')
            worksheet.write(i * 3 + 1, 1, label='待定')
            worksheet.write(i * 3 + 2, 1, label='待定')
            for j in range(len(able_matrix)):
                if int(var_matrix[j][i].varValue) == 1:
                    for u in range(3):
                        if need_to_defeat[homework[j][u]["boss"]] > 0:
                            worksheet.write(i * 3 + u, 1, label=list_to_string(homework[j][u]["chara"]))
                            output += 1
                            worksheet.write(i * 3 + u, 2, label=homework[j][u]["boss"])
                            worksheet.write(i * 3 + u, 3, label=str(homework[j][u]["soccer"]))
                            worksheet.write(i * 3 + u, 4, label="借 " + borrow[j][i][u])
                            need_to_defeat[homework[j][u]["boss"]] -= homework[j][u]["soccer"]
        # 保存
        workbook.save('排刀表.xls')
        print("出刀数: ", output)
    return can_solve
