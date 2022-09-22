# 协程与任务
## 协程
通过async/await语法来声明协程是编写asyncio应用的推荐方式.例如,以下代码打印"hello",等待1秒,再打印"world":
```
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')

asyncio.run(main())
```
**注意:** 简单的调用一个协程并不会使其被调度执行
```
main()
```
输出:
```
 RuntimeWarning: coroutine 'main' was never awaited
  main()
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```
要真正运行一个协程,asyncio提供了三种主要机制:
- asycnio.run()函数用来运行最高层级的入口点"main()"函数(参见上面的示例.)
- **等待**一个协程.以下代码会再等待3秒后打印'hello',然后再次等待1秒后打印'world'.

```
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(3, 'hello')
    await say_after(1, 'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```
输出:
```
started at 22:12:04
hello
world
finished at 22:12:08
```
从运行结果来看,先输出的'hello',过了1秒输出'world',而且总共用时4秒,所以并**没有**并发运行.
- asyncio.create_task()函数用来**并发**运行作为asyncio任务的多个协程任务.

```
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(say_after(3, 'hello'))
    task2 = asyncio.create_task(say_after(1, 'world'))

    print(f"started at {time.strftime('%X')}")

    # 等两个任务都完成
    # 预期先输出world且用时少于4秒
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```
**注意**,先输出了world,并且时间比之前快了1秒:
```
started at 22:23:33
world
hello
finished at 22:23:36
```
所以想实现并发运行协程,得使用**task**.

## 可等待对象
如果一个对象可以在await语句中使用,那么它就是**可等待对象.许多asyncio API都被设计为接受可等待对象.

可等待对象有三种主要类型:**Coroutine**,**Task**和**Future**

**Coroutine(协程):**

Python协程属于可等待对象,因此可以在在他协程中被等待:
```
import asyncio

async def nested():
    return 42

async def main():
    # 直接调用协程函数什么都不会发生
    # 因为只是创建了协程对象,但协程对象并没有被等待
    print(nested())

    # 等待协程对象
    print(await nested())

asyncio.run(main())
```
输出:
```
RuntimeWarning: coroutine 'nested' was never awaited
  print(nested())
RuntimeWarning: Enable tracemalloc to get the object allocation traceback  
42
```
如果协程对象没有被等待,就会提示`coroutine 'nested' was never awaited`,并且不会被执行.

**重要:** 在文档中"协程"可用来表示两个紧密关联的概念:
- 协程函数:定义形式为async def 的函数
- 协程对象:调用*协程函数*返回的对象

asyncio也支持旧式基于*生成器*的协程(使用装饰器和yield from的)

**Task(任务)**

*任务*被用来**并行**调度协程

当一个协程通过asyncio.create_task()等函数封装为成*任务*,该协程会被自动调度执行:

```
import asyncio

async def nested():
    return 42

async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task

asyncio.run(main())
```

**Futures**

Future是一种特殊的**低层级**可等待对象,表示一个异步操作的**最终结果**.

当一个Future对象*被等待*,这意味着协程将保持等待直到该Future对象在其他地方操作完毕。

在 asyncio 中需要 Future 对象以便允许通过 async/await 使用基于回调的代码。

通常情况下**没有必要**在应用层级的代码中创建 Future 对象。

Future 对象有时会由库和某些 asyncio API 暴露给用户，用作可等待对象:
```

async def main():
    await function_that_returns_a_future_object()

    # this is also valid:
    await asyncio.gather(
        function_that_returns_a_future_object(),
        some_python_coroutine()
    )
```

 一个很好的返回对象的低层级函数的示例是 loop.run_in_executor()。

**这段没看懂**

## 运行asyncio程序

asyncio.run(coro,*,debug=False)执行`coroutine coro`并返回结果.

此函数会运行传入的协程，负责管理 asyncio 事件循环，终结异步生成器，并关闭线程池。

当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用。

如果 debug 为 True，事件循环将以调试模式运行。

此函数总是会创建一个新的事件循环并在结束时关闭之。它应当被用作 asyncio 程序的主入口点，理想情况下应当只被调用一次。

示例:
```
async def main():
    await asyncio.sleep(1)
    print('hello')

asyncio.run(main())
```

## 创建任务
`asyncio.create_task(coro,*,name=None)`

将coro协程封装为一个Task并调度其执行.返回Task对象.name不为None,它将使用Task.set_name()来设为任务的名称.该任务会在get_running_loop()返回的循环中执行,如果当前线程没有正在运行的循环则会引发RuntimeError.


```
background_tasks = set()

for i in range(10):
    task = asyncio.create_task(some_coro(param=i))

    # 建立一个强有力的联系
    background_tasks.add(task)

    # add_done_callback是回调函数,意思是当任务执行完之后,执行括号里的参数(回调函数)
    # 调用的方法是集合的discard方法,discard()的作用是删除集合里的元素
    # 所以,这段代码的意思是当任务执行完之后,伤处background_tasks里的元素
    # 作用是防止重复调用集合里的任务
    task.add_done_callback(background_tasks.discard)
```

## 休眠

coroutine `asyncio.sleep(delay,result=None)`

阻塞delay指定的秒数.

如果指定了result,则当协程完成时将其返回给调用者.

sleep()总是会挂起当前任务,以允许其他任务运行.

将 delay 设为 0 将提供一个经优化的路径以允许其他任务运行。 这可供长期间运行的函数使用以避免在函数调用的全过程中阻塞事件循环.

一下协程示例运行5秒,每秒显示一次当前日期:
```
import asyncio
import datetime

async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        # 显示当前日期
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(display_date())
```

## 并发运行任务

`awaitable` `asyncio.gather(*aws,return_exceptions=False)`

gather英文意思是收集

并发运行aws序列中的可等待对象.

如果aws中的某个可等待对象为协程,它将自动被作为一个任务调度.

如果所有可等待对象都成功完成,结果将是一个由所有返回值聚合而成的列表.结果值的顺序与aws中可等待对象的顺序一直.

如果return_exceptions为False(默认),所引发的首个异常会立即传播给等待gather()的任务.aws序列中的其他可等待对象**不会被取消**并将继续运行.

如果return_exceptions为True,异常会和成功的结果一样处理,并聚合至结果列表.

如果gather()被取消,所有被提交(尚未完成)的可等待对象也会被取消.

如果aws序列中的任一Task或Future对象被取消,它将被当作引发了CancelledError一样处理--在此情况下gather()调用**不会**被取消.这是为了防止一个已提交的Task/Future被取消导致其他Task/Future也被取消.

示例:
```
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

async def main():
    # 同时执行三个协程,所有返回值会聚合成一个列表,赋值给L
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L)

asyncio.run(main())

# Expected output:
#
#     Task A: Compute factorial(2), currently i=2...
#     Task B: Compute factorial(3), currently i=2...
#     Task C: Compute factorial(4), currently i=2...
#     Task A: factorial(2) = 2
#     Task B: Compute factorial(3), currently i=3...
#     Task C: Compute factorial(4), currently i=3...
#     Task B: factorial(3) = 6
#     Task C: Compute factorial(4), currently i=4...
#     Task C: factorial(4) = 24
#     [2, 6, 24]
```

## 屏蔽取消操作

**注意：** 这段完全没看懂

awaitable asyncio.shield(aw)
保护一个 可等待对象 防止其被 取消。

如果 aw 是一个协程，它将自动被作为任务调度。

以下语句:
```
task = asyncio.create_task(something())
res = await shield(task)
```
相当于:
```
res = await something()
```
不同之处 在于如果包含它的协程被取消，在 something() 中运行的任务不会被取消。从 something() 的角度看来，取消操作并没有发生。然而其调用者已被取消，因此 "await" 表达式仍然会引发 CancelledError。

如果通过其他方式取消 something() (例如在其内部操作) 则 shield() 也会取消。

如果希望完全忽略取消操作 (不推荐) 则 shield() 函数需要配合一个 try/except 代码段，如下所示:
```
task = asyncio.create_task(something())
try:
    res = await shield(task)
except CancelledError:
    res = None
```
**重要** Save a reference to tasks passed to this function, to avoid a task disappearing mid-execution. The event loop only keeps weak references to tasks. A task that isn't referenced elsewhere may get garbage collected at any time, even before it's done.

## 超时

coroutine asyncio.wait_for(aw,timeout)

等待aw可等待对象完成,指定timeout秒数后超时.

如果aw是一个协程,它将自动被作为任务调度.

timeout可以为None,也可以为float或int型数值表示的等待秒数.如果timeout为None,则等待直到完成.

如果发生超时,任务将取消并引发asyncio.TimeoutError.

要避免任务取消,可以加上shield().**(这里因为shield不懂,所以暂时忽略)**

此函数将等待直到Future确实被取消,所以总等待时间可能超过timeout.如果在取消期间发生了异常,异常将会传播.

如果等待被取消,则aw指定的对象也会被取消.

示例1:没超时
```
import asyncio

async def eleternity():
    # 休眠一秒
    await asyncio.sleep(1)
    print('yay!')

async def main():
    try:
        await asyncio.wait_for(eleternity(), timeout=2)
    except asyncio.TimeoutError:
        print('timeout!')

asyncio.run(main())
```
示例2:超时
```
import asyncio

async def eternity():
    # 休眠五秒
    await asyncio.sleep(5)
    print('yay!')

async def main():
    try:
        await asyncio.wait_for(eternity(), timeout=2)
    except asyncio.TimeoutError:
        print('timeout!')

asyncio.run(main())
```

## 简单等待
coroutine asyncio.wait(aws,*,timeout=None,return_when=ALL_COMPLETE)

**并发**的运行aws可迭代对象中的可等待对象并进入阻塞状态知道满足return_when所指定的条件.

aws可迭代对象必须**不为空**.

返回一个由两个集合组成的元组(done, pending),分表表示**已完成**任务,和**代办**任务(未完成).

如果指定timeout(float或int)则它将用于控制返回之前等待的最长秒数.

**注意:** 此函数不会引发asyncio.TimeoutError.当超时发生时,未完成的Future或Task将在指定秒数后被返回.

return_when指定此函数应在合适返回.它必须为一下常数之一:
|常量|秒数|
|:---|:---|
|FIRST_COMPLETED|函数将在任意可等待对象结束或取消时返回|
|FIRST_EXCEPTION|函数将在任意可等待对象因引发异常而结束时返回.当没有引发异常时它就相当于ALL_COMPLETE|
|ALL_COMPLETED|函数将在所有可等待对象结束或取消时返回

与 wait_for() 不同，wait() 在超时发生时不会取消可等待对象。

示例1:
```
import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():

    task = [asyncio.create_task(say_after(2, x)) for x in range(5)]
    result = await asyncio.wait(task)
    print(type(result))

asyncio.run(main())
```
输出:
```
({<Task finished name='Task-6' coro=<say_after() done, defined at d:\Python\自学Python异步协程\test.py:3> result=None>, <Task finished name='Task-2' coro=<say_after() done, defined at d:\Python\自学Python异步协程\test.py:3> result=None>, <Task finished name='Task-3' coro=<say_after() done, defined at d:\Python\自学Python异步协程\test.py:3> result=None>, <Task finished name='Task-5' coro=<say_after() done, defined at d:\Python\自学Python异步协程\test.py:3> result=None>, <Task finished name='Task-4' coro=<say_after() done, defined at d:\Python\自学Python异步协程\test.py:3> result=None>}, set())
```
输出的结果显示,所有任务都被执行了,代办任务是一个空集合set()

示例2:
```
import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():

    task = [asyncio.create_task(say_after(x, x)) for x in range(5)]
    result = await asyncio.wait(task,timeout=2)
    print(result)

asyncio.run(main())
```
输出:
```
0
1
2
({<Task finished name='Task-2' coro=<say_after() done, defined at d:\Python\自学Python异步协程\test2.py:3> result=None>, <Task finished name='Task-3' coro=<say_after() done, defined at d:\Python\自学Python异步协程\test2.py:3> result=None>, <Task finished name='Task-4' coro=<say_after() done, defined at d:\Python\自学Python异步协程\test2.py:3> result=None>}, {<Task pending name='Task-6' coro=<say_after() running at d:\Python\自学Python异步协程\test2.py:4> wait_for=<Future pending cb=[Task.task_wakeup()]>>, <Task pending name='Task-5' coro=<say_after() running at d:\Python\自学Python异步协程\test2.py:4> wait_for=<Future pending cb=[Task.task_wakeup()]>>})
```
输出结果显示由三个任务完成了,又在两个在代办集合里,这是因为这两个任务超时了.

## 在线程中运行
coroutine asyncio.to_thread(func,/,*args,**kwargs)

**重点:** 

在不同线程中**异步**地运行**普通函数**func

返回一个可被等待以获取func的最终结果的协程.

这个协程函数主要用于执行在其他情况下会阻塞事件循环的IO密集型函数/方法.

示例:
```
import asyncio, time

def blocking_io():
    '''模拟IO阻塞'''
    time.sleep(2)

def test():
    start_time = time.time()
    # 运行两次IO阻塞
    blocking_io()
    blocking_io()
    end_time = time.time()
    print('cost time:', end_time - start_time)

async def main():
    start_time = time.time()
    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.to_thread(blocking_io)
    )
    end_time = time.time()
    print('cost time:', end_time - start_time)
    
if __name__ == '__main__':
    test()
    asyncio.run(main())
```
输出:
```
cost time: 4.019327640533447
cost time: 2.019427537918091
```
**结果分析:**

通过分析输出可以发现,不适用to_thread时函数是以同步方法运行的,所耗费的时间时4秒多,正好时单次执行所耗费时间的两倍.

而使用to_thread将blocking_io转化为协程函数之后,是以异步方式运行的,所以所花费的时间缩短了将近一半.

**参数:**

向此函数提供的任何 *args 和 **kwargs 会被直接传给 func。 并且，当前 contextvars.Context 会被传播，允许在不同的线程中访问来自事件循环的上下文变量
```
import asyncio, time

def blocking_io(delay,what=None):
    '''模拟IO阻塞'''
    time.sleep(delay)
    print(what)

async def main():
    start_time = time.time()
    await asyncio.gather(
        asyncio.to_thread(blocking_io, 3, what='hello'),
        asyncio.to_thread(blocking_io,2, what='world')
    )
    end_time = time.time()
    print('cost time:', end_time - start_time)
    
if __name__ == '__main__':
    asyncio.run(main())
```
输出:
```
world
hello
cost time: 3.016490936279297
```
需要为func传入参数时,可以直接在to_thread里按照位置形参或关键字形参传入即可.

## 跨协程调度

**没太看懂**

asyncio.run_coroutine_threadsafe(coro, loop)

向指定事件循环提交一个协程。（线程安全）

返回一个 concurrent.futures.Future 以等待来自其他 OS 线程的结果。

此函数应该从另一个 OS 线程中调用，而非事件循环运行所在线程。示例:
```
# Create a coroutine
coro = asyncio.sleep(1, result=3)

# Submit the coroutine to a given loop
future = asyncio.run_coroutine_threadsafe(coro, loop)

# Wait for the result with an optional timeout argument
assert future.result(timeout) == 3
```
如果在协程内产生了异常，将会通知返回的 Future 对象。它也可被用来取消事件循环中的任务:
```
try:
    result = future.result(timeout)
except concurrent.futures.TimeoutError:
    print('The coroutine took too long, cancelling the task...')
    future.cancel()
except Exception as exc:
    print(f'The coroutine raised an exception: {exc!r}')
else:
    print(f'The coroutine returned: {result!r}')
```

## 内省
asyncio.current_task(loop=None)

返回当前运行的 Task 实例，如果没有正在运行的任务则返回 None。

如果 loop 为 None 则会使用 get_running_loop() 获取当前事件循环。
