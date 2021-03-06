from pulp import *
import xlwt
from chara import list_to_string
from box import get_person_num
from time import time


def slove(able_matrix, homework, box, need_to_defeat, borrow):
    patho = os.path.join(os.getcwd(), 'data', 'cbc.exe')
    # print(patho)
    problem = LpProblem("Ads_Optimization", LpMinimize)
    var_matrix = []
    begin_time = time()
    for i in range(len(able_matrix)):
        tmp_list = []
        for j in range(get_person_num()):
            ud_tmp = LpVariable("%d_%d_var" % (i, j), lowBound=0, upBound=able_matrix[i][j], cat=const.LpBinary, e=None)
            tmp_list.append(ud_tmp)
            if able_matrix[i][j] == 0:
                problem += ud_tmp == 0
        var_matrix.append(tmp_list)

    for x in range(get_person_num()):
        problem += lpSum([
            var_matrix[i][x]
            for i in range(len(able_matrix))
        ]) <= 1

    person_num = get_person_num()
    for x in need_to_defeat:
        if need_to_defeat[x] != 0:
            problem += lpSum([
                homework[i][y]['soccer'] * var_matrix[i][j]
                for i in range(len(able_matrix))
                for j in range(person_num)
                for y in range(3)
                if homework[i][y]['boss'] == x
            ]) >= need_to_defeat[x]

    problem += lpSum([
        var_matrix[i][j]
        for i in range(len(able_matrix))
        for j in range(person_num)
        for y in range(3)
        if homework[i][y]['boss'][0] != 'd'
    ])
    print("录入完成\n请耐心等待几分钟，如果超过10min，一般为无解\n如果无解，请调整轴，box，或者进度，求解时间跟分刀可能数正相关\n或者删掉d轴进行近似求解")
    solver = COIN_CMD(path=patho,
                      msg=False)
    can_solve = problem.solve(solver)

    if can_solve == 1:
        tot = 0
        for i in range(len(able_matrix)):
            for j in range(get_person_num()):
                tot += int(var_matrix[i][j].varValue)
        print("出刀人数：", tot)
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
        worksheet.col(1).width = 256 * 40
        worksheet.col(7).width = 256 * 60
        worksheet.col(9).width = 256 * 15
        worksheet.col(10).width = 256 * 40
        boss_defeat = {}
        homework_num = {}
        for i in range(len(homework)):
            homework_num[i] = 0
        for x in need_to_defeat:
            if need_to_defeat[x] != 0:
                boss_defeat[x] = []
        for i in range(get_person_num()):

            worksheet.write(i * 3, 0, label=name_list[i])
            worksheet.write(i * 3, 1, label='待定')
            worksheet.write(i * 3 + 1, 1, label='待定')
            worksheet.write(i * 3 + 2, 1, label='待定')

            for j in range(len(able_matrix)):
                if int(var_matrix[j][i].varValue) == 1:
                    homework_num[j] += 1
                    for u in range(3):
                        if need_to_defeat[homework[j][u]["boss"]] > 0:
                            boss_defeat[homework[j][u]["boss"]].append([name_list[i], homework[j][u]])
                            worksheet.write(i * 3 + u, 1, label=list_to_string(homework[j][u]["chara"]))
                            output += 1
                            worksheet.write(i * 3 + u, 2, label=homework[j][u]["boss"])
                            worksheet.write(i * 3 + u, 3, label=str(homework[j][u]["soccer"]))
                            worksheet.write(i * 3 + u, 4, label="借 " + borrow[j][i][u])
                            need_to_defeat[homework[j][u]["boss"]] -= homework[j][u]["soccer"]
        line_no = 0
        for i, x in enumerate(boss_defeat):
            worksheet.write(line_no, 6, label=f"{len(boss_defeat[x])}人打{x}")
            for j, (person_name, work) in enumerate(boss_defeat[x]):
                worksheet.write(line_no, 7,
                                label=f"{person_name} 打轴 {list_to_string(work['chara'])} 伤害{work['soccer']}w")
                line_no += 1
            line_no += 1

        line_no = 0
        for x in homework_num:
            if homework_num[x] != 0:
                worksheet.write(line_no, 9,
                                label=f"{homework_num[x]}人打 {homework[x][0]['boss']}-{homework[x][1]['boss']}-{homework[x][2]['boss']}")
                worksheet.write(line_no, 10,
                                label=f"{list_to_string(homework[x][0]['chara'])} {homework[x][0]['soccer']}w")
                worksheet.write(line_no + 1, 10,
                                label=f"{list_to_string(homework[x][1]['chara'])} {homework[x][1]['soccer']}w")
                worksheet.write(line_no + 2, 10,
                                label=f"{list_to_string(homework[x][2]['chara'])} {homework[x][2]['soccer']}w")
                line_no += 4
        # 保存
        workbook.save('排刀表.xls')
        print("出刀数: ", output)
    else:
        print("无解，请更新box，轴，或者调整目标周目")
    return can_solve
