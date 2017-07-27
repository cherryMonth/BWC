#coding=utf-8
import csv


class Read(object):

    @staticmethod
    def read(filename, key_list=None):
        # 信息通配符 一次只能接受一个原子字典
        if key_list and type(key_list) != dict:
            return []
        try:
            with open(filename, "rb") as csv_file:
                reader = csv.DictReader(csv_file)
                data = []
                for info in reader:
                    if not key_list:
                        data.append(info)
                    else:
                        count = 0
                        for (_key, item) in key_list.items():
                            if item == '*':
                                continue
                            elif item == '?':
                                count = 2
                            elif not info. has_key(_key) or info[_key] != item:
                                count = 1
                                break
                        if count % 2 == 0:
                            data.append(info)
                        if count == 2:
                            break
                csv_file.close()
                return data

        except IOError:
            return []

if __name__ == '__main__':
    _list = Read().read('xxx',{'TeacherIDx':'200463xx3'})
    _list2 = Read().read('zxczc')
    print _list
