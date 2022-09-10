# 工厂函数

# 这是一个计算x的n次方的函数,外层函数变量是n,嵌套在里边的函数变量是x
def func_n(n):
    '''输入n返回一个可以计算x的n次方的函数func_x'''
    def func_x(x):
        '''输入x,返回x的n次方'''
        return x ** n
    return func_x

f_p2 = func_n(2)  # n=2,f_p2 = func_x,切func_x内部的n=2
result = f_p2(4)  # n=2, result = func_x(4),返回是4**2
print(result)
    
