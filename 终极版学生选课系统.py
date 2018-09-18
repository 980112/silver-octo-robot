import time,sys
flag0 = 1
class Person:
    def __init__(self,name):
        self.name = name


class Course:
    def __init__(self,name,price,time,teacher):
        self.name = name
        self.price = price
        self.time = time
        self.teacher = teacher


class Student(Person):  # 学生类
    li = [('查看所有课程', 'check_Selectable_lesson'), ('选择课程', 'choose_lesson'),
          ('查看所选课程', 'check_selected_lesson'), ('退出程序', 'exit_program')]

    def check_Selectable_lesson(self):
        '''
        查看可以选择的课程
        :return:
        '''
        file_lesson = open('lesson_information','r',encoding='utf-8')
        print('\033[31m可选择的全部课程为\033[0m'.center(50, '='))
        for k, v in enumerate(file_lesson.readlines(), 1):
            lst = v.strip().split(',')
            print('\n', k, lst[0], lst[1], lst[2], lst[3])
        input('按下Enter回退上一级菜单!')

    def choose_lesson(self):
        '''
        开始选择课程
        选择完毕之后将选择的课程写入到文件
        :return:
        '''
        f = open('lesson_information', encoding='utf-8')
        lit = []
        print('\033[31m可选择的全部课程为\033[0m'.center(50, '='))
        for k, v in enumerate(f.readlines(), 1):
            lst = v.strip().split(',')
            lit.append(lst[0])
            print('\n',k,lst[0],lst[1],lst[2],lst[3])
        choice = int(input('输入课程编号来选择课程:'))
        file_stu = open('student_lesson','a',encoding='utf-8')
        file_stu.write('%s:%s\n' % (self.name,lit[choice-1]))
        input('选择成功,按下Enter回退上一级菜单!')

    def check_selected_lesson(self):
        '''
        查看已选择的课程和历史选择的课程
        :return:
        '''
        lesson = set()
        file_stu = open('student_lesson','r',encoding='utf-8')
        for line in file_stu:
            lesson_list = line.strip().split(':')
            if lesson_list[0] == self.name:
                lesson.add(lesson_list[1])
        if not lesson:
            print('\033[32m你当前为选择任何课程!\033[0m')
        else:
            print('你的姓名:%s\n当前你已选择的课程有:%s\n' % (self.name,tuple(lesson)))
        input('按下Enter回退上一级菜单!')

    def exit_program(self):
        print('\033[1;34m退出成功!\033[0m')
        global flag0
        flag0 = 0


class Manager(Person):    # 管理员类
    li = [('创建课程', 'create_lesson'), ('创建学生账号', 'create_student_account'),
          ('查看所有课程', 'check_all_lesson'), ('查看所有学生', 'check_all_student'),
          ('查看学生所选课程', 'check_all_student_lesson'), ('退出程序', 'exit_program')]
    @staticmethod
    def create_lesson():
        '''
        创建课程
        :return:
        '''
        while 1:
            lesson_name = input('请输入课程名称:')
            lesson_price = input('请输入课程价格:')
            lesson_time = input('请输入课程周期:')
            lesson_teacher = input('请输入任课教师:')
            file_less = open('lesson_information', 'a', encoding='utf-8')
            file_less.write(lesson_name + ',' + lesson_price + ',' + lesson_time + ',' + lesson_teacher + '\n')
            continue_or_not = input('\033[1;32m\n是否继续创建(输入n退出):\033[0m')
            if continue_or_not.upper() == 'N':
                break
        input('按下Enter回退上一级菜单!')
    @staticmethod
    def create_student_account():
        '''
        创建学生账号密码,且学生的账号密码只有此一种创建方式
        先输入要创建的学生账号,验证账号是否存在,如果存在,创建不成功,继续输入账号,如果不存在,继续输入密码和学生姓名
        :return:
        '''
        file_account = open('account_information', 'a', encoding='utf-8')
        while 1:
            student_account = input('请输入要创建的学生账号:')
            file_account.seek(0)
            for line in file_account:
                ift = line.strip().split(':')
                if student_account == ift[0]:
                    print('你输入的账号已存在,请重新输入')
                    break
            else:
                student_password = input('请输入要创建的学生密码:')
                student_name = input('请输入学生姓名')
                print('创建学生账号成功!')
                goon_or_not = input('\033[1;32m\n输入N停止创建,其他任意内容则继续创建:\033[0m')
                if goon_or_not.upper() == 'N':
                    break
        # 创建成功,将账号密码姓名写入文件
        file_account.write('%s:%s:Student:%s' % (student_account,student_password,student_name))
        file_account.flush()
        file_account.close()
        input('按下Enter回退上一级菜单!')

    @staticmethod
    def check_all_lesson():
        '''
        查看现在已有的可供学生选择的所有课程
        :return:
        '''
        file_check = open('lesson_information', 'r', encoding='utf-8')
        print('\033[31m可供学生选择的全部课程为\033[0m'.center(50, '='))
        for line in file_check:
            lesson_list = line.strip().split(',')
            print('\n课程名称:%s\t课程价格:%s\t课程周期:%s\t任课教师:%s' % \
                  (lesson_list[0], lesson_list[1], lesson_list[2], lesson_list[3]))

        input('按下Enter回退上一级菜单!')
    @staticmethod
    def check_all_student():
        '''
        查看现在已创建账户的学生信息
        :return:
        '''
        file_check = open('account_information', 'r', encoding='utf-8')
        print('\033[31m现在已创建账户的学生有\033[0m'.center(50, '='))
        for line in file_check:
            ift = line.strip().split(':')
            if ift[2] == 'Student':
                print('学生姓名:%s,学生账户:%s' % (ift[3],ift[0]))
        input('按下Enter回退上一级菜单!')

    @staticmethod
    def check_all_student_lesson():
        '''
        查看所有学生的选课情况,key为学生姓名,value为此学生所选择的全部课程
        :return:
        '''
        less = {}
        file_stu = open('student_lesson', 'r', encoding='utf-8')
        print('\033[31m已选课学生的选课情况\033[0m'.center(50, '='))
        for line in file_stu:
            name,course = line.strip().split(':')
            if name in less:
                less[name].add(course)
            else:
                lsn = set()
                lsn.add(course)
                less[name] = lsn
        for k,v in less.items():
            print('学生姓名:%s\t\t所选择的课程:%s\n' % (k,tuple(v)))
        input('按下Enter回退上一级菜单!')

    @staticmethod
    def exit_program():
        print('\033[1;34m退出成功!\033[0m')
        global flag0
        flag0 = 0

# 登录函数
def login():
    '''
    登录函数,验证账号密码,账号密码不与文件内容一致就重复登录,直到完全一致为止

    :return:
    '''
    while 1:
        username = input('请输入您的账号:').strip()
        password = input('请输入您的密码:').strip()
        f = open('account_information','r',encoding='utf-8')
        if username == '' or password == '':
            print('\033[1;32m账号或密码不能为空!\n\033[0m')
        else:
            for line in f:
                user,pwd,status,name = line.strip().split(':')
                if username == user and password == pwd:
                    print('\033[1;32m登录成功\033[0m')
                    f.close()
                    return {'username':name,'status':status}
            else:
                print('\033[1;32m你的账号或密码输入错误,请重新输入!\n\033[0m')

# 主程序入口
def main():
    print('\033[1;34m欢迎进入学生选课系统\033[0m'.center(50,'*'))
    ret = login()
    if ret:
        cls = getattr(sys.modules['__main__'], ret['status'])       # 得到类名
        obj = cls(ret['username'])     # 根据类名实例化对象
        while flag0:
            if ret['status'] == 'Student':
                print('\033[1;34m学生选课系统:学生端\033[0m'.center(50,'*')+'\n')
                print(('\033[1;34m当前登录用户:%s\033[0m' % obj.name).center(50))
            else:
                print('\033[1;34m学生选课系统:管理员端\033[0m'.center(50, '*')+'\n')
            for key,item in enumerate(cls.li,1):
                print(str(key).center(20),item[0])
            num = int(input('\n输入您要做的操作序号：'))
            if num <= len(cls.li):
                getattr(obj,cls.li[num-1][1])()
            else:
                print('\033[1;32m\n你的输入有误,请重新输入!\033[0m')
main()