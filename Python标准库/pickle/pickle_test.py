import pickle

# 定义一个函数，测试用
def func(x):
    print(x)

# dumps()将数据转换为plk格式的字符串
print('函数：', func) # 输出是一个function对象
data1 = pickle.dumps(func)
print(data1)

# loads()将plk格式字符串转码为python对象
print(pickle.loads(data1))

# 保存文件,'wb'
with open('data.plk', 'wb') as f:
    pickle.dump(func,f)

# 读取文件,'rb'
with open('data.plk', 'rb') as f:
    data = pickle.load(f)
    print('从文件读取的data：',data)