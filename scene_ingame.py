from pico2d import *

class SceneIngame:
    def __init__(self):
        self.image = load_image(f'resource/image/demon.png')  # 게임 씬 이미지 로드
        self.tile = load_image(f'resource/image/stone_tile.png')  # 게임 씬 이미지 로드
        self.board_size = 8  # 8x8 보드 크기
        self.grid_size = 50  # 각 셀의 크기 (픽셀)
        
    def update(self):
        pass

    def draw(self):
        clear_canvas()  # 화면 지우기
        self.image.draw(200, 350, 400, 700)  # 이미지 그리기
        # 보드판 그리기
        for row in range(self.board_size):
            for col in range(self.board_size):
                # 각 타일을 그릴 위치 계산
                x = col * self.grid_size + self.grid_size // 2  # 타일의 중심을 맞추기 위해 이동
                y = row * self.grid_size + self.grid_size // 2+100
                self.tile.draw(x, y, self.grid_size, self.grid_size)

        # 배경 이미지와 타일 이미지 그리기 (기존 이미지)
        
        

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전 (캔버스 높이에 맞게)
            
        return self  # 기본적으로 현재 씬 유지
