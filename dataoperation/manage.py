# coding=utf-8
from query import Query
from update import Update
from check import Check


class DataManage(object):

    target_key = 1
    target_info = 2
    find_file = 3
    format_check = 4
    update = 5
    get_result = 6

    def __init__(self, target=None, args=()):
        self.target = target
        self.args = args

    def run(self):
        if self.target == 1:
            return Query.query_target_keys(*self.args)
        elif self.target == 2:
            return Query.query_target_info(*self.args)
        elif self.target == 3:
            return Query.query_file_names(*self.args)
        elif self.target == 4:
            return Check.format_check(*self.args)
        elif self.target == 5:
            return Update.update(*self.args)
        elif self.target == 6:
            return Check.get_result(*self.args)
        else:
            print '类型错误无该函数调用!'
            return None


if __name__ == '__main__':
    print DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()