#! /usr/bin/python3
# coding: utf-8
# @Author: Jorhelp<jorhelp@tom.com>
# @Date: 2020年 04月 09日 星期四 22:07:00 CST
# @Desc: 用来调试或其他额外的工作

import os

os.chdir("qq_photos/")
files = os.listdir()

for i in files:
    os.remove(i)

#  with open('10011.png', 'rb') as f:
#      default = f.read()
#
#
#  for i in files:
#      with open(i, 'rb') as f:
#          if f.read() == default:
#              print(i)
#              os.remove(i)
