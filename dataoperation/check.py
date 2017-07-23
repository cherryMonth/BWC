# coding=utf-8
import re


class Check(object):

    @staticmethod
    def format_check(data, _format=None):
        # 格式检查

        error = {}
        row = 1
        if not data:
            error['Format error '] = 'The external data is empty and cannot be imported!'
            return error
        for line in data:
            Check().re_line_check(line, row, error, _format)
            row = row + 1
        return error

    @staticmethod
    def get_primary_item(keys, line):
        key = reduce((lambda x, y: str(x) + ','+str(y)),
                     [line[key] for key in keys if line. has_key(key)], '')
        return key if key else None

    @staticmethod
    def del_repeat(out_data, in_data=None, keys=None, _type='w'):
        #   可以自我去重 也可以指定外部数据后覆盖掉内部的数据或追加或删除到内部数据 可以指定主键充当判断准则
        if Check.get_result(Check.format_check(out_data)):
            return []
        if not keys:
            keys = in_data[0].keys() if in_data else out_data[0].keys()

        for line in out_data:
            key1 = Check().get_primary_item(keys, line)
            record = {}
            for index in in_data:
                key2 = Check().get_primary_item(keys, index)
                if not record. has_key(key2):
                    record[key2] = 1
                if key1 and key1 == key2:
                    if _type != 'w' or not record[key2]:
                        in_data.remove(index)
                    elif record[key2]:
                        in_data[in_data.index(index)] = line
                        record[key2] = 0
                elif not key1 or not key2:
                    print 'The external data is different from the internal data key ！'
                    return []
            if _type == 'w' and record.get(key1, 1):
                in_data.append(line)
        return in_data

    @staticmethod
    def re_line_check(line, row, error, _format=None):
        # 利用正则表达式对数据进行检查
        if not line or type(error) != dict:
            error['Format error row (%d) '] = 'The data is empty or the data structure is not a dictionary！'
            return True

        if not _format:
            for (key, item) in line.items():
                if not item:
                    error['Error line row [' + str(row) + ']'] = 'Datakey '+key + ': value does not exist!'
            return Check.get_result(error)

        for (key, item) in _format.items():
            if not line. has_key(key):
                error['Error line row [' + str(row) + ']'] = 'Data ' + key + ' The key or value does not exist!'
            else:
                if line[key] and re.findall(item, line[key]):
                    pass
                else:
                    error['Error line row ['+str(row)+']'] = 'The line information does not conform to the standard!'

        return Check.get_result(error)

    @staticmethod
    def get_result(dictionary):
        # 判断一个字典是否为空
        if type(dictionary) is not dict:
            return True
        for (key, item) in dictionary.items():
            if item:
                return True
        return False

