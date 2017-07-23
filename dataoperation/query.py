# coding=utf-8
import os
import re

from database.database import DataAPI


class Query(object):

    # 查询目标信息通过不同的参数达到查询不同的效果

    @staticmethod
    def query_target_keys(obj):
        # 返回目标的键 也可查询含有合法信息的文件是否存在 若不存在则返回None
        pattern = re.compile(r'.+\.csv$', re.I)
        if not pattern.match(obj):
            return []
        elif DataAPI(obj, 'r').run():
            return sorted(DataAPI(obj, 'r').run()[0].keys())
        return []

    @staticmethod
    def query_target_info(filename="", parameter=None):

        # 给定字典查询指定文件中满足字典的信息 可以使用通配符
        if Query.query_target_keys(filename):
            return DataAPI(filename, 'r', parameter).run()

        elif not filename:
            data = []
            file_list = Query.query_file_names(Query.query_target_keys)
            for line in file_list:
                info = DataAPI(line, 'r', parameter).run()
                if info and parameter:
                    data.append(info)
            return data

        else:
            return []

    @staticmethod
    def query_file_names(operation):

        #   查找符合对应函数的信息的文件名
        file_list = []
        for f_path, dirs, fs in os.walk('..'):
            for f in fs:
                file_list.append(os.path.join(f_path, f))
        data = []
        for line in file_list:
            if operation and operation(line):
                data.append(line)
        return data


