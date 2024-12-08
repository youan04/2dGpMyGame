# scene_select.py
from pico2d import *
class SceneSelect:
    def __init__(self):
        self.image = load_image(f'resource/image/map.png')  # 선택 씬 이미지 로드

        self.buttons = [
            {"name": "dragon", "x": 100, "y": 575, "image": load_image('resource/image/boss_dragon.png')},
            {"name": "demon", "x": 100, "y": 450, "image": load_image('resource/image/boss_demon.png')},
        ]
        self.button_size = 250  # 버튼 크기
        
    def update(self):
        pass

    def draw(self):
        clear_canvas()  # 화면 지우기
        self.image.draw(200, 350, 400, 700)  # 이미지 그리기
        for button in self.buttons:
            self.draw_button(button)
        
    def draw_button(self, button):
        self.buttons[0]["image"].clip_draw(
            0, 
            int(self.buttons[0]["image"].h / 24),  # 정수로 변환
            int(self.buttons[0]["image"].w / 5),      # 정수로 변환
            int(self.buttons[0]["image"].h / 24),      # 정수로 변환
            self.buttons[0]["x"], 
            self.buttons[0]["y"], 
            self.button_size, 
            self.button_size
        )

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사
        
    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전 (캔버스 높이에 맞게)
            
        return self  # 기본적으로 현재 씬 유지