from pico2d import *
import scene_character, scene_select

class SceneMain:
    def __init__(self):
        self.image = load_image(f'resource/image/blue_sky.png')  # 메인 씬 이미지 로드
        self.adventure_button = load_image(f'resource/image/adventure_button.png')  # 모험 버튼 이미지 로드
        self.character_button = load_image(f'resource/image/charactor_choice_button.png')  # 캐릭터 선택 버튼 이미지 로드
        
        # 버튼 위치 및 크기 설정 (좌표 및 크기는 필요에 따라 조정)
        self.adventure_button_x, self.adventure_button_y = 100, 150
        self.character_button_x, self.character_button_y = 300, 150
        self.button_width, self.button_height = 100, 100  # 버튼의 가로세로 크기 설정

    def update(self):
        pass

    def draw(self):
        clear_canvas()  # 화면 지우기
        self.image.draw(200, 350, 400, 700)  # 이미지 그리기
        self.adventure_button.draw(self.adventure_button_x, self.adventure_button_y, self.button_width, self.button_height)  # 모험 버튼 그리기
        self.character_button.draw(self.character_button_x, self.character_button_y, self.button_width, self.button_height)  # 캐릭터 선택 버튼 그리기

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전 (캔버스 높이에 맞게)
            
            # 캐릭터 선택 버튼 클릭 감지
            if (self.character_button_x - self.button_width // 2 < x < self.character_button_x + self.button_width // 2 and
                self.character_button_y - self.button_height // 2 < y < self.character_button_y + self.button_height // 2):
                print("캐릭터 버튼 클릭됨")
                self.change_scene(scene_character.SceneCharacter())  # 캐릭터 씬으로 전환
                
            elif (self.adventure_button_x - self.button_width // 2 < x < self.adventure_button_x + self.button_width // 2 and
                self.adventure_button_y - self.button_height // 2 < y < self.adventure_button_y + self.button_height // 2):
                print("모험 버튼 클릭됨")
                self.change_scene(scene_select.SceneSelect())  # 선택 씬으로 전환 
                
        
        return self  # 기본적으로 현재 씬 유지