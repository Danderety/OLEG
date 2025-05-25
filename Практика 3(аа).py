student = [
    {"name": "Олег", "grades": [3,5,4,3,2,5]},
    {"name": "Ярослав", "grades": [3,5,4,3,2,5,2,5]}
]
for i in student:
    sr = sum(i["grades"]) / len(i["grades"])
    print(f"{i['name']}: Ср.балл {sr:.1f}")