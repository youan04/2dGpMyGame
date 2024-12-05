# character_object.py
from character_class import Character
from pico2d import *
import global_state 

# 각 캐릭터 객체를 생성하고 관리
def create_characters():
    characters = [
        Character("knight", load_image('resource/image/knight.png'), 125, 225, load_image('resource/image/knight_atk.png'), atk=20, atk_spd = 0.5, hp=500, speed=0.2, melee = True),
        Character("archer", load_image('resource/image/archer.png'), 175, 225, load_image('resource/image/knight_atk.png'), atk=20, atk_spd = 0.5,hp=300, speed=0.4, melee = False),
        Character("mage", load_image('resource/image/mage.png'), 225, 225, load_image('resource/image/knight_atk.png'), atk=30, atk_spd = 0.5,hp=300, speed=0.4, melee = False),
        Character("priest", load_image('resource/image/priest.png'), 275, 225, load_image('resource/image/knight_atk.png'),atk=10, atk_spd = 0.5,hp=300, speed=0.3, melee = False),
        Character("guard", load_image('resource/image/guard.png'), 325, 225, load_image('resource/image/knight_atk.png'),atk=10, atk_spd = 0.5,hp=1000, speed=0.1, melee = True)
    ]
    return characters