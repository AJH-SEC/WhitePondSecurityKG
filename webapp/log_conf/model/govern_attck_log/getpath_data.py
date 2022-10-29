# -*- coding: UTF-8 -*-

'''
读取文件的路径
保存起来
'''

import glob
import os
from xml.dom.minidom import parse

class data_path:
    def __init__(self, path):
        self.path = path

    # 对规则库进行一个属性值一个处理
    def relustr(self,systlog):
        self.mit = systlog.split(',')
        return self.mit

    # 对规则库里面的字段进行处理
    def replice(self,ruleinitlist):
        self.mnt = []
        for mint in ruleinitlist:
            min1t = mint.replace('FTPD: ', '')
            # min1t = min1t.replace(' ', '')
            self.mit.append(min1t)
        return self.mnt

    def all_path(self):
        '''
        循环全部文件的路径
        :return: 保存到列表里面返回
        '''
        self.lujing = []
        if os.path.exists(self.path):
            f = glob.glob(self.path+'\\*.xml')
            for file in f:
                self.lujing.append(file)

        return self.lujing

    def initially(self):
        '''
        循环读取文件路径并初始化解析
        :return: #将解析的初始信息保存返回
        '''
        self.root_list = []
        self.groupstr_list = []
        self.dirlist = self.all_path()
        for route in self.dirlist:
            self.contents = parse(route)
            self.root = self.contents.documentElement

            # 获取根节点的属性值
            self.atr_root = self.root.attributes['name']
            self.groupvalue = self.atr_root.value
            self.groupstr = self.relustr(self.groupvalue)

            self.root_list.append(self.root)
            self.groupstr_list.append(self.groupstr)
        return self.root_list,self.groupstr_list


# if __name__ == '__main__':
#     dirlist = r'E:\Desktop\niso_server-main\rules'
#     dm = data_path(dirlist)
#     dm.initially()