class Student:
    def __init__(self, name: str):
        """Инициализация студента с именем и пустым списком оценок"""
        self.name = name
        self.grades = []  # Будет хранить все оценки студента
    
    def add_grade(self, grade: int) -> None:
        """Добавляет оценку (от 2 до 5)"""
        if 2 <= grade <= 5:
            self.grades.append(grade)
        else:
            print(f"Ошибка: оценка {grade} недопустима (должна быть от 2 до 5)")
    
    def get_average(self) -> float:
        """Возвращает средний балл студента"""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)


class Group:
    def __init__(self):
        """Инициализация группы с пустым списком студентов"""
        self.students = []
    
    def add_student(self, student: Student) -> None:
        """Добавляет студента в группу"""
        self.students.append(student)
        print(f"Студент {student.name} добавлен в группу")
    
    def remove_student(self, student: Student) -> None:
        """Удаляет студента из группы"""
        if student in self.students:
            self.students.remove(student)
            print(f"Студент {student.name} удалён из группы")
        else:
            print(f"Студент {student.name} не найден в группе")
    
    def get_group_average(self) -> float:
        """Возвращает средний балл всей группы"""
        if not self.students:
            print("В группе нет студентов!")
            return 0.0
        
        total = sum(student.get_average() for student in self.students)
        return total / len(self.students)


# Создаём студентов
student1 = Student("Леха")
student1.add_grade(5)
student1.add_grade(4)
student1.add_grade(2)

student2 = Student("Димон")
student2.add_grade(5)
student2.add_grade(3)
student2.add_grade(4)

student3 = Student("Гена")
student3.add_grade(5)
student3.add_grade(3)
student3.add_grade(2)

student4 = Student("Игорь")
student4.add_grade(3)
student4.add_grade(3)
student4.add_grade(3)

student5 = Student("Толик")
student5.add_grade(2)
student5.add_grade(2)
student5.add_grade(2)

student6 = Student("Ванек")
student6.add_grade(4)
student6.add_grade(4)
student6.add_grade(4)

# Создаём группу и добавляем студентов
group = Group()
group.add_student(student1)
group.add_student(student2)
group.add_student(student3)
group.add_student(student4)
group.add_student(student5)
group.add_student(student6)

# Выводим средний балл группы
print(f'Средний балл группы: {group.get_group_average():.2f}')

# Выводим средние баллы каждого студента
print("\nСредние баллы студентов:")
for student in group.students:
    print(f"{student.name}: {student.get_average():.2f}")