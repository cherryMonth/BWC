# coding=utf-8
import datetime


class Log(object):

    @staticmethod
    def add(info):
        _file = open('../InData/log.log','a')
        _file.write('Time : '+str(datetime.datetime.now())[:-7]+'\n')
        for (key, item) in info.items():
            _file.write(key+' : '+item+' \n')
