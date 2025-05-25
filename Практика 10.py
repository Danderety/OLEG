# class Car:
#     def __init__(self, brand, model, year):
#         self.brand = brand
#         self.model = model
#         self.year = year
#         self.__km = 0
#     def __str__(self):
#         return(f"Марка:{self.brand}, Модель: {self.model}, Год выпуска: {self.year}")
#     def getkm(self):
#         return self.__km
#     def addkm(self, km):
#         if km > 0:
#             self.__km+=km
#         else:
#             print("Пробег не бывает отрицательным")
#     def start(self):
#         print("Двигатель запущен")

# class Electrocar(Car):
#     def __init__(self, brand, model, year,battery):
#         super().__init__(brand,model,year)
#         self.battery =battery
#     def __str__(self):
#         return(f"Марка:{self.brand}, Модель: {self.model}, Год выпуска: {self.year}, Обьем батареи {self.battery}")

#     def start(self):
#         print("двигатель запущен электричка")

# my_car = Car('Tesla', 'Model Y',2024)
# my_car1 = Electrocar('SangYong', 'Canyon',2011, 500)
# print(my_car)
# print(my_car1)
# my_car.start()Ф
# my_car1.start()
# my_car.addkm(-100)

# my_car.addkm(300)
# print(my_car.getkm())

# class Animal:
#     def sound(self):
#         pass
# class Dog(Animal):
#     def sound(self):
#         return "Гав"

# class Cat(Animal):
#     def sound(self):
#         return "Мяу"

# print(Dog().sound())
# print(Cat().sound())
# class Engine:
#     def start(self):
#         print("Двигатель запущен")
# class Car:
#     def __init__(self,brand):
#         self.brand=brand
#         self.engine=Engine()
   
#     def start(self):
#         self.engine.start()
# car=Car("Gelik")
# car.start()
# class math:
#     @staticmethod
#     def add(a,b):
#         return a + b
# print(math.add(3,8))





