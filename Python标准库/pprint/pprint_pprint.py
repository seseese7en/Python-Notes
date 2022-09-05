import pprint

company = {
    "Apple":    {"founder": "Steven Jobs", "prodctions":["IPhone", "Mac"]},
    "MicroSoft":{"founder": "Bill Gates", "prodctions": ["Windows", "Office","Xbox"]},
}

# 观察print，pprint的区别
print(company)
print('-' * 80)
pprint.pprint(company)