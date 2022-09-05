# pickle模块

Python专用的持久化模块，可以持久化包括自定义类在内的各种数据

比较适合Python本身复杂数据的存贮

我自己的理解是**可以将Python中的<ins>对象</ins>直接存储到plk文件中，可以从文件里直接提取对象使用**

但是持久化后的字串是不可认读的，并且只能用于Python环境，不能用作与其它语言进行数据交换。

主要方法：
- dumps():把Python对象转码为plk格式的字符串bytes
- loads():把plk格式的字符串（bytes）转化为Python对象
- dump():把Python对象写入plk文件
- lload():从plk文件中导入Python对象
