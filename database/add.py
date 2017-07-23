# coding=utf-8
import csv
import os
import collections


class Add(object):

    @staticmethod
    def add(filename, key_list=None):

        if not os.path.exists(filename):
            index = 1
        else:
            index = 0
        try:
            with open(filename, 'ab') as csv_file:

                if not key_list:
                    csv_file.close()
                    return True

                def num(string):
                    count = 0
                    for n in string:
                        count = count + ord(n)
                    return count

                error = []

                for key in key_list:
                    d = collections.OrderedDict()
                    key = sorted(key.items(), key=lambda x: num(x[0]))
                    for k in key:
                        d[k[0]] = k[1]
                    error.append(d)

                key_list = error
                row_name = key_list[0].keys()  # 类变量记录列名
                writer = csv.DictWriter(csv_file, fieldnames=row_name)
                if index == 1:
                    writer.writerow(dict(zip(row_name, row_name)))  # 写表头
                for key in key_list:
                    writer.writerow(key)    # 写数据
                csv_file.close()
                return True

        except IOError:
            print "File open error : " + filename + "\nplease check the filename"
            return False

