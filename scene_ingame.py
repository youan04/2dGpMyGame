#scene_ingame.py

from pico2d import *
from character_class import Character
import global_state  # global_state.py 임포트


class SceneIngame:
    def __init__(self):
        self.image = load_image('resource/image/demon.png')
        self.tile = load_image('resource/image/stone_tile.png')
        self.board_size = 8
        self.grid_size = 50

        # 선택된 캐릭터를 기반으로 이미 global_state에서 캐릭터들이 존재하므로
        self.characters = global_state.selected_characters  # 이미 선택된 Character 객체를 그대로 사용
        start_x, start_y = 125, 225
        x_offset = self.grid_size

        # self.characters는 이미 Character 객체 리스트이므로, 별도로 추가할 필요 없음
        for i, character in enumerate(self.characters):  # global_state.selected_characters에서 직접 가져옴
            character.x = start_x + (i * x_offset)  # 캐릭터 위치 설정
            character.y = start_y  # y 좌표 설정

    def update(self):
        for character in self.characters:
            character.update()  # 각 캐릭터의 애니메이션 업데이트

    def draw(self):
        clear_canvas()
        self.image.draw(200, 350, 400, 700)  # 배경 이미지

        # 보드판 그리기
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.grid_size + self.grid_size // 2
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
            x, y = event.x, 700 - event.y
            grid_x = x // self.grid_size
            grid_y = (y - 100) // self.grid_size

            if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size:
                # 빈 땅인지 확인
                target_tile_empty = True
                clicked_character = None

                for character in self.characters:
                    if character.x == grid_x * self.grid_size + self.grid_size // 2 and \
                    character.y == grid_y * self.grid_size + self.grid_size // 2 + 100:
                        target_tile_empty = False
                        clicked_character = character
                        break

                # 선택된 캐릭터를 가져옴
                selected_character = None
                for character in self.characters:
                    if character.isSelected:
                        selected_character = character
                        break

                if selected_character:
                    if target_tile_empty:
                        # 빈 타일 클릭 시 선택된 캐릭터 이동
                        self.deselect_all_characters()
                        selected_character.move_to(grid_x, grid_y, self.grid_size, 100)
                    else:
                        # 다른 캐릭터 클릭 시 선택 캐릭터 변경
                        self.deselect_all_characters()
                        clicked_character.isSelected = True
                else:
                    # 선택된 캐릭터가 없는 경우, 클릭된 캐릭터 선택
                    if not target_tile_empty:
                        self.deselect_all_characters()
                        clicked_character.isSelected = True


    def deselect_all_characters(self):
        """모든 캐릭터의 선택 상태를 해제하는 함수"""
        for character in self.characters:
            character.isSelected = False

    
