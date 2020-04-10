#! /usr/bin/python3
# coding: utf-8
# @Author: Jorhelp<jorhelp@tom.com>
# @Date: 2020年 04月 09日 星期四 18:44:31 CST
# @Desc: 枚举qq号，爬取qq对应的头像


import os
import time
import imghdr
import logging
import requests
import logging.config
from threading import Thread, Lock
#  from multiprocessing import Process, Lock


#-----------------------
# global vars
#-----------------------
CWD = os.path.abspath(".")
QQ = 950000   # 从哪个qq号开始
PHOTO_PATH = os.path.join(CWD, "qq_photos")   # 头像存放位置
TH_NUM = 16   # 线程数

# 日志配置
logging_config_file = os.path.join(CWD, "conf/logging.conf")
logging.config.fileConfig(logging_config_file)
logger = logging.getLogger("spider")



class QSpider(object):

    def __init__(self, qq=QQ, photo_path=PHOTO_PATH, th_num=TH_NUM):
        self.qq = qq
        self.photo_path = photo_path
        self.th_num = th_num
        self.default_photo = []   # 存储默认的企鹅图像，来过滤默认头像
        self.lock = Lock()   # 线程锁
        self.pool = []   # 线程池

    def get_qq(self):
        """生成一个qq号"""
        with self.lock:
            _qq = self.qq
            #  with open("last_qq", 'w') as f:
            #      # 记录最后一次请求的qq
            #      f.write(str(_qq))
            self.qq += 1
            return _qq

    def get_url(self, qq):
        """返回qq所对应的链接"""
        return 'http://q2.qlogo.cn/headimg_dl?dst_uin=' + str(qq) + '&spec=5'

    def get_r(self, url):
        """requests请求url
        接收一个url
        返回response
        """
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return r
        except Exception as e:
            logger.error(url)
            logger.error(e)
            return False

    def is_net_ok(self):
        """测试网络连通情况"""
        if self.get_r('https://www.baidu.com'):
            logger.info("网络状况正常")
            return True
        logger.error("网络未连通")
        return False

    def get_default_photo(self):
        """获取默认头像
        有些qq号返回的是默认企鹅图像，该函数会获取默认头像并保存
        之后其他头像与其进行对比，若也是默认头像就不存盘
        """
        for _qq in [1, 10011]:
            _url = self.get_url(_qq)
            r = self.get_r(_url)
            if not r:
                return False
            else:
                self.default_photo.append(r.content)
        return True

    def get_photo(self):
        """抓取头像
        拿一个qq号，合成链接，获取头像
        如果头像是企鹅，丢掉；否则存盘
        """
        while True:
            _qq = self.get_qq()
            _url = self.get_url(_qq)
            r = self.get_r(_url)
            if r:
                if r.content in self.default_photo:
                    # 先保存一下默认的头像看是否有问题
                    #  with open('default/{}.jpeg'.format(_qq), 'wb') as f:
                    #      f.write(r.content)
                    continue
                else:
                    _file_path = os.path.join(self.photo_path, str(_qq)+"."+imghdr.what('', r.content))
                    with open(_file_path, "wb") as f:
                        f.write(r.content)
                        print("{} 的头像已经保存!".format(_qq))
            time.sleep(0.1)

    def run(self):
        """主函数"""
        if self.is_net_ok() and self.get_default_photo():
            for _ in range(self.th_num):
                th = Thread(target=self.get_photo)
                #  th = Process(target=self.get_photo)
                self.pool.append(th)
            for th in self.pool:
                th.start()



if __name__ == "__main__":
    sp = QSpider()
    sp.run()
