# Python-Notes

记录Python过程中遇到的问题！！！

# 9.类

## 9.8迭代器

**可迭代对象:** 可以使用for循环遍历的容器对象,例如列表,元组,字符串,文本文件等.

```python
for element in [1, 2, 3]:
    print(element)
for element in (1, 2, 3):
    print(element)
for key in {'one':1, 'two':2}:
    print(key)
for char in "123":
    print(char)
for line in open("myfile.txt"):
    print(line, end='')
```

**迭代器:** iter(可迭代对象)返回一个迭代器.

```python
a = 'abc'
it = iter(a)
print(type(it))
```

```powershell
<class 'str_iterator'>
```

可以看到it是一个迭代器.

迭代器可以使用next()方法逐一访问迭代器元素.

```python
a = 'abc'
it = iter(a)
print(type(it))
print(type(it))
print(type(it))
```

```powershell
a
b
c
```

当元素用尽是,将引发StopIteration错误.

```python
a = 'abc'
it = iter(a)
print(next(it))
print(next(it))
print(next(it))
print(next(it))
```

```powershell
a
b
c
Traceback (most recent call last):
  File "d:\Python\Python-Notes\test.py", line 6, in <module>
    print(next(it))
StopIteration
```

**幕后机制**，给你的类添加迭代器行为。 定义一个__iter__()方法来返回一个带有__next__()方法的对象。 如果类已定义了__next__()，则__iter__()可以简单地返回self:

```python
class Reverse:
    '''用于向后循环序列的迭代器'''
    def __init__(self, data) -> None:
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:  # 代表迭代器元素被用完了
            raise StopIteration
        self.index -= 1  # 每次调用next方法,迭代器就去掉一个元素
        return self.data[self.index]  # 这里是倒序调用元素

rev = Reverse('spam')
print(iter(rev))
for char in rev:
    print(char)
```

输出:

```powershell
<__main__.Reverse object at 0x0000020DDA8DBE50>
m
a
p
s
```

其实迭代器幕后的原理就是调用iter方法时,类的内部就会调用__iter__()方法,生成一个迭代器,调用next方法时,类内部就会自动调用__next__()方法.

## 9.9生成器

**生成器**是一个用于创建迭代器的简单而强大的工具。 它们的写法类似于标准的函数，但当它们要返回数据时会使用yield语句。 每次在生成器上调用next()时，它会从上次离开的位置恢复执行（它会记住上次执行语句时的所有数据值）。 一个显示如何非常容易地创建生成器的示例如下:

```python
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]
for char in reverse('golf'):
    print(char)
```

输出:

```powershell
f
l
o
g
```

**注意:** 程序碰到yield语句后就会暂停执行,下次从暂停出继续执行.

示例:

```python
def reverse(data):
    for index in range(len(data)):
        yield data[index]
        print(index)

data = reverse('hello')

next(data)  # 第一次
next(data)  # 第二次
next(data)  # 第三次
```

输出:

```powershell
0
1
```

这里我们调用了三次,为什么只输出了0和1?

因为第一次调用next时,程序执行到yield处,返回了data[inex=0]也就是h就停止了,第二次从print(index)出开始执行,所以输出了0,然后运行到yield data[index=1]出又停止了,第三次运行从print(index=1)出运行,输出了1,然后程序运行到yield data[index=2]就停止了.

可以用生成器来完成的操作同样可以用前一节所描述的基于类的迭代器来完成。 但生成器的写法更为紧凑，因为它会自动创建__iter__()和__next__()方法。

另一个关键特性在于局部变量和执行状态会在每次调用之间自动保存。 这使得该函数相比使用self.index和self.data这种实例变量的方式更易编写且更为清晰。

除了会自动创建方法和保存程序状态，当生成器终结时，它们还会自动引发StopIterater这些特性结合在一起，使得创建迭代器能与编写常规函数一样容易。

## 9.10生成器表达式

某些简单的生成器可以写成简洁的表达式代码，所用语法类似**列表推导式**，但外层为**圆括号**而非方括号。 这种表达式被设计用于生成器将立即被外层函数所使用的情况。 生成器表达式相比完整的生成器更紧凑但较不灵活，**相比等效的列表推导式则更为节省内存**。

示例:1

```python
l = (i for i in range(10))
print(l)
```

输出:

```powershell
<generator object <genexpr> at 0x000001B045D82490>
```

示例2:

生成器表达式的一些应用

```python
# 1到10的平方之和
sum_of_num = sum(i*i for i in range(10))
print(sum_of_num)

# 点积之和
x = [1,4,7]
y = [2,5,8]
sum_dot_product = sum(x*y for x,y in zip(x,y))
print(sum_dot_product)
```

输出:

```powershell
285
78
```

**补充:** zip的作用是将可迭代对象压缩成一个类似于元组的压缩对象,在函数里以参数的形式传入时,可以使用*来进行解压.

```python
a = [1, 2, 3]
b = ['a', 'b', 'c']

zip(a, b)
print(list(zip(a, b)))

print(*zip(a, b))

a = 'abc'
b = 'xyz'

zip(a, b)
print(list(zip(a, b)))

print(*zip(a, b))
```

```powershell
[(1, 'a'), (2, 'b'), (3, 'c')]
(1, 'a') (2, 'b') (3, 'c')

[('a', 'x'), ('b', 'y'), ('c', 'z')]
('a', 'x') ('b', 'y') ('c', 'z')
```
