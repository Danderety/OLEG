# def f(*args): 
#     return sum(args) #считает сумму всех чисел в списке
# print(f(4,5,6,3,6,4,76,4,6,4,6,4,456,43,6,63))
# def f(**kwargs):
#     print(f"Имя: {kwargs.get('name')}, Возраст: {kwargs.get('age')}")
# f(name="Олег", age=16)

#Вывод индекса и значения
# def f(*args):
#     for index, value in enumerate(args):
#         print(f"{index}: {value}")
# f(12,343,5435,65464)
# def f(*args):
#     for i in args:
#         print(f"{args.index(i)}, {i}")
# f(12,343,5435,65464)



# Количество параметров
# def f(**kwargs):
#     return len(kwargs)
# print(f(name="gg", color="blue", hair="corty"))


#Сортировка по длине
# stroka = ['Ананас',"Банан","Яблоко" ,"Мандарин" ,"Груша"]
# sorted = sorted(stroka, key=lambda stroka: len(stroka))
# print(sorted)



#Фильтр положительнх чисел
# n= [-2,3,6,-10,54,66,-100,200,400]
# p= list(filter(lambda x: x>0, n))
# print(p)

# g=[]
# def f(*args):
#     for i in args:
#         if i > 0:
#             g.append(i)
# f(3,6,4,8,4,7,4,8,4,-4,-30,0,-20,-210,-450)
# print(g)

#КОРТЕЖ



# 1 Сумма перенос в *args
# f = lambda x, y, z, v, g, h: (x + y + z +v +g +h)/6
# print(f(1,43,5,6,7,8))
# def f(*args):
#     return sum(args)/ len(args)
# print(f(1,43,5,6,7,8))

# 2 Сортировка по длине перенос в *args
# stroka = ['Ананас',"Банан","Яблоко" ,"Мандарин" ,"Груша"]
# sorted = sorted(stroka, key=lambda stroka: len(stroka))
# print(sorted)
# def stroka(*args):
#     return sorted(args, key=lambda x: len(x))
# print(stroka('Ананас',"Банан","Яблоко" ,"Мандарин" ,"Груша"))

# 3 Длина строки перенос в *args
# string_length = lambda s: len(s)
# print(f'Длина строки: {string_length(input("Введите строку: "))}')  
# def f(*args):
#     return [len(s) for s in args]
# print(f('fdsfdsfs'))

# 4 Проверка числа больше 100 перенос в *args
# is_greater_100 = lambda x: x > 100
# print(is_greater_100(150)) 
# def check(*args):
#     return [x> 100 for x in args]
# print(check(100,343,50,4,540))
# g=[]
# def f(*args):
#     for i in args:
#         if i > 0:
#             g.append(i)
# f(3,6,4,8,4,7,4,8,4,-4,-30,0,-20,-210,-450)
# print(g)

# *5 Минимальное и максимальное число перенос в lambda
# def min_max(*args):
#     return min(args), max(args)

# print(min_max(10, 5, 20, 1))  
# def f(*args):
#     return min(args), max(args)
# print(f(10, 5, 20, 1))

