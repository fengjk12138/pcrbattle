# coding=utf-8
import xlrd
import chara

person_num = 30


def get_name(name):
    id_ = chara.name2id(name)
    confi = 100
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
    if (confi < 60):  # 人物名字不正确
        raise AssertionError("不认识", name)
    return chara.id2name(id_)


def get_person_num():
    global person_num
    return person_num


# 打开文件
def get_box(filename):
    global person_num
    out = {}

    data = xlrd.open_workbook(filename)
    # 通过文件名获得工作表,获取工作表1
    table = data.sheet_by_name(data.sheet_names()[0])
    name = []
    for x in range(3, table.ncols - 3):
        name.append(get_name(table.cell(0, x).value))
    person_num = table.nrows - 1

    dao = [3] * person_num

    for i in range(1, table.nrows):
        out[table.cell(i, 2).value] = {}
        for j in range(3, table.ncols - 3):
            if table.cell_type(i, j) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                myval = table.cell(i, j).value
                if isinstance(myval, float):
                    myval = int(myval)
                myval = str(myval)
                out[table.cell(i, 2).value][name[j - 3]] = myval.strip()
        for j in range(table.ncols - 3, table.ncols):
            if table.cell_type(i, j) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                myval = table.cell(i, j).value
                if isinstance(myval, float):
                    myval = int(myval)
                myval = str(myval).strip().split()
                for tmp in myval:
                    truename = get_name(tmp)
                    if truename in out[table.cell(i, 2).value]:
                        out[table.cell(i, 2).value].pop(truename)
                dao[i - 1] -= 1
    return out, dao


# def executable(command):
#     if os.path.isabs(command):
#         if os.path.exists(command) and os.access(command, os.X_OK):
#             return command
#     for path in os.environ.get("PATH", []).split(os.pathsep):
#         new_path = os.path.join(path, command)
#         if os.path.exists(new_path) and os.access(new_path, os.X_OK):
#             return os.path.join(path, command)
#     return False
#     executable = staticmethod(executable)
#
if __name__ == '__main__':
    x, y = get_box("box表.xlsx")
    print(y)
    # print(executable('glpsol.exe'))
