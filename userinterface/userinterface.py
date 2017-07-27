# coding=utf-8
import sys
from business.businessapi import Business


class SystemRun(object):

    @staticmethod
    def stu_form(key, line):
        while True:
            print "*************欢迎进入学生模拟控制菜单******************"
            print "*****************1.在线请假*************************"
            print "*****************2.进行考勤*************************"
            print "*****************3.进行抽点考勤**********************"
            print "*****************4.查看当前考勤结果*******************"
            print "*****************5.查看历史考勤结果*******************"
            print "*****************6.回到上级目录**********************"
            line.tips(key, 'info')
            op_num = raw_input("请输入您想要的操作：")
            if op_num == '1':
                if line.tips(key) < 1:
                    print '当前没有与您有关的自动考勤窗口被发起,无法请假!'
                    continue
                key['ProofPath'] = raw_input("请输入您的请假证据：（学生）")
                line.insert_leave(key)

            elif op_num == '2':  # 在线考勤
                if line.tips(key) < 1:
                    print '当前没有与您有关的自动考勤窗口被发起!'
                    continue
                key['ProofPath'] = raw_input("请输入您的考勤证据路径：（学生）")
                key['Type'] = 'auto'
                line.auto_check_in(key)

            elif op_num == '3':
                if line.tips(key) != 3:
                    print '当前没有与您有关的随机考勤窗口被发起!'
                    continue
                key['ProofPath'] = raw_input("请输入您的考勤证据路径：（学生）")
                key['Type'] = 'random'
                line.random_check_in(key)

            elif op_num == '4':
                line.stufunct.real_view(key)

            elif op_num == '5':
                line.stufunct.history(key)

            elif op_num == '6':  # 回到主菜单
                break

            else:
                print "输入有误 没有对应输入的选项！"

    @staticmethod
    def att_output(key, line):

        while True:
            print "*************欢迎进入考勤成绩统计菜单*********************"
            print "*****************1.查看某次课程的出勤率******************"
            print "*****************2.查看某课程汇总出勤信息*****************"
            print "*****************3.显示用户总考勤概要信息****************"
            print "*****************4.显示用户总考勤详细信息****************"
            print "*****************5.回到上级目录************************"
            op_num = raw_input("请输入您想要的操作：")
            if op_num == '1':
                key['CourseID'] = raw_input("请输入课程ID")
                num = raw_input('请输入查看课程的次序号')
                line.view.get_count_rate(key, num)

            elif op_num == '2':  # 在线考勤
                key['CourseID'] = raw_input("请输入课程ID")
                line.view.get_all_rate(key)

            elif op_num == '3':
                line.view.dis_summary_sum(key)
            elif op_num == '4':
                line.view.dis_all_sum(key)
            elif op_num == '5':  # 回到主菜单
                break
            else:
                print "输入有误 没有对应输入的选项！"

    def teacher_form(self, key, line):
        while True:
            print "*************欢迎进入教师模拟控制菜单******************"
            print "*****************1.开启自动考勤************************"
            print "*****************2.开启抽点考勤************************"
            print "*****************3.开始手动考勤************************"
            print "*****************4.设置考勤缓冲时间********************"
            print "*****************5.出勤情况随堂（实时）统计************"
            print "*****************6.生成出勤状况统计表******************"
            print "*****************7.出勤成绩统计汇总输出****************"
            print "*****************8.学生信息维护************************"
            print "*****************9.考勤信息维护************************"
            print "****************10.回到上级目录************************"
            line.dis_info(key)
            op_num = raw_input("请输入您想要的操作：")
            if op_num == '1':
                key['CourseID'] = raw_input('请输入您要考勤的课程ID!')
                if not line.start_check_in(key):
                    print '开启考勤失败!'

            elif op_num == '2':  # 在线考勤
                line.start_random(key)

            elif op_num == '3':
                course_id = raw_input('请输入您要考勤的课程ID!')
                key['CourseID'] = course_id
                if not line.man_check_in(key):
                    print '开启考勤失败!'

            elif op_num == '4':
                line.maintain.rule_set(key)

            elif op_num == '5':
                line.view.view_time(key)

            elif op_num == '6':  # 回到主菜单
                if line.can_statistics(key):
                    key['CourseID'] = raw_input('请输入需要计算的课程ID')
                    key['SeqNum'] = raw_input('请输入考勤次序号')
                    line.view.create_sum(key)

            elif op_num == '7':
                self.att_output(key, line)

            elif op_num == '8':
                line.maintain.maintain_stu(key)

            elif op_num == '9':  # 回到主菜单
                key['CourseID'] = raw_input('请输入需要维护的课程ID')
                line.maintain.maintain_info(key)

            elif op_num == '10':
                break
            else:
                print "输入有误 没有对应输入的选项！"

    @staticmethod
    def admin_form(line):
        while True:
            print "*************欢迎进入管理员模拟控制菜单***************"
            print "******************1.教师信息导入**********************"
            print "******************2.学生信息导入**********************"
            print "******************3.课程信息导入**********************"
            print "******************4.返回上一层************************"
            op_num = raw_input("请输入您想要的操作：")

            if op_num in ['1', '2', '3', '4']:
                outfile = raw_input('请输入导入外部文件路径 :')
                if op_num == '1':
                    if line.import_file.import_teacher(outfile):
                        print '导入教师信息成功!'
                elif op_num == '2':
                    if line.import_file.import_stu(outfile):
                        print '导入学生信息成功!'
                elif op_num == '3':
                    if line.import_file.import_class(outfile):
                        print '导入课程信息成功!'
                else:
                    break
            else:
                print '错误输入,没有对应输入的选项!'

    def form(self):
        business = Business()
        while True:
            print "****************欢迎进入模拟控制菜单****************"
            print "*****************1.教师登录*************************"
            print "*****************2.学生登录*************************"
            print "*****************3.管理员登录***********************"
            print "*****************4.退出程序*************************"
            op_num = raw_input("请输入您想要的操作：")
            if op_num == '1':  # 教师开启考勤
                teacher_we_chat_id = raw_input("请输入您的微信号：（教师）")
                key = business.teacher_test(teacher_we_chat_id)
                if key:
                    self.teacher_form(key, business)
                else:
                    continue

            elif op_num == '2':  # 学生正常考勤操作
                stu_we_chat_id = raw_input("请输入您的微信号：（学生）")
                key = business.stu_info_test(stu_we_chat_id)
                if key:
                    self.stu_form(key, business)
                else:
                    continue

            elif op_num == '3':  #
                self.admin_form(business)

            elif op_num == '4':  # 退出系统
                sys.exit(0)
            else:
                print "输入有误 没有对应输入的选项！"

if __name__ == "__main__":

    SystemRun().form()