import pprint

company = {
    "Apple":    {"founder": "Steven Jobs", "prodctions":["IPhone", "Mac"]},
    "MicroSoft":{"founder": "Bill Gates", "prodctions": ["Windows", "Office","Xbox"]},
}

# 将字符串写入本地py文件
with open('company_file.py', 'w') as f:
    data = 'company = ' + pprint.pformat(company)
    f.write(data)

# 需要使用company变量的时候直接调用文件
import company_file
pprint.pprint(company_file.company)