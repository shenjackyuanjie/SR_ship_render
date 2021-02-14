"""
by shenjack(shenjackyuanjie)
"""

import os
import xml
import math
import json
import shutil
import random
from PIL import Image
import xml.dom.minidom
# from main import tools as tt
from xml.dom.minidom import parse
# --------------可修改变量------------------
ship_pic_filename = 'ShipSprites.png'
ship_pic_config = 'ShipSprites.xml'
output_pic_size = [1024, 1024]
output_pic_color = 'white'
render_ship_name = 'test.xml'
# --------------可修改变量结束--------------


class ship_render():

    def __init__(self, render_size=[1024, 1024], render_color='red'):
        self.pic_path = './pic_storage/'
        self.part_config_path = '/part_config.json'
        self.part_list_path = '/PartList.xml'
        self.main_path = './main/'
        self.render_center = [render_size[0] // 2, render_size[1] // 2]
        self.part_pics = {}
        self.part_list = []
        self.part_config = {}
        self.render_pic = Image.new('RGBA', render_size, render_color)
        self.SR_pi = 3.141593

    def save_part_config(self):
        save_dic = {'part_png': {}, 'part_size': {}}

        partlist_path = self.main_path + self.part_list_path
        part_list = tt.load_xml(partlist_path, getEBTN='PartType')
        for part_config in part_list:
            part_id, sprite = tt.get_At(['id', 'sprite'], part_config)
            w, h = tt.get_At(['width', 'height'], part_config, int)
            part_size = {'width': w, 'height': h}
            save_dic['part_size'][part_id] = part_size
            save_dic['part_png'][part_id] = sprite
        save_path = self.main_path + self.part_config_path
        print(save_path, 'saveing')
        with open(save_path, mode='w') as part_config_json:
            json.dump(save_dic, part_config_json)

    def load_part_config(self):
        open_path = self.main_path + self.part_config_path
        try:
            with open(open_path, mode='r') as parts:
                part_config = json.load(parts)
                self.part_config = part_config
        except FileNotFoundError:
            self.save_part_config()
            self.load_part_config()

    def load_part_pic(self):
        pics = os.listdir(self.pic_path)
        for pic in pics:
            part_pic = Image.open(self.pic_path + pic)
            pic_name = pic[:-4]
            self.part_pics[pic_name] = part_pic

    def load_ship_xml(self, ship_xml_name):
        ship_xml = tt.load_xml(ship_xml_name, 'Part')
        for part in ship_xml:
            x, y = tt.get_At(['x', 'y'], part, float)
            x, y = int(x), int(y)
            t = tt.get_At('angle', part, float)
            PT = tt.get_At('partType', part, str)
            part_config = {'x': x, 'y': y, 'part_id': PT, 'turn': t}
            print(part_config)
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
        self.load_part_config()
        for part in self.part_list:
            png = self.part_config['part_png'][part['part_id']][:-4]
            pic_pic = self.part_pics[png]
            w, h = pic_pic.size
            pic_c = [int(self.render_center[0]), int(self.render_center[1])]
            turn = part['turn']
            paste_box = [pic_c[0], pic_c[1], pic_c[0], pic_c[1]]
            part['x'], part['y'] = part['x'] * 60, part['y'] * 60
            paste_box = [part['x'] + pic_c[0], part['y'] + pic_c[1],
                         part['x'] + w + pic_c[0], part['y'] + h + pic_c[1]]
            if turn == 0.0:
                print('no turn ', end=' paste_box ')
            elif turn == 1.570796:
                pic_pic = pic_pic.rotate(90)
                print('turn 90 ', end=' paste_box ')    
            elif turn == 3.141593:
                pic_pic = pic_pic.rotate(180)
                print('turn 180', end=' paste_box ')
            elif turn == 4.712389:
                pic_pic = pic_pic.rotate(270)
                print('turn 270', end=' paste_box ')
            print(paste_box)
            self.render_pic.paste(pic_pic, paste_box)  
        self.render_pic.save('render.png')
        self.render_pic.show()


test_class = ship_render()

# test_class.save_part_config()

# test_class.render_ship('test.xml')

# test_class.load_xml('PartList.xml')

"""
{
    "part_png":{
        'part_id': 'part_1'
    }
}
{'part_png':[{'part': 'png-1'}]}
"""
