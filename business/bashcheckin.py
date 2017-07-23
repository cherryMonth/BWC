# coding=utf-8
import datetime
import ConfigParser
import re
from maintain import Maintain
from dataoperation.manage import DataManage
import random
import time


class BashCheckIn(object):

    def __init__(self, key):
        self.counter = {'auto': {}, 'random': {}}
        self.status = False
        self.random_info = []
        self.time = int(Maintain().read_rule(key)['bufferTime']) * 60
        self.start_time = None
        self.start = datetime.datetime.now()
        self.end_time = None
        self.key = key  # 包含该课的老师ID　课程ID　以及班级集合
        self.filename = None
        cf = ConfigParser.ConfigParser()
        cf.read('../InData/settings.ini')
        info = map((lambda x: re.split('-|:', x[1])), cf.items('sectime'))
        self.Time_info = map((lambda x: [int(x[0]) * 3600 + int(x[1]) * 60, int(x[2]) * 3600 + int(x[3]) * 60]), info)

    def get_time(self):
        localtime = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        for Time in self.Time_info:
            if localtime >= Time[0] - self.time:
                if localtime <= Time[1] - self.time:
                    self.end_time = Time[1]
                    self.start_time = localtime
                    self.status = True
                    return True
            elif localtime < Time[0] - self.time:
                if localtime >= Time[0] - 600:
                    print '据可开始考勤的时间还有%d秒,你可设置考勤缓冲提前开始考勤!' % (Time[0] - self.time - localtime)
                    return False
            elif localtime < Time[1] - 60:
                if localtime > Time[1] - self.time:
                    print '您已超过考勤缓冲有效范围%d秒,学生所需的上传信息时间不足所以无法开启,' \
                          '你可设置考勤缓冲调整此时间!' % (localtime - Time[1] + self.time)
                    return False

        status = raw_input(" 当前不是开启考勤的有效时间,您是否开启窗口? yes or other ")
        if status == 'yes':
            self.status = True
            self.start_time = localtime
            self.end_time = localtime+6000
            return True
        else:
            print '当前不是有效时间,开启考勤失败!'
            return False

    def init_data(self, stu_info_list, _type):
        # 格式化初始数据

        info = []
        for line in stu_info_list:
            data = {}
            if _type != 'man':
                self.counter[_type][line['StuID']] = 5
            data['StuID'] = line['StuID']
            data['checkTime'] = 'null'
            data['ProofPath'] = 'null'
            data['checkinType'] = _type
            data['IsSucc'] = 'False'
            if _type == 'man':
                sel=raw_input('当前学生学号:'+data['StuID']+' 请输入您的选项!')
                keys = {'1': 'normal', '2': 'Late', '3': 'leaveEarlier', '4': 'Absence', '5': 'approve'}
                if sel in list('12345'):
                    data['checkinResult'] = keys[sel]
                else:
                    print '您输入了非法选项默认该学生为缺勤!'
                    data['checkinResult'] = keys['4']
                print '学号为 : %s 的考勤状态设定完毕 为 :%s' % (data['StuID'], data['checkinResult'])
            else:
                data['checkinResult'] = 'Absence'
            info.append(data)
        return info

    def get_seq_num(self):
        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',
                                                            {'TeacherID': self.key['teacher_info']['TeacherID'],
                                                             'CourseID': self.key['CourseID']})).run()
        if not seq_info:
            return '1'
        return str(int(seq_info[-1]['SeqID'])+1)

    def get_seq_info(self):
        seq_info = {'TeacherID': self.key['TeacherID'], 'CourseID': self.key['CourseID']}
        seq_num = self.get_seq_num()
        self.filename = '../InData/'+self.key['TeacherID'] + '_' + self.key['CourseID'] + '_' + seq_num + '_Detail.csv'
        seq_info['StartTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seq_info['SeqID'] = self.get_seq_num()
        return seq_info

    def write_seq(self):
        if not DataManage(DataManage.target_key, args=('../InData/seq.csv',)).run():
            print 'The system creates the seq.csv file automatically！'
        return DataManage(DataManage.update, args=('../InData/seq.csv', 'a', [self.get_seq_info()])).run()

    def random_stu_list(self):

        now = datetime.datetime.now()
        if (now - self.start).seconds < self.time:
            print '当前自动考勤的仍然存在缓冲时间无法开启随机窗口,您可修改缓冲时间改变此设置!'
            return False

        stu_list = set()
        for _class in list(self.key['ClassList']):
            student = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv', {'ClassID': _class})).run()
            for stu in student:
                stu_list.add(stu)

        stu_list = list(stu_list)

        while True:
            num = raw_input('请输入需要抽点的百分比!')
            try:
                num = float(num)
            except TypeError and ValueError:
                print '您的输入不符合规则,请重新输入!'
                continue

            if num <= 0 or num > 100 or int(len(stu_list) * num / 100) == 0:
                print '抽点的数量大于或小于当前学生的数量请重新输入!'
                time.sleep(1)
            else:
                num = int(len(stu_list) * num / 100)
                print '抽点完成您此时共抽点了%-3d名学生!' % ( num,)
                break

        stu = []
        while len(stu) != num:
            index = random.randint(0, len(stu_list)-1)
            if stu_list[index] not in stu:
                stu.append(stu_list[index])
        return stu

    def auto_cal(self, stu_info):
        if DataManage(DataManage.target_info, args=(self.filename, {'StuID': stu_info['StuID'],
                                                                    'checkinType': 'leave'})).run():
            print '您在该次考勤中已经申请过请假无法进行考勤!'
            return False

        if self.counter['auto'][stu_info['StuID']] == 0:
            print '您当前进行自动考勤次数已经用完无法考勤!'
            return False

        self.counter['auto'][stu_info['StuID']] -= 1
        data = DataManage(DataManage.target_info, args=(self.filename, {'checkinType': 'auto',
                                                                        'StuID': stu_info['StuID']})).run()[0]

        if data['IsSucc'] == 'True':
            print '您已经完成自动考勤无法再次考勤!'
            return False

        data['checkTime'] = datetime.datetime.now()
        data['ProofPath'] = stu_info['ProofPath']
        num = random.randint(0, 1)
        if num:
            data['IsSucc'] = 'True'
            seconds = (data['checkTime'] - self.start).seconds
            if seconds <= self.time:
                print '考勤成功!'
                data['checkinResult'] = 'normal'
            else:
                print '考勤有效时间已过您当前为迟到!'
                data['checkinResult'] = 'Late'
        else:
            print '身份验证失败！ 您还有 %d 次机会 ' % (self.counter['auto'][stu_info['StuID']])
        data['checkTime'] = str(datetime.datetime.now())[:-7]
        return DataManage(DataManage.update, args=(self.filename, 'w', [data], ['StuID', 'checkinType'])).run()

    def random_cal(self, stu_info):

        if DataManage(DataManage.target_info, args=(self.filename, {'StuID': stu_info['StuID'],
                                                                    'checkinType': 'leave'})).run():
            print '您在该次考勤中已经申请过请假无法进行考勤!'
            return False

        if self.counter['random'][stu_info['StuID']] == 0:
            print '您当前进行随机考勤次数已经用完无法考勤!'
            return False

        data = DataManage(DataManage.target_info, args=(self.filename,
                                                        {'checkinType': 'random', 'StuID': stu_info['StuID']})).run()

        self.counter['random'][stu_info['StuID']] -= 1

        if data[-1]['IsSucc'] == 'True':
            print '您已经完成随机考勤无法再次考勤'
            return False

        DataManage(DataManage.update, args=(self.filename, 'dl', data, ['StuID', 'checkinType'])).run()
        data[-1]['ProofPath'] = stu_info['ProofPath']
        num = random.randint(0, 1)
        if num:
            data[-1]['IsSucc'] = 'True'
            print '随机考勤成功!'
            data[-1]['checkinResult'] = 'normal'
        else:
            print '身份验证失败！ 您还有 %d 次机会 ' % (self.counter['random'][stu_info['StuID']])
        data[-1]['checkTime'] = str(datetime.datetime.now())[:-7]
        return DataManage(DataManage.update, args=(self.filename, 'a', data)).run()
