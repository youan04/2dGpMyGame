import global_state
import scene_ingame
from pico2d import *
import scene_main

def resource_path(relative_path):
    try:    
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SceneSelect:
    def __init__(self):
        self.image = load_image(resource_path('resource/image/map.png'))  # 선택 씬 이미지 로드
        self.buttons = [
            {"name": "dragon", "x": 100, "y": 575, "image": load_image(resource_path('resource/image/boss_dragon.png'))},
            #{"name": "demon", "x": 100, "y": 450, "image": load_image('resource/image/boss_demon.png')},
        ]
        self.home = load_image('resource/image/home.png')
        self.button_size = 250  # 버튼 크기

    def update(self):
        pass

    def draw(self):
        clear_canvas()  # 화면 지우기
        self.image.draw(200, 350, 400, 700)  # 이미지 그리기
        for button in self.buttons:
            self.draw_button(button)

    def draw_button(self, button):
        button["image"].clip_draw(
            0,
            int(button["image"].h / 24),  # 정수로 변환
            int(button["image"].w / 5),  # 정수로 변환
            int(button["image"].h / 24),  # 정수로 변환
            button["x"],
            button["y"],
            self.button_size,
            self.button_size,
        )
        self.home.draw(200, 100, 100, 100)

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사
        
    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전 (캔버스 높이에 맞게)
            for button in self.buttons:
                if button["x"] - self.button_size // 2 < x < button["x"] + self.button_size // 2 and \
                   button["y"] - self.button_size // 2 < y < button["y"] + self.button_size // 2:
                    global_state.selected_boss = button["name"]  # 선택된 보스 설정
                    global_state.current_scene = scene_ingame.SceneIngame()  # 씬 전환
                    
            home_button_x, home_button_y, home_button_width, home_button_height = 200, 100, 100, 100
        
            # 클릭된 좌표가 버튼 안에 있으면
            if home_button_x - 50 <= x <= home_button_x + 50 and \
                home_button_y - 50 <= y <= home_button_y + 50:
                self.change_scene(scene_main.SceneMain())  # 선택 씬으로 전환 
            
