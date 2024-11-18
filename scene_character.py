from pico2d import *
class SceneCharacter:
    def __init__(self):
        self.image = load_image('door.png')  # 캐릭터 씬 이미지 로드

    def update(self):
        pass

    def draw(self):
        clear_canvas()  # 화면 지우기
        self.image.draw(200, 350, 400, 700)  # 이미지 그리기

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사
        
        
    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전 (캔버스 높이에 맞게)
            
        return self  # 기본적으로 현재 씬 유지
            
    
            