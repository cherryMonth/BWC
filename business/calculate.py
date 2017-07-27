# coding=utf-8
from dataoperation.manage import DataManage
'''
此模块对　出勤情况历史统计　出勤成绩输出　出勤情况随堂（实时）统计　　请假认定 考勤规则的指定
'''


class AuxiliaryFunction(object):

    @staticmethod
    def __calculation(absence):  # 子计算
        absence_num = 0  # 缺勤人数
        sub_num = 0  # 请假提交人数
        app_num = 0  # 请假批准人数
        late_num = 0  # 迟到人数
        early_num = 0  # 早退人数
        normal = 0  # 正常人数
        all_info = {}
        length = len(absence.keys())
        for (key, item) in absence.items():
            if item['Type'] == 'Late':
                late_num = late_num + 1
            elif item['Type'] == 'Submitted':
                sub_num = sub_num + 1
            elif item['Type'] == 'Absence':
                absence_num = absence_num + 1
            elif item['Type'] == 'normal':
                normal = normal + 1
            elif item['Type'] == 'leaveEarlier':
                early_num = early_num + 1
            elif item['Type'] == 'approve':
                app_num = app_num + 1

            if item['Type'] != 'normal':
                all_info[key] = item

        grade = 1.0 * normal / length * 100
        info = dict()
        info['checkin'] = all_info
        info['latenum'] = late_num
        info['approve'] = app_num
        info['subnum'] = sub_num
        info['length'] = length
        info['leaveEarlier'] = early_num
        info['normal'] = normal
        info['absence'] = absence_num
        info['grade'] = grade
        return info

    def statistics_calculation(self, stu_info_list, _type=''):  # 给定一定数量的学生考勤信息计算该信息内所有学生的考勤结果
        absence = {}
        keys = {'null': 0, 'normal': 1, 'Late': 2, 'leaveEarlier': 3, 'Absence': 4, 'Submitted': 5, 'approve': 6}

        for stu in stu_info_list:
            info = {}
            if absence. has_key(stu['StuID']):
                continue
            else:
                absence[stu['StuID']] = info
            info['Type'] = 'null'
            info['StuName'] = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv',
                                                                       {'StuID': stu['StuID']})).run()[0]['StuName']
        if not _type:
            _type = 'checkinResult'

        for stu in stu_info_list:
            info = absence[stu['StuID']]
            if keys[info['Type']] < keys[stu[_type]]:
                if info['Type'] == 'null':
                    info['Type'] = stu[_type]
                elif info['Type'] == 'normal' or info['Type'] == 'Late':
                    if stu[_type] == 'Absence':
                        info['Type'] = 'leaveEarlier'
                    else:
                        info['Type'] = stu[_type]
                elif info['Type'] == 'leaveEarlier' or info['Type'] == 'Absence':
                    if keys[stu[_type]] >= 5:
                        info['Type'] = stu[_type]
                    else:
                        continue
                else:
                    info['Type'] = stu[_type]
            else:
                if info['Type'] == 'Absence':
                    if stu[_type] == 'normal' or stu[_type] == 'Late':
                        info['Type'] = 'Late'
                continue

        return self.__calculation(absence)

    def dis_play(self, stu_info_list,_type=''):  # 自带格式化并显示考勤结果到终端
        check_info = self.statistics_calculation(stu_info_list,_type)
        if not check_info:
            print '数据不合法无法进行计算!'
            return False

        print '最近一节课的出勤状况如下 :'
        print '考勤总人数:%d 正常考勤人数:%d 缺勤人数:%d 请假人数:%d 迟到人数:%d 早退人数:%d 出勤率%.2f %% ' % (
            check_info['length'], check_info['normal'], check_info['absence'],
            check_info['subnum'] + check_info['approve'], check_info['latenum'], check_info['leaveEarlier'],
            check_info['grade'])

        if int(check_info['grade']) != 100:
            print '未出勤学生详细信息如下:'
            for (key, item) in check_info['checkin'].items():
                print '学号 :%-15s 姓名 :%-15s 考勤状况 :%-12s ' % (key, item['StuName'], item['Type'])
        return True

