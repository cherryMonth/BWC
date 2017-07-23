# coding=utf-8
import time
import copy
from checkinnode import CheckInNode
from basebusiness import BaseBusiness
from dataoperation.manage import DataManage
from stufunction import StudentFun
from maintain import Maintain
from view import View
from importfile import ImportFile


class Business(BaseBusiness):

    def __init__(self):
        BaseBusiness.__init__(self)

        self.stufunct = StudentFun()

        self.maintain = Maintain()

        self.view = View()

        self.import_file = ImportFile()

    @staticmethod
    def stu_info_test(key):

        stu_info = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv', {'WeChatID': key})).run()
        if not stu_info:
            print '学生微信不存在请检查您的输入信息!'
            return False
        return stu_info[0]

    @staticmethod
    def teacher_test(key):  # 输入微信号和班级　进行验证
        teacher_info = DataManage(DataManage.target_info, args=('../InData/teacherInfo.csv', {'WeChatID': key})).run()

        key = {}
        if not teacher_info:
            print '教师微信不存在请检查您的输入信息!'
            return False
        key['TeacherID'] = teacher_info[0]['TeacherID']
        key['teacher_info'] = teacher_info[0]
        info_list = DataManage(DataManage.target_info, args=('../InData/courseInfo.csv',
                                                             {'TeacherID': key['teacher_info']['TeacherID']})).run()

        key['course_info'] = {}
        for info in info_list:
            if not key['course_info']. has_key(info['CourseID']):
                key['course_info'][info['CourseID']] = {}
                key['course_info'][info['CourseID']]['CourseName'] = info['CourseName']
                key['course_info'][info['CourseID']]['ClassInfo'] = set()
                key['course_info'][info['CourseID']]['ClassInfo'].add(info['ClassName'])
            for (k, item) in key['course_info'].items():
                if k == info['CourseID']:
                    item['ClassInfo'].add(info['ClassName'])
        return key

    def insert_leave(self, key):
        key = copy.deepcopy(key)
        for line in self.list:
            if key['ClassID'] in list(line.key['ClassList']):
                key['CourseID'] = line['CourseID']
                key['TeacherID'] = line['TeacherID']
                return self.stufunct.insert_leave_record(key)
        return False

    def auto_check_in(self, key):
        for line in self.list:
            if key['ClassID'] in list(line.key['ClassList']):
                return line.receive(key)
        return False

    def tips(self, key, info=''):
        count = 0
        for line in self.list:
            if key['ClassID'] in list(line.key['ClassList']):  # 1
                if info:
                    print '当前工号为:%s 的老师正在向您的班级发起自动考勤!' %(line.key['TeacherID'], )
                count += 1
                if not line.random_info:
                    return count
                for _info in line.random_info:
                    if _info['StuID'] == key['StuID']:  # 2
                        if info:
                            print '当前存在和您有关的抽点考勤!'
                        count += 2
        return count

    def start_random(self, key):
        for line in self.list:
            if line.key['TeacherID'] == key['teacher_info']['TeacherID']:
                return line.start_random()
        print '当前您没有开启一个自动考勤窗口无法开启随机考勤!'
        return False

    def dis_info(self,key):
        for line in self.list:
            if key['TeacherID'] == line.key['TeacherID']:  # 1
                print '您当前正在对课程%s进行考勤 ' % (line.key['course_info'][line.key['CourseID']]['CourseName'])
                if not line.random_info:
                    return True
                print '当前存在您开启的抽点考勤!'
                return True
        print '您的课头列表信息如下: '
        for (k, item) in key['course_info'].items():
            print '课程ID %s 课程名 %s,有关班级如下 :' % (k,item['CourseName'])
            for _class in item['ClassInfo']:
                print _class
        return False

    @staticmethod
    def __time_check(check_node):  # 判断是否下课
        localtime = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        if localtime > check_node.end_time:
            return False
        return True

    def start_check_in(self, key):  # 教师ID　课程ID　学生班级集合
        key = copy.deepcopy(key)
        if key['CourseID'] not in key['course_info'].keys():
            print '课程不在您的课头列表之中,请检查您的输入信息后重试!'
            return False

        info = dict()
        info = key
        info['TeacherID'] = key['teacher_info']['TeacherID']
        info['CourseID'] = key['CourseID']
        info['ClassList'] = key['course_info'][key['CourseID']]['ClassInfo']
        c = CheckInNode(info)

        for index in self.list:
            if index.key['TeacherID'] == key['teacher_info']['TeacherID']:
                if self.__time_check(index):
                    print '您已经对课程:%s开启自动考勤无法再次开启' % (index.key['CourseID'])
                    return False
                else:
                    if self.list.index(index) == 0:
                        self.stop_check_in()
                    else:
                        self.list.remove(index)

        for index in self.list:
            intersect = index.key['ClassList'] & info['ClassID']
            if intersect:
                if self.__time_check(index):
                    print '以下班级正在被老师:%s考勤,无法对此班级发起考勤!' % (index.key['TeacherID'])
                    for line in list(intersect):
                        print line
                    return False
                else:
                    if self.list.index(index) == 0:
                        self.stop_check_in()
                    else:
                        self.list.remove(index)

        if not c.start_auto():
            return False

        if not self.list:
            self.list.append(c)
            self.start_check_time()
        else:
            self.list.append(c)

        print '发起考勤成功!'
        return True

    def random_check_in(self, key):
        for line in self.list:
            if key['ClassID'] in list(line.key['ClassList']):
                for info in line.random_info:
                    if info['StuID'] == key['StuID']:
                        return line.receive(key)
        print '没有与您有关的随机考勤窗口!'
        return False

    def man_check_in(self, key):
        if self.can_statistics(key):
            return CheckInNode(key).man_check_in()

    def can_statistics(self,key):
        for line in self.list:
            if line.key['TeacherID'] == key['teacher_info']['TeacherID']:
                print '当前您开启了对课程%s的考勤，无法开启统计功能!' % (line.key['CourseID'], )
                return False
        return True

