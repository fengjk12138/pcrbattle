import xlrd
from box import get_name
import copy
from box import person_num

boss_name = ['1', '2', '3', '4', '5']
boss_status = ['a', 'b', 'c', 'd']


def get_timeline(filename):
    out = []
    data = xlrd.open_workbook(filename)
    # 通过文件名获得工作表,获取工作表1
    table = data.sheet_by_name(data.sheet_names()[0])
    for i in range(1, table.nrows):
        # 识别boss
        boss = table.cell(i, 0).value
        if len(boss) != 2 or boss[0] not in boss_status or boss[1] not in boss_name:
            print(boss + "不是能识别的boss")
            raise AssertionError(boss + "不是能识别的boss")

        # 识别阵容
        name = table.cell(i, 1).value
        true_name = []
        for x in name.strip().split():
            true_name.append(get_name(x))
        true_name.sort()
        for j in range(len(true_name) - 1):
            if true_name[j] == true_name[j + 1]:
                print(name + "阵容有两个相同的人物")
                raise AssertionError(name + "阵容有两个相同的人物")

        # 识别伤害
        hurt = table.cell(i, 2).value
        if hurt[-1] != 'w' or not hurt[0:-1].isdigit():
            print(hurt + "不是合理伤害")
            raise AssertionError(hurt + "不是合理伤害")

        # 识别借人
        borrow_name = None
        if table.cell_type(i, 3) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
            name = table.cell(i, 3).value
            borrow_name = []
            for x in name.strip().split():
                borrow_name.append(get_name(x))
            borrow_name.sort()

        if borrow_name is None:
            borrow_name = copy.deepcopy(true_name)

        # 识别轴限定rank，等级，星级，等等
        j = 4
        limit = {}
        while True:
            if j >= table.ncols or table.cell_type(i, j) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                break
            li = table.cell(i, j).value
            li = li.strip().split()
            name = get_name(li[0])

            if name not in true_name:
                print(name + "不在这个轴里面")
                raise AssertionError(name + "不在这个轴里面")
            if name in limit:
                print(name + "限定了两次")
                raise AssertionError(name + "限定了两次")
            limit[name] = li[1:]
            j += 1
        tmp = {
            "chara": true_name,
            "soccer": int(copy.deepcopy(hurt[0:-1])),
            "boss": boss,
            "borrow": borrow_name,
            "limited": limit
        }
        out.append(tmp)
    return out


if __name__ == '__main__':
    timelien = get_timeline("轴表.xlsx")
    print(timelien)
