from pico2d import *
from character_class import Character
from scene_select_character import selected_characters

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

        for i, name in enumerate(selected_characters):
            image_path = f'resource/image/{name.lower()}.png'
            x = start_x + (i * x_offset)
            self.characters.append(Character(name, image_path, x, start_y))

        self.selected_ingame_character = None  # 선택된 캐릭터를 추적

    def update(self):
        if self.selected_ingame_character:
            self.selected_ingame_character.update()  # 선택된 캐릭터 애니메이션 업데이트

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
                # 클릭된 타일 위치에 캐릭터를 올바르게 이동
                for character in self.characters:
                    if character.x == grid_x * self.grid_size + self.grid_size // 2 and \
                       character.y == grid_y * self.grid_size + self.grid_size // 2 + 100:
                        # 선택된 캐릭터가 있으면 선택을 해제하고 새 캐릭터 선택
                        if self.selected_ingame_character == character:
                            self.selected_ingame_character = None  # 선택 해제
                        else:
                            self.selected_ingame_character = character  # 새 캐릭터 선택
                        return self  # 현재 씬 유지

                # 선택된 캐릭터가 있을 경우, 그 캐릭터를 이동시킴
                if self.selected_ingame_character:
                    # 타일에 해당하는 좌표로 이동
                    self.move_character(self.selected_ingame_character, grid_x, grid_y)

            return self  # 현재 씬 유지

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
