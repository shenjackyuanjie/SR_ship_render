"""
by shenjack(shenjackyuanjie)
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
from main import tools as tt
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
        self.config_path = './config/'
        self.part_pics = {}
        self.part_list = []
        self.render_pic = Image.new('RGB', render_size, render_color)
        self.SR_pi = 3.141593

    def save_part_config(self, part_list_xml):
        save_dic = {'part_to_png': []}
        part_list = tt.load_xml(part_list_xml, getEBTN='PartType')
        for part_config in part_list:
            part_id, sprite = tt.get_At(['id', 'sprite'], part_config, need_type=str)
            push = {'part': part_id, 'png': sprite}
            save_dic['part_to_png'].append(push)
        with open(self.part_config, mode='w') as part_config_json:
            json.dump(save_dic, part_config_json)

    def load_part_pic(self):
        pics = os.listdir(self.pic_path)
        for pic in pics:
            part_pic = Image.open(self.pic_path + pic)
            pic_name = pic[:-4]
            self.part_pics[pic_name] = part_pic

    def load_ship_xml(self, ship_xml_name):
        ship_xml = tt.load_xml(ship_xml_name, 'part')
        for part in ship_xml:
            x, y = tt.get_At(['x', 'y'], part, int)
            t = tt.get_At('angle', part, float)
            PT = tt.get_At('partType', part, float)
            part_config = [PT, x, y, t]
            self.part_list.append(part_config)

    def reflash_pic(self, load_pic_name, load_xml_name):
        pic = Image.open(load_pic_name, mode='r')
        xml_sprite = tt.load_xml(load_pic_name, 'sprite')
        for pic_config in xml_sprite:
            x, y, w, h = tt.get_At(['x', 'y', 'w', 'h'], pic_config, int)
            n = tt.get_At('n', pic_config, str)
            crop_box = [x, y, x+w, y+h]
            save_name = n[:-4] + '.png'
            crop_pic = pic.crop(crop_box)
            crop_pic.save(save_name)
            shutil.move('./' + save_name, self.pic_path + save_name)
        self.load_part_pic()

    def render_ship(self, render_ship_name):
        self.load_ship_xml(render_ship_name)
        self.load_part_pic()
        for part in self.part_list:
            print(part)
            pass

test_class = ship_render()

test_class.save_part_config('PartList.xml')

# test_class.load_xml('PartList.xml')

"""
        {
            "part_to_png":[
                {"part":"part-1",
                "png":"png-1"},
                {"part":"part-2",
                "png":"png-2"}
            ]
        }
        {'part_to_png':[{'part':'part_name', 'png': 'png-1'}]}
"""
