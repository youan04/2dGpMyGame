# character_object.py
from character_class import Character
from pico2d import *
import global_state 

# 각 캐릭터 객체를 생성하고 관리
def create_characters():
    characters = [
        Character("knight", load_image('resource/image/knight.png'), 125, 225, attack=10, hp=5, speed=0.2),
        Character("archer", load_image('resource/image/archer.png'), 175, 225, attack=8, hp=4, speed=0.4),
        Character("mage", load_image('resource/image/mage.png'), 225, 225, attack=12, hp=2, speed=0.4),
        Character("priest", load_image('resource/image/priest.png'), 275, 225, attack=6, hp=8, speed=0.3),
        Character("guard", load_image('resource/image/guard.png'), 325, 225, attack=7, hp=10, speed=0.1)
    ]
    return characters