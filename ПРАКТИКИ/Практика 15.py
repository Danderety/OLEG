import json


# with open('orders.json') as f:
#     data = json.load(f)


# html = """<table border = '1'
# <tr><th>Product</th><th>Кол-во</th></tr>"""
# for item in data['transactions']:
#     html += f'<tr><td> {item['product']} </td><td> {item['amount']} </td></tr>'


# html += "</table>"

# with open('report.html', 'w') as f:
#     f.write(html)


with open('data.json') as f:
    data = json.load(f)

data['people'].sort(key=lambda x: x['salary'], reverse = True)
print(data['people'][1]['name'])