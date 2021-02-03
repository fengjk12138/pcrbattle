from pulp import *

problem = LpProblem("Ads Optimization", LpMaximize)
boss_name = ['1', '2', '3', '4', '5']
boss_status = ['a', 'b', 'c']


def slove(able_matrix, homework):
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
        'a1': 600 * 4,
        'a2': 800 * 3,
        'a3': 1000 * 3,
        'a4': 1200 * 3,
        'a5': 2000 * 3,
        'b1': 0,
        'b2': 0,
        'b3': 0,
        'b4': 0,
        'b5': 0,
        'c1': 0,
        'c2': 0,
        'c3': 0,
        'c4': 0,
        'c5': 0,
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
    for i in range(len(able_matrix)):
        for j in range(30):
            if able_matrix[i][j]:
                for y in homework[i]:
                    if plan_to_defeat[y["boss"]] is not None:
                        plan_to_defeat[y["boss"]] = y["soccer"] * var_matrix[i][j] + plan_to_defeat[y["boss"]]
                    else:
                        plan_to_defeat[y["boss"]] = y["soccer"] * var_matrix[i][j]
    for x in plan_to_defeat:
        if plan_to_defeat[x] is not None and need_to_defeat[x] != 0:
            problem += plan_to_defeat[x] >= need_to_defeat[x]
            # problem += plan_to_defeat[x] <= need_to_defeat[x] + 2?\000
    obj = None
    for i in range(len(able_matrix)):
        for j in range(30):
            if able_matrix[i][j] != 0:
                if obj is None:
                    obj = var_matrix[i][j] * (
                            homework[i][0]["soccer"] + homework[i][1]["soccer"] + homework[i][2]["soccer"])
                else:
                    obj = var_matrix[i][j] * (
                            homework[i][0]["soccer"] + homework[i][1]["soccer"] + homework[i][2]["soccer"]) + obj
    problem += obj
    print(problem)
    print(problem.solve())
    tot = 0
    for i in range(len(able_matrix)):
        for j in range(30):
            tot += int(var_matrix[i][j].varValue)
    print(tot)
    print(int(value(problem.objective)))
