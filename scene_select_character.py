from pico2d import *
import global_state  # global_state.py 파일 임포트

class SceneCharacter:
    def __init__(self):
        # 캐릭터 씬 이미지 로드
        self.image = load_image('resource/image/door.png')  
        self.knight_button = load_image('resource/image/knight.png')
        self.archer_button = load_image('resource/image/archer.png')
        self.mage_button = load_image('resource/image/mage.png')
        self.priest_button = load_image('resource/image/priest.png')
        self.guard_button = load_image('resource/image/guard.png')

        # 버튼 위치와 크기
        self.buttons = [
            {"name": "Knight", "x": 75, "y": 575, "image": self.knight_button},
            {"name": "Archer", "x": 200, "y": 575, "image": self.archer_button},
            {"name": "Mage", "x": 75, "y": 450, "image": self.mage_button},
            {"name": "Priest", "x": 200, "y": 450, "image": self.priest_button},
            {"name": "Guard", "x": 325, "y": 575, "image": self.guard_button},
        ]
        self.button_size = 125  # 버튼 크기

    def update(self):
        pass
    
    def draw_button(self, button):
        """버튼을 그리면서 선택 여부에 따라 테두리를 표시"""
        if button["name"] in global_state.selected_characters:
            # 선택된 버튼은 빨간색 테두리를 그림
            draw_rectangle(button["x"] - self.button_size // 2, 
                           button["y"] - self.button_size // 2, 
                           button["x"] + self.button_size // 2, 
                           button["y"] + self.button_size // 2)
        
        # 버튼 이미지를 그림
        button["image"].clip_draw(
            0, 
            int(button["image"].h / 4 * 3),  # 정수로 변환
            int(button["image"].w / 3),      # 정수로 변환
            int(button["image"].h / 4),      # 정수로 변환
            button["x"], 
            button["y"], 
            self.button_size, 
            self.button_size
        )

    def draw(self):
        clear_canvas()
        self.image.draw(200, 350, 400, 700)  # 배경 이미지 그리기
        for button in self.buttons:
            self.draw_button(button)
            
    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전
            for button in self.buttons:
                bx, by = button["x"], button["y"]
                # 버튼 클릭 여부 확인
                if (bx - self.button_size // 2 <= x <= bx + self.button_size // 2 and
                        by - self.button_size // 2 <= y <= by + self.button_size // 2):
                    if button["name"] in global_state.selected_characters:
                        # 이미 선택된 캐릭터라면 배열에서 제거
                        global_state.selected_characters.remove(button["name"])
                    else:
                        # 선택 가능한 공간이 있다면 배열에 추가
                        if len(global_state.selected_characters) < 4:
                            global_state.selected_characters.append(button["name"])
                        else:
                            print("선택 가능한 캐릭터는 최대 4명입니다!")
                    break
