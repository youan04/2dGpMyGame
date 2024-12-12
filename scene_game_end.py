# scene_game_end.py

from pico2d import *
import scene_main
from character_class import Character
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class SceneGameEnd:
    def __init__(self, result):
        self.image = load_image(resource_path('resource/image/map.png'))  # 선택 씬 이미지 로드
        self.result = result  # "Victory" 또는 "Defeat"
        self.font = load_font(resource_path('C:/Windows/Fonts/Consola.ttf'), 50)
        
    
    def update(self):
        pass

    def draw(self):
        clear_canvas()
        if self.result == "Victory":
            self.font.draw(100, 350, "Victory!", (0, 255, 0))
        elif self.result == "Defeat":
            self.font.draw(100, 350, "Defeat!", (255, 0, 0))
            
            self.font.draw(100, 450, "select your character", (0, 0, 0))
            self.font.draw(100, 400, "character", (0, 0, 0))
        update_canvas()

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사
        
    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전 (캔버스 높이에 맞게)
            self.change_scene(scene_main.SceneMain())
        return self  # 기본적으로 현재 씬 유지