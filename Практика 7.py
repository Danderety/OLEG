# def chet(f):
#     if f % 2 == 0:
#         return True
#     else:
#         return False
# print(chet(int(input("Ввведите число: "))))


# import random

# def temp():
#     return random.randint(-100,30)
# def calc(t):
#     if t< 0:
#         return "Слишком холодно " + str(t)
#     elif t > 25:
#         return "Слишком жарко " + str(t)
#     else:
#         return "Норма " + str(t)

# print(calc(temp()))

# def chet(f, g):
#     if f % 2 == 0 and g % 2 == 0:
#         return True
#     else:
#         return False
# print(chet(int(input("Ввведите число 1: ")),int(input("Ввведите число 2: ")) ))


# def f():
#     pass
# print(f())

# f = lambda x, y: x + y
# print(f(3,4))


# stroka = ['Ананас',"Банан","Яблоко" ,"Мандарин" ,"Груша"]
# sorted = sorted(stroka, key=lambda stroka: len(stroka))
# print(sorted)

# def f(*fff):
#     print(sorted(fff, len(fff)))
# f('Ананас',"Банан","Яблоко" ,"Мандарин" ,"Груша")
# def sort_words_by_length(*args):
#     sorted_words = sorted(args, key=lambda word: len(word))
#     return sorted_words

# передаём слова через *args
# result = sort_words_by_length('Ананас', 'Банан', 'Яблоко', 'Мандарин', 'Груша')
# print(result)
