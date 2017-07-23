# coding=utf-8
from database.database import DataAPI
from check import Check
from query import Query


class Update(object):

    @staticmethod
    def update(filename, _type, out_data, keys=None):
        # 更新数据 可以覆盖 添加 和追加到文件末尾  外部数据必须是以列表为容器　元素是字典
        error = Check.format_check(out_data)
        if Check.get_result(error):
            print error
            return False

        if _type == 'w' or _type == 'dl':
            data = Query.query_target_info(filename, None)
            data = Check.del_repeat(out_data, data, keys, _type)
            return DataAPI(filename, 'w', data).run()

        elif _type == 'a':
            return DataAPI(filename, 'a', out_data).run()

        else:
            print 'invalid parameter : %s' % (_type,)
            return False


