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
        self.frame_speed = 1.0
        self.isSelected = False  # 선택된 상태를 추적
        self.target_x = self.x  # 이동 목표 x
        self.target_y = self.y  # 이동 목표 y
        self.speed = speed  # 이동 속도 (픽셀/frame)
        self.max_hp = hp  # 최대 체력
        self.current_hp = hp  # 현재 체력

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame = 0  # 상태 전환 시 프레임 초기화

    def update(self):
        # 프레임 업데이트
        if "walk" in self.state:
            self.frame = (self.frame + self.frame_speed) % 3
        else:
            self.frame = 0
        
        # 이동 처리
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5  # 남은 거리 계산

        if "walk" in self.state and distance > self.speed:  # 아직 도달하지 않았다면
            direction_x = dx / distance
            direction_y = dy / distance
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed
        else:
            # 목표 지점에 도달하면 정지 상태로 전환
            self.x = self.target_x
            self.y = self.target_y
            self.set_state(f"idle_{self.state.split('_')[1]}")
            
        

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
        
        # 체력바 그리기
        bar_width = 40
        bar_height = 5
        hp_ratio = self.current_hp / self.max_hp
        filled_width = int(bar_width * hp_ratio)
        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.height // 2 + 5

        # 체력 바의 배경 (회색)
        #draw_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height)

        # 체력 바의 현재 체력 (녹색)
        draw_rectangle(bar_x, bar_y, bar_x + filled_width, bar_y + bar_height)

        # 선택된 캐릭터는 빨간색 테두리로 강조 표시
        if self.isSelected:
            draw_rectangle(self.x - 50//2, self.y - 50//2, self.x + 50//2, self.y + 50//2)  # 빨간 사각형 그리기
            
    def move_to(self, target_x, target_y, grid_size, y_offset):
        """캐릭터 이동 목표 설정"""
        self.target_x = target_x * grid_size + grid_size // 2
        self.target_y = target_y * grid_size + grid_size // 2 + y_offset

        start_x, start_y = self.x // grid_size, (self.y - y_offset) // grid_size
        if target_x > start_x:
            self.set_state("walk_right")
        elif target_x < start_x:
            self.set_state("walk_left")
        elif target_y > start_y:
            self.set_state("walk_up")
        elif target_y < start_y:
            self.set_state("walk_down")


    def receive_attack(self, damage):
        """적으로부터 공격을 받아 HP 감소"""
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            print(f"{self.name}이(가) 쓰러졌습니다!")