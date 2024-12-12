from pico2d import *
import time
from projectile import Projectile

class Boss:
    def __init__(self, name, image_path, x, y, hp, atk, atk_speed):
        self.name = name
        self.image = image_path
        self.x, self.y = x, y
        self.width, self.height = 180, 180  # 보스는 캐릭터보다 크기가 큼
        self.max_hp = hp
        self.current_hp = hp
        self.atk = atk
        self.atk_speed = atk_speed
        self.is_dead = False
        self.state = "idle"
        self.frame = 0
        self.last_frame_time = time.time()  # 마지막 프레임 전환 시간을 기록
        self.frame_duration = 0.2  # 프레임이 전환되는 간격 (0.2초마다 프레임 전환)
        self.last_atk_time = 0
        self.projectiles = []  # 보스의 공격(투사체) 저장

    def update(self, chracters):
        """보스 상태 업데이트"""
        if self.is_dead:
            return

        current_time = time.time()
        if "idle" in self.state or "attack" in self.state:
            if current_time - self.last_frame_time > self.frame_duration:
                self.frame = (self.frame + 1) % 5
                self.last_frame_time = current_time  # 마지막 프레임 시간 갱신

        # 공격 처리
        current_time = time.time()


    def draw(self):
        """보스 그리기"""
        if self.is_dead:
            return  # 죽은 상태에서는 그리지 않음

        # 보스 이미지 그리기
        total_columns = 3
        frame_int = int(self.frame)
        frame_width = self.image.w // total_columns
        frame_height = self.image.h

        self.image.clip_draw(
            frame_width * frame_int, 0, frame_width, frame_height,
            self.x, self.y, self.width, self.height
        )

        # 체력 바 그리기
        self.draw_health_bar()

        # 투사체 그리기
        for projectile in self.projectiles:
            projectile.draw()

    def draw_health_bar(self):
        """보스 체력 바 그리기"""
        bar_width = 300
        bar_height = 10
        hp_ratio = self.current_hp / self.max_hp
        filled_width = int(bar_width * hp_ratio)
        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.height // 2 + 10

        # 체력 바의 배경 (회색)
        draw_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height)

        # 체력 바의 현재 체력 (빨간색)
        draw_rectangle(bar_x, bar_y, bar_x + filled_width, bar_y + bar_height)

    def receive_attack(self, damage):
        """보스가 공격을 받아 HP 감소"""
        if self.current_hp > 0:
            self.current_hp -= damage
            print(f"{self.name}이(가) {damage}의 피해를 입었습니다! (남은 체력: {self.current_hp})")
            if self.current_hp <= 0:
                self.current_hp = 0
                print(f"{self.name}이(가) 쓰러졌습니다!")
                self.die()


    def die(self):
        """보스 사망 처리"""
        self.is_dead = True
        print(f"{self.name}이(가) 처치되었습니다!")
