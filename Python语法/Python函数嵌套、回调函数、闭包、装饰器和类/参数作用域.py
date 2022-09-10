# 正常情况下,函数内部的变量是局部变量
x = 1

def cal(x):
    x = 2 # 这里在函数内部将2赋值给x
    print('call is over')

# 调用函数,观察全局变量是否有所改变
cal(x=x)

print(x)  # 预期是1,因为x是全局变量,而函数体内部的是局部变量

# 如果向修改x的值可以在函数内部声明全局变量
def func():
    global x  # 这样x就是全局变量了
    x = 2
    print('func is over')

# 调用func
func()
print(x)  # x被成功修改为2