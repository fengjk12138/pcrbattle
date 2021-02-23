from importlib import reload
from unicodedata import normalize
from pygtrie import CharTrie
from fuzzywuzzy import process
from zhconv import convert
import json
import _pcr_data

UNKNOWN = 1000
UnavailableChara = {
    1067,  # 穗希
    1069,  # 霸瞳
    1072,  # 可萝爹
    1073,  # 拉基拉基
    1102,  # 泳装大眼
}


def normalize_str(string) -> str:
    """
    规范化unicode字符串 并 转为小写 并 转为简体
    """
    # with open('./zhcdict.json', 'r', encoding='utf-8') as pf:
    #     dist_json = json.load(pf)
    string = normalize('NFKC', string)
    string = string.lower()
    # string = convert(string, 'zh-hans', dist_json)
    return string


class Roster:

    def __init__(self):
        self._roster = CharTrie()
        self.update()

    def update(self):
        reload(_pcr_data)
        self._roster.clear()
        for idx, names in _pcr_data.CHARA_NAME.items():
            for n in names:
                n = normalize_str(n)
                if n not in self._roster:
                    self._roster[n] = idx
        self._all_name_list = self._roster.keys()

    def get_id(self, name):
        name = normalize_str(name)
        return self._roster[name] if name in self._roster else UNKNOWN

    def guess_id(self, name):
        """@return: id, name, score"""
        name, score = process.extractOne(name, self._all_name_list, processor=normalize_str)
        return self._roster[name], name, score

    def get_true_name(self, id):
        """@return: name"""
        return _pcr_data.CHARA_NAME[int(id)][0]

    def parse_team(self, namestr):
        """@return: List[ids], unknown_namestr"""
        namestr = normalize_str(namestr.strip())
        team = []
        unknown = []
        while namestr:
            item = self._roster.longest_prefix(namestr)
            if not item:
                unknown.append(namestr[0])
                namestr = namestr[1:].lstrip()
            else:
                team.append(item.value)
                namestr = namestr[len(item.key):].lstrip()
        return team, ''.join(unknown)


roster = Roster()


def name2id(name):
    return roster.get_id(name)


def guess_id(name):
    """@return: id, name, score"""
    return roster.guess_id(name)


def id2name(id):
    return roster.get_true_name(id)


def list_to_string(chara):
    out = ""
    for x in chara:
        out += x + " "
    return out
