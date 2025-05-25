# Вот несколько заданий по Python, связанных с классами и ООП, разного уровня сложности:  

# ### **1. Базовые задания**  
# 1. **Создание класса**  
#    - Создай класс `Person` с атрибутами `name` (имя) и `age` (возраст).  
#    - Добавь метод `introduce()`, который выводит: `"Привет, меня зовут [name] и мне [age] лет."`  

# 2. **Калькулятор**  
#    - Создай класс `Calculator` с методами `add`, `subtract`, `multiply`, `divide`.  
#    - Каждый метод должен принимать два числа и возвращать результат операции.  

# 3. **Книга**  
#    - Создай класс `Book` с атрибутами `title`, `author` и `year`.  
#    - Добавь метод `get_info()`, который возвращает строку: `"[title] написан(а) [author] в [year] году."`  

# ---  

# ### **2. Задания среднего уровня**  
# 4. **Банковский счёт**  
#    - Создай класс `BankAccount` с атрибутами `owner` (владелец) и `balance` (баланс).  
#    - Добавь методы:  
#      - `deposit(amount)` – пополняет баланс.  
#      - `withdraw(amount)` – снимает деньги (если хватает средств).  
#      - `check_balance()` – выводит текущий баланс.  

  

# 6. **Студенты и группа**  
#    - Создай класс `Student` с атрибутами `name` и `grades` (список оценок).  
#    - Создай класс `Group`, который хранит список студентов.  
#    - Добавь методы:  
#      - `add_student(student)` – добавляет студента в группу.  
#      - `remove_student(student)` – удаляет студента.  
#      - `get_average_grade()` – считает средний балл группы.  

# ---  

# ### **3. Продвинутые задания**  
# 7. **Фигуры (наследование)**  
#    - Создай базовый класс `Shape` с методом `area()` (возвращает 0).  
#    - Создай подклассы `Circle`, `Rectangle`, `Triangle`, переопределяющие `area()`.  

# 8. **Магазин и товары**  
#    - Создай класс `Product` с атрибутами `name`, `price`, `quantity`.  
#    - Создай класс `Store`, который может добавлять/удалять товары и считать общую стоимость.  

# 9. **Игра "Змейка" (ООП подход)**  
#    - Создай классы `Snake`, `Food`, `Game`.  
#    - Змейка должна двигаться, есть еду и увеличиваться.  

# ---  

# **Дополнительные идеи:**  
# - Реализуй класс `ToDoList` для управления задачами.  
# - Создай систему классов для игры в "Кки-нолики".  
# - Напиши класс `Fraction` для работы с дробями (сложение, вычитание и т. д.).  

# Какое задание тебе больше нравится? Могу помочь с реализацией! 🚀

# class Car:
#     def __init__(self, brand: str, model: str, year: int, probeg: float):
#         self.brand =brand
#         self.model =model
#         self.year =year
#         self.probeg =probeg

#     def drive(self, distance: float):
#         if distance <= 0:
#             print("Ошибка")
        
#         else:
#             self.probeg += distance
#             print(f"Пройдено нынешним владельцем {distance} км. Общий пробег: {self.probeg} км")
#     def display_info(self):
#         info = f'Марка автомобиля - {self.brand} Модель автомобиля - {self.model} Год выпуска - {self.year} Пробег - {self.probeg} км'
#         print(info)
#         return info

# car = Car("Toyota", "Camry 3.5", 2012, 2000)
# car.drive(3000)
# car.display_info()






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

