def calculate(x,y,func):
    '''调用func函数的功能来对x,y进行操作'''
    return func(x,y)

def max(x,y):
    '''比较x,y大小,输出大的那一个'''
    while x>y:
        print(x)
    else:
        print(y)

def sum(x,y):
    '''计算x+y'''
    print(x+y)

if __name__ == "__main__":
    # calculate -> max -> print(7)
    result_max = calculate(5,7,max)
    
    # calculate -> sum -> print(12)
    result_sum = calculate(5,7,sum)
    