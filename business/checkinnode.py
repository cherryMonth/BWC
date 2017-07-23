# coding=utf-8
from bashcheckin import BashCheckIn
from dataoperation.manage import DataManage


class CheckInNode(BashCheckIn):

    def start_auto(self):
        if self.status:
            print ' 当前已经存在自动考勤窗口无法再次开启!'
            return False

        if not self.get_time():
            return False

        stu_list = []
        for _class in list(self.key['ClassList']):
            student = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv', {'ClassID': _class})).run()
            for stu in student:
                stu_list.append(stu)

        self.write_seq()
        stu_list = self.init_data(stu_list, 'auto')
        self.status = True
        return DataManage(DataManage.update, args=(self.filename, 'w', stu_list)).run()

    def start_random(self):
        if not self.status:
            print ' 当前没有开启自动考勤无法进行抽点考勤!'
            return False
        self.random_info = self.random_stu_list()
        if not self.random_info:
            return False
        stu_list = self.init_data(self.random_info, 'random')
        return DataManage(DataManage.update, args=(self.filename, 'a', stu_list)).run()

    def receive(self, stu_info):
        if stu_info['Type'] == 'auto':
            return self.auto_cal(stu_info)
        else:
            return self.random_cal(stu_info)

    def man_check_in(self):  # 手动考勤

        course_info = DataManage(DataManage.target_info,
                                 args=('../InData/courseInfo.csv', {'CourseID': self.key['CourseID'],
                                                                    'TeacherID': self.key['TeacherID']})).run()

        if not course_info:
            print '当前没有与您相关的课程!'
            return False

        class_list = []

        for course in course_info:
            if course['ClassName'] not in class_list:
                class_list.append(course['ClassName'])

        stu_list = []
        for _class in class_list:
            student = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv', {'ClassID': _class})).run()
            for stu in student:
                stu_list.append(stu)

        self.write_seq()
        print '请按照以下选项输入状态 非法输入默认为缺勤!'
        print ' 1　正常　2　迟到　３　早退　４　缺勤 5　请假已批准'
        stu_list = self.init_data(stu_list, 'man')
        print '学生考勤状态手动设置完成!'
        return DataManage(DataManage.update, args=(self.filename, 'w', stu_list)).run()