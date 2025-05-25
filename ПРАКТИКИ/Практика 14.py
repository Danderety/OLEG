import json

# with open('weather.json', 'r') as f:
#     data = json.load(f)

# for city in data['cities']:
#     if city['temp'] > 30:
#         print(str(city['name']))


# with open('product.json', 'r+') as f: #октрываем базу данных "r" - читать "w" -  записывать
#     data = json.load(f) #подгружаем базу данных и присваиваем значение 
#     for product in data['tovari']: # запускаем цикл перебора всех презиков
#         print(f'Цена {product['name']} поднялась на {product['price']*0.1}')
#         product['price'] *= 1.1
#         print(f'Цена {product['name']} теперь {product['price']}')
#     f.seek(0) #чистка базы данных от старого 
#     json.dump(data, f, indent=4) #загружаем обратно базу данных вместо старой и делаем с помощью   indent=4   означает что запись будет выглядеть не горизонтально а вертикально на 4 строки вниз
with open('orders.json', 'r') as f:
    data = json.load(f)
total = 0 
for order in data['orders']:    
    total += order['price']
print(total)
    

