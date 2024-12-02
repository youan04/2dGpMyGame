#character_calss.py
from pico2d import *

class Character:
    def __init__(self, name, image_path, x, y, attack, hp, speed):
        self.name = name
        self.image = image_path
        self.x, self.y = x, y
        self.width, self.height = 50, 50
        self.state = "idle_up"
        self.frame = 0
        self.frame_speed = 0.2
        self.isSelected = False  # 선택된 상태를 추적

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame = 0  # 상태 전환 시 프레임 초기화

    def update(self):
        if "walk" in self.state:
            self.frame = (self.frame + self.frame_speed) % 3
        else:
            self.frame = 0

    def draw(self):
        total_columns = 3
        total_rows = 4
        frame_int = int(self.frame)
        frame_width = self.image.w // total_columns
        frame_height = self.image.h // total_rows

        if self.state == "idle_down" or self.state == "walk_down":
            current_row = 3
        elif self.state == "idle_right" or self.state == "walk_right":
            current_row = 1
        elif self.state == "idle_left" or self.state == "walk_left":
            current_row = 2
        elif self.state == "idle_up" or self.state == "walk_up":
            current_row = 0

        if "idle" in self.state:
            current_column = 0
        else:
            current_column = frame_int

        self.image.clip_draw(
            frame_width * current_column,
            frame_height * current_row,
            frame_width,
            frame_height,
            self.x, self.y, self.width, self.height
        )

        # 선택된 캐릭터는 빨간색 테두리로 강조 표시
        if self.isSelected:
            draw_rectangle(self.x - 50//2, self.y - 50//2, self.x + 50//2, self.y + 50//2)  # 빨간 사각형 그리기
            
    def move_to(self, target_x, target_y, grid_size, y_offset):
        """캐릭터 이동 처리"""
        start_x, start_y = self.x // grid_size, (self.y - y_offset) // grid_size

        if target_x > start_x:
            self.set_state("walk_right")
        elif target_x < start_x:
            self.set_state("walk_left")
        elif target_y > start_y:
            self.set_state("walk_up")
        elif target_y < start_y:
            self.set_state("walk_down")

        # 이동 후 정지 상태로 전환
        self.x = target_x * grid_size + grid_size // 2
        self.y = target_y * grid_size + grid_size // 2 + y_offset
        self.set_state(f"idle_{self.state.split('_')[1]}")
