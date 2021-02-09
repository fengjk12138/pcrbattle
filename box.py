# coding=utf-8
import xlrd
import chara

person_num = 30


def get_name(name):
    id_ = chara.name2id(name)
    confi = 100
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
    assert confi >= 60  # 人物名字不正确

    return chara.id2name(id_)


# 打开文件
def get_box(filename):
    global person_num
    out = {}
    data = xlrd.open_workbook(filename)
    # 通过文件名获得工作表,获取工作表1
    table = data.sheet_by_name(data.sheet_names()[0])
    name = []
    for x in range(3, table.ncols):
        name.append(get_name(table.cell(0, x).value))
    person_num = table.nrows - 1
    for i in range(1, table.nrows):
        out[table.cell(i, 2).value] = {}
        for j in range(3, table.ncols):
            if table.cell_type(i, j) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                out[table.cell(i, 2).value][name[j - 3]] = 1
    return out


if __name__ == '__main__':
    # x = get_box("demo.xlsx")
    print(get_name('狼'))
