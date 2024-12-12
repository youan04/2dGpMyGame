# character_object.py
from character_class import Character
from pico2d import *
import global_state 
from skill import Skill
import sys
import os

# 각 캐릭터 객체를 생성하고 관리

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_characters():
    characters = [
        Character("knight", 
                  load_image(resource_path('resource/image/knight.png')), 
                  125, 
                  225, 
                  load_image(resource_path('resource/image/knight_nomal_atk.png')), 
                  load_image(resource_path('resource/image/knight.png')),
                  load_image(resource_path('resource/image/yellow-shield.png')),
                  atk=25, atk_spd = 0.5, atk_length = 1, hp=500, speed=0.2, melee = True, skill_cool_down=12),
                  
        Character("archer", 
                  load_image(resource_path('resource/image/archer.png')), 
                  175, 
                  225, 
                  load_image(resource_path('resource/image/archer_nomal_atk.png')),
                  load_image(resource_path('resource/image/archer.png')), 
                  load_image(resource_path('resource/image/yellow-shield.png')),
                  atk=20, atk_spd = 0.7, atk_length = 7, hp=100, speed=0.4, melee = False, skill_cool_down=12),
        
        Character("mage", 
                  load_image(resource_path('resource/image/mage.png')), 
                  225, 
                  225, 
                  load_image(resource_path('resource/image/knight_nomal_atk.png')),
                  load_image(resource_path('resource/image/mage.png')), 
                  load_image(resource_path('resource/image/magic_ball.png')),
                  atk=40, atk_spd = 0.3, atk_length = 5, hp=200, speed=0.4, melee = False, skill_cool_down=5),
                  
        Character("priest", 
                  load_image(resource_path('resource/image/priest.png')),  
                  275,
                  225, 
                  load_image(resource_path('resource/image/knight_nomal_atk.png')),
                  load_image(resource_path('resource/image/priest.png')),
                  load_image(resource_path('resource/image/yellow-shield.png')),
                  atk=20, atk_spd = 0.7, atk_length = 3, hp=200, speed=0.3, melee = False, skill_cool_down=23),
                  
                  
        Character("guard", 
                  load_image(resource_path('resource/image/guard.png')),  
                  325, 
                  225, 
                  load_image(resource_path('resource/image/knight_nomal_atk.png')),
                  load_image(resource_path('resource/image/guard.png')),
                  load_image(resource_path('resource/image/yellow-shield.png')),
                  atk=20, atk_spd = 0.5, atk_length = 1,hp=1000, speed=0.1, melee = True, skill_cool_down=12),
                  
    ]
    return characters