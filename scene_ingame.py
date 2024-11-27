from pico2d import *
from character_class import Character  # 캐릭터 클래스 임포트
from scene_select_character import selected_characters  # 선택된 캐릭터 배열 가져오기

class SceneIngame:
    def __init__(self):
        self.image = load_image('resource/image/demon.png')  # 게임 씬 배경 이미지
        self.tile = load_image('resource/image/stone_tile.png')  # 게임 보드 타일 이미지
        self.board_size = 8  # 8x8 보드 크기
        self.grid_size = 50  # 각 셀의 크기 (픽셀)

        # 선택된 캐릭터를 기반으로 생성
        self.characters = []
        start_x, start_y = 100, 200  # 캐릭터 배치 시작 위치
        x_offset = 50  # 캐릭터 간 간격

        for i, name in enumerate(selected_characters):
            image_path = f'resource/image/{name.lower()}.png'  # 이름에 따라 이미지 경로 설정
            x = start_x + (i * x_offset)  # x 좌표는 간격을 고려하여 설정
            self.characters.append(Character(name, image_path, x, start_y))  # 캐릭터 생성

    def update(self):
        for character in self.characters:
            character.update()  # 각 캐릭터 업데이트 (애니메이션 등)

    def draw(self):
        clear_canvas()  # 화면 지우기
        self.image.draw(200, 350, 400, 700)  # 배경 이미지 그리기

        # 보드판 그리기
        for row in range(self.board_size):
            for col in range(self.board_size):
                # 각 타일을 그릴 위치 계산
                x = col * self.grid_size + self.grid_size // 2  # 타일 중심 위치
                y = row * self.grid_size + self.grid_size // 2 + 100
                self.tile.draw(x, y, self.grid_size, self.grid_size)

        # 선택된 캐릭터 그리기
        for character in self.characters:
            character.draw()

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전
            grid_x = (x - self.grid_size // 2) // self.grid_size
            grid_y = (y - 100 - self.grid_size // 2) // self.grid_size

            # 클릭된 좌표가 보드 내에 있는지 확인
            if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size:
                for character in self.characters:
                    character.x = grid_x * self.grid_size + self.grid_size // 2
                    character.y = grid_y * self.grid_size + self.grid_size // 2 + 100

        return self  # 현재 씬 유지
