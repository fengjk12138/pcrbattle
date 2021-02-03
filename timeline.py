import xlrd
from box import get_name

boss_name = ['1', '2', '3', '4', '5']
boss_status = ['a', 'b', 'c']


def get_timeline(filename):
    out = []
    data = xlrd.open_workbook(filename)
    # 通过文件名获得工作表,获取工作表1
    table = data.sheet_by_name(data.sheet_names()[0])
    for i in range(1, table.nrows):
        boss = table.cell(i, 0).value
        if len(boss) != 2 or boss[0] not in boss_status or boss[1] not in boss_name:
            print(boss + "不是能识别的boss")
            exit(0)
        name = table.cell(i, 1).value
        true_name = []
        for x in name.strip().split():
            true_name.append(get_name(x))
        true_name.sort()
        for i in range(len(true_name) - 1):
            if true_name[i] == true_name[i + 1]:
                print(name + "阵容有两个相同的人物")
                exit(0)
        assert len(true_name) == 5  # 一个阵容5个人
        hurt = table.cell(i, 2).value
        if hurt[-1] != 'w' or not hurt[0:-1].isdigit():
            print(hurt + "不是合理伤害")
            exit(0)
        tmp = {"chara": true_name, "soccer": int(hurt[0:-1]), "boss": boss}
        out.append(tmp)
    return out
