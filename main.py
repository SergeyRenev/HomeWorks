class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        courses_in_progress = ""  # курсы в процессе
        for cours_in_prog in self.courses_in_progress:
            courses_in_progress += cours_in_prog + ' '
        finished_courses = ""  # законченные курсы
        for finish_in_cour in self.finished_courses:
            finished_courses += finish_in_cour + ' '

        mid_grade = 0.
        if len(self.grades) > 0:
            com = 0. # общая сумма
            col = 0  # количество оценок
            for vals in self.grades.values():
                com += sum(vals)
                col += len(vals)
            mid_grade = com / col  # средняя оценка

        return 'Имя: ' + self.name + '\n' + 'Фамилия: ' + self.surname + '\n' + \
               'Средняя оценка за домашние задания: ' + str(mid_grade) + '\n' + \
               'Курсы в процессе изучения: ' + courses_in_progress + '\n' + \
               'Завершенные курсы: ' + finished_courses

#оценки лекторам от студентов
    def add_grade_Lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and (course in self.courses_in_progress or course in self.finished_courses):

            if course in lecturer.grades_lect.items(): # смотрим, есть ли лектор в списке оценок
                lecturer.grades_lect[course] += [grade]
            elif course in lecturer.courses_attached: # проверяем, закреплен ли лектор за данным курсом студента
                lecturer.grades_lect[course] = [grade]
            else:
                return 'Ошибка'



class Mentor:
    def __init__(self, name, surname, courses_attached):
        self.name = name
        self.surname = surname
        self.courses_attached = courses_attached



class Lecturer(Mentor): #имя, фамилия и список закрепленных курсов наследуем от Mentor

    grades_lect = {} #атрибут-словарь где хранятся оценки (ключи – названия курсов, а значения – списки оценок)

    def __str__(self):
        mid_grade = 0.
        if len(self.grades_lect) > 0:
            com = 0. # общая сумма
            col = 0  # количество оценок
            for vals in self.grades_lect.values():
                com += sum(vals)
                col += len(vals)
            mid_grade = com / col  # средняя оценка
        return 'Имя: ' + self.name + '\n' + 'Фамилия: ' + self.surname + '\n' + \
               'Средняя оценка за лекции: ' + str(mid_grade)



class Reviewer(Mentor): # имя, фамилия и список закрепленных курсов наследуем от Mentor

    def __str__(self):
        return 'Имя: ' + self.name + '\n' + 'Фамилия: ' + self.surname

    def rate_hw(self, student, course, grade): # оценки за домашнюю работу
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'



# подсчет средней оценки за домашние задания по всем студентам в рамках конкретного курса
def GetMidGradeAllStudents(students, course):
    com = 0.  # общая сумма
    col = 0  # количество оценок
    for student in students:
        if student.grades.get(course,None):
            for vals in student.grades.values():
                com += sum(vals)
                col += len(vals)
    return com / col  # средняя оценка

# подсчет средней оценки за лекции всех лекторов в рамках курса
def GetMidGradeAllLecturers(lecturers, course):
    com = 0.  # общая сумма
    col = 0  # количество оценок
    for lecturer in lecturers:
        if lecturer.grades_lect.get(course,None):
            for vals in lecturer.grades_lect.values():
                com += sum(vals)
                col += len(vals)
    return com / col  # средняя оценка



student1 = Student('Сергей','Ренев','м')
student2 = Student('Ирина','Ренева','ж')

# завершенные курсы
student1.finished_courses = ['Физика','Химия']
student2.finished_courses = ['Биология','География']

# курсы в процессе изучения
student1.courses_in_progress = ['Математика','Физика']
student2.courses_in_progress.append('Физика')

# mentor1 = Mentor('Илья','Петров',[])
# mentor2 = Mentor('Николай','Иванов',[])

lecturer1 = Lecturer('Вова','Сидоров',['Математика','Физика'])
lecturer2 = Lecturer('Илья','Круглов',['Математика','Физика'])

reviewer1 = Reviewer('Денис','Попков',['Математика','Физика'])
reviewer2 = Reviewer('Рома','Игошев',['Математика','Физика'])

reviewer1.rate_hw(student1, 'Математика', 5)
reviewer1.rate_hw(student2, 'Математика', 4)

reviewer2.rate_hw(student1, 'Физика', 3)
reviewer2.rate_hw(student2, 'Физика', 5)

#оценки лекторам от студентов
student1.add_grade_Lecturer(lecturer1, 'Математика', 7)
student2.add_grade_Lecturer(lecturer2, 'Физика', 7)

print(student1)
print(GetMidGradeAllLecturers([lecturer1], 'Математика'))
