# student = [
#     {"name": "Олег", "grades": [3,5,4,3,2,5]},
#     {"name": "Ярослав", "grades": [3,5,4,3,2,5,2,5]}
# ]
# for i in student:
#     sr = sum(i["grades"]) / len(i["grades"])
#     print(f"{i['name']}: Ср.балл {sr:.1f}")
# 1- чисел после запятой f - float
# sum - сумма чисел в списке
# len - считает количество значений в списке 

# student = [
#     {"name": "Олег", "grades": [3,5,4,3,2,5]},
#     {"name": "Ярослав", "grades": [3,5,4,3,2,5,2,5]}
# ]
# for i in student:
#     sr = sum(i["grades"]) / len(i["grades"])
#     if sr>=4:
#         result = "Сдал"
#     else:
#         result =  "Не сдал"
#     print(f'{i["name"]}: Средний балл {sr:.1f}, результат: {result}')


import random
num = random.randint(1,100)
attemps = 0
while True: 
    attemps += 1
    a = int(input("Введите число от 1 до 6: "))
    if attemps<3:
        print("Попытки кончились")
        break
    else:
        
        
        if a == num:
            print(f'Поздравляю ты угадал число за {attemps} попыток')
            break
        elif a <num:
            print(f"Число больше чем {a}")
        else:
            print(f"Число меньше чем {a}")
