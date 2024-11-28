from pico2d import *
from character_class import Character
import global_state  # global_state.py 임포트


class SceneIngame:
    def __init__(self):
        self.image = load_image('resource/image/demon.png')
        self.tile = load_image('resource/image/stone_tile.png')
        self.board_size = 8
        self.grid_size = 50

        # 선택된 캐릭터를 기반으로 생성
        self.characters = []
        start_x, start_y = 125, 225
        x_offset = self.grid_size

        for i, name in enumerate(global_state.selected_characters):  # global_state에서 가져옴
            image_path = f'resource/image/{name.lower()}.png'
            x = start_x + (i * x_offset)
            self.characters.append(Character(name, image_path, x, start_y))

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
            x, y = event.x, 700 - event.y  # y 좌표 반전

            # 타일의 왼쪽 상단 위치 기준으로 계산
            grid_x = (x // self.grid_size)
            grid_y = ((y - 100) // self.grid_size)  # 100은 타일의 시작 y 좌표로 오프셋 처리

            # 클릭된 좌표가 보드 내에 있는지 확인
            if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size:
                # 선택된 캐릭터가 있으면 이동
                selected_character = None
                for character in self.characters:
                    if character.isSelected:
                        selected_character = character
                        break

                if selected_character:
                    # 이동하기 전에 선택된 캐릭터 상태 해제
                    self.deselect_all_characters()  # 다른 캐릭터 선택을 위해 해제
                    self.move_character(selected_character, grid_x, grid_y)
                # 타일에 위치한 캐릭터 선택
                else:
                    for character in self.characters:
                        if character.x == grid_x * self.grid_size + self.grid_size // 2 and \
                           character.y == grid_y * self.grid_size + self.grid_size // 2 + 100:
                            # 기존 선택된 캐릭터는 선택 해제
                            self.deselect_all_characters()
                            # 새로 선택된 캐릭터는 선택 상태로 설정
                            character.isSelected = True
                            return self  # 새로 선택된 캐릭터로 갱신

            return self  # 현재 씬 유지

    def deselect_all_characters(self):
        """모든 캐릭터의 선택 상태를 해제하는 함수"""
        for character in self.characters:
            character.isSelected = False

    def move_character(self, character, target_x, target_y):
        """선택된 캐릭터를 상하좌우로 이동시키기 위한 함수"""
        start_x, start_y = character.x // self.grid_size, character.y // self.grid_size

        # 이동 방향에 맞는 상태로 설정
        if target_x > start_x:
            character.set_state("walk_right")
        elif target_x < start_x:
            character.set_state("walk_left")
        elif target_y > start_y:
            character.set_state("walk_down")
        elif target_y < start_y:
            character.set_state("walk_up")

        # 이동 애니메이션이 끝나면 정지 상태로 변경
        character.x = target_x * self.grid_size + self.grid_size // 2
        character.y = target_y * self.grid_size + self.grid_size // 2 + 100
        character.set_state(f"idle_{character.state.split('_')[1]}")  # 정지 상태로 변경
