## @_@

这是我见过最简单的爬虫，一点反爬机制都没有，甚至都不用管header，直接请求url就行!! 

理论上可以获取所有的QQ头像!! 但是我现在拿到这一大堆头像不知该如何利用，所以先放着吧


## 使用

可能需要安装requests(如果默认库里没有带的话)；还需要邻居家的优质高速wifi(你懂的)

直接执行`qq_spider.py`文件即可


## 多进程 or 多线程

虽然有GIL的限制，但是爬虫是IO密集型的，因为其需要频繁的将数据写入磁盘，所以多线程与多进程差别应该不大

线(进)程数的设置：
+	如果想提高准确率，可以将线(进)程数设置的底一点，不过速度可能比较慢
+	如果想快速爬，对丢失情况要求不高的话，可以将进程数调高


## 题外话

QQ号为8的那个用户是马总吗???
