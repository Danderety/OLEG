v=[]
while True:
    print('\n1: Написать заметку\n2: Все заметки\n3: Удалить заметку')
    c=int(input())
    if c==1 or c==2 or c==3: 
        if c==1:
            a = str(input("Введите заметку: "))
            if len(a) > 30:
                print("Превышение допустимого количества символов")
            else:
                v.append(a)
        elif c==2:
            if not v:
                print("Заметок нет!")
            else:
                print('История операций:')
                for i in v:
                    print(f'ID - {v.index(i)} Заметка: {i}')
        elif c==3:
            if not v:
                print("Заметок нет")
            else:
                dil = v.pop(int(input("Введите id: ")))
                print("Заметка удалена!")
    else: 
        print('Некоректное число')
        continue
# b=[]
# while True:
#     print('1: добавить заметку,\n2: история заметок,\n3: выход')
#     c=input()
#     if c=='1' or c=='2' or c=='3':
#         if c=='1':
#             a=str(input('Заметка: '))
#             b.append(a)

#         elif c=="2":
#             for i in b:

#                 print(i)
#     else:
#         continue    
# v=[]
# while True:
#     a=float(input("Введите первое число: "))
#     b=float(input("Введите второе число: "))
#     print('1: Сложение,\n2:Вычитание,\n3:Умножение,\n4:Деление,\n5:История,\n6:Выход')
#     c=input()
#     if c=='1' and c=='2' and c=='3' and c=='4' and c=='5' and c=='6': 
#         if c=='1':
#             result=a+b
#             x='+' 
#             v.append(f'{a}{x}{b}={result}')
#             print('Результат: ',result)
#         elif c=='2': 
#             result=a-b
#             x='-' 
#             v.append(f'{a}{x}{b}={result}')
#             print('Результат: ',result)
#         elif c=='3':
#             result=a*b
#             x='*' 
#             v.append(f'{a}{x}{b}={result}')
#             print('Результат: ',result)
#         elif c=='4':
#             result=a/b
#             x='/' 
#             v.append(f'{a}{x}{b}={result}')
#             print('Результат: ',result)
#         elif c=='5':
#             print('История операций')
#             for i in v:
#                 print(i)
#         elif c=='6':
#             break 
#     else: 
#         print('Некоректное число')
#         continue
# n = int(input())  # Количество учеников
# f = 0  # Счетчик неудовлетворительных оценок
# all = False  # Флаг, был ли хотя бы один ученик с 10 правильными ответами

# for _ in range(n):
#     c = int(input())  # Количество правильно решенных примеров
#     if c < 5:  # Неудовлетворительная оценка (меньше половины от 10)
#         f += 1
#     if c == 10:  # Проверяем, есть ли хотя бы один отличник
#         all = True

# print(f)  # Выводим количество неудовлетворительных оценок
# if all:
#     print('YES')
# else:
#     print("NO")
