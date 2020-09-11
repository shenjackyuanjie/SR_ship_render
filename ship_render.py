"""
by shenjack
"""

import os
import xml
import math
import json
import shutil
import random
import easygui
from PIL import Image
import xml.dom.minidom
from xml.dom.minidom import parse
# --------------可修改变量------------------
ship_pic_filename = 'ShipSprites.png'
ship_pic_config = 'ShipSprites.xml'
output_pic_size = [1024, 1024]
output_pic_color = 'white'
render_ship_name = 'test.xml'
# --------------可修改变量结束--------------

class ship_render():

    def __init__(self, render_size=[1024, 1024], render_color='white'):
        self.pic_path = './pic_storage/'
        self.part_config = 'part_config.json'
        self.part_pics = {}
        self.part_list = []
        self.render_pic = Image.new('RGB', render_size, render_color)
        self.SR_pi = 3.141593

    def get_At(self, name, in_xml, need_type=str):
        name_type = type(name) # 判定输入需要获取At的数据类型
        if name_type == list: # 如果需要获取列表数据
            At_list = [] # 获取到的数据的列表
            for need_name in name: # 挨个获取
                get = in_xml.getAttribute(need_name) # 要说啥？
                At_list.append(need_type(get))
            return At_list
        elif name_type == str: # 直接获取
            At = in_xml.getAttribute(name)
        else: # 说好的只能文本和列表呢？？
            raise TypeError('only str and list type is ok but you give me a' + name_type + 'type')
        return need_type(At)

    def save_part_config(self):
        try:
            with open(self.part_config, mode='r'):
                pass
        except:
            pass

    def load_xml(self, xml_name, getEBTN='', mode='r'):
        xml_load = xml.dom.minidom.parse(xml_name, mode) # 先load
        if not (getEBTN == ''): # 需要顺手获取一波数据
            xml_get = xml_load.getElementsByTagName(getEBTN)
        else:
            return xml_load
        return xml_get

    def load_part_pic(self):
        pics = os.listdir(self.pic_path) # 获取文件夹里的图片列表
        for pic in pics: # 挨个处理
            part_pic = Image.open(self.pic_path + pic) # 打开新图片
            pic_name = pic[:-4] # 文件名处理
            self.part_pics[pic_name] = part_pic # 把新的图片存储进去

    def load_ship_xml(self, ship_xml_name):
        ship_xml = self.load_xml(ship_xml_name, 'part') # 先加载飞船的存档
        for part in ship_xml: # 挨个零件保存
            x, y = self.get_At(['x', 'y'], part, int) # 部件的x、y值
            t = self.get_At('angle', part, float) # 部件的旋转值
            PT = self.get_At('partType', part, float) # 部件的类型
            part_config = [PT, x, y, t] # 压缩数据并保存
            self.part_list.append(part_config)

    def reflash_pic(self, load_pic_name, load_xml_name):
        pic = Image.open(load_pic_name, mode='r') # 加载被切割图片
        xml_sprite = self.load_xml(load_pic_name, 'sprite')
        for pic_config in xml_sprite:
            x, y, w, h = self.get_At(['x', 'y', 'w', 'h'], pic_config, int)
            n = self.get_At('n', pic_config, str) # 一  大  堆  数  据
            crop_box = [x, y, x+w, y+h] # 确定切割框
            save_name = n[:-4] + '.png' # 确定保存名
            crop_pic = pic.crop(crop_box) # 切割照片
            crop_pic.save(save_name) # 保存照片
            shutil.move('./' + save_name, self.pic_path + save_name) # 移动图片
        self.load_part_pic()

    def render_ship(self, render_ship_name):
        self.load_ship_xml(render_ship_name)
        self.load_part_pic()
        for part in self.part_list:
            print(part)
            pass



test_class = ship_render()
