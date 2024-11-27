from pico2d import *

class Character:
    def __init__(self, name, image_path, x, y):
        self.name = name
        self.image = load_image(image_path)
        self.x, self.y = x, y
        self.width, self.height = 50, 50
        self.state = "idle_down"
        self.frame = 0
        self.frame_speed = 0.2

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
            current_row = 2
        elif self.state == "idle_left" or self.state == "walk_left":
            current_row = 1
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
