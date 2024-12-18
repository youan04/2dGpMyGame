#enemy.py
from pico2d import *
import time
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Enemy:
    def __init__(self, name, position, attack_power, attack_speed, hp):
        """
        Enemy 객체 초기화
        :param name: 적의 이름
        :param position: 현재 위치 (튜플로 표현: (x, y))
        :param attack_power: 공격력
        :param attack_speed: 초당 공격 횟수
        :param health: 체력
        """
        self.name = name
        self.position = position
        self.attack_power = attack_power
        self.attack_speed = attack_speed
        self.current_hp = hp
        self.max_hp = hp
        self.image = load_image(resource_path('resource/image/little_dragon.png'))  # 적 이미지
        self.width, self.height = 50, 50
        self.last_attack_time = 0  # 마지막 공격 시각
        self.x = position[0] * 50 + 50 // 2
        self.y = position[1] * 50 + 50 // 2 + 100
        
        self.is_dead = False  # 적이 살아 있는 상태
        
        self.base_y = self.y  # 기본 y 위치 저장
        self.is_shaking = False  # 흔들림 상태
        self.shake_start_time = 0  # 흔들림 시작 시간
        self.shake_duration = 0.2  # 흔들림 지속 시간
        self.shake_amplitude = 8  # 흔들림 강도

    def update(self, characters):
        """적의 상태 업데이트 및 공격"""
        current_time = time.time()
        
        # 흔들림 지속 시간이 지나면 흔들림 종료
        if self.is_shaking and current_time - self.shake_start_time > self.shake_duration:
            self.is_shaking = False
            self.y = self.base_y  # 원래 위치로 복원

        # 인접한 타일에 있는 캐릭터 찾기
        target_character = self.find_target(characters)
        if target_character:
            # 공격 속도에 따라 공격
            if current_time - self.last_attack_time >= 1 / self.attack_speed:
                self.nomal_attack(target_character)
                self.last_attack_time = current_time
            
        #사망 코드
        if self.is_dead:
            return "remove"  # 'remove' 신호를 반환
            return
    def find_target(self, characters):
        """인접한 타일에 있는 캐릭터 중 체력이 가장 높은 캐릭터 선택"""
        max_health = -1
        target_character = None

        for character in characters:
            dx = abs(character.x - (self.position[0] * 50 + 25))
            dy = abs(character.y - (self.position[1] * 50 + 125))
            if dx <= 50 and dy <= 50:  # 인접한 타일 (최대 거리 50픽셀 기준)
                if character.current_hp > max_health:
                    max_health = character.current_hp
                    target_character = character

        return target_character
    
    
                
    def nomal_attack(self, character):
        """캐릭터 공격"""
        
        if character:
            print(f"{self.name}가 {character.name}을(를) 공격합니다! (-{self.attack_power} HP)")
            character.receive_attack(self.attack_power)
            self.start_shaking()

            
    def receive_attack(self, damage):
        """적으로부터 공격을 받아 HP 감소"""
        if self.current_hp > 0:
            self.current_hp -= damage
            print(f"{self.name}이(가) {damage}의 피해를 입었습니다! (남은 체력: {self.current_hp})")
            if self.current_hp <= 0:
                self.current_hp = 0
                print(f"{self.name}이(가) 쓰러졌습니다!")
                self.die()
                
    def start_shaking(self):
        """흔들림 효과 시작"""
        self.is_shaking = True
        self.shake_start_time = time.time()

    def die(self):
        """
        적이 사망했을 때 호출.
        """
        self.is_dead = True
        print(f"{self.name}이(가) 사망했습니다!")

    def move_to(self, new_position):
        """
        적의 위치 이동.
        :param new_position: 새로운 위치 (x, y)
        """
        print(f"{self.name}이 위치를 {self.position}에서 {new_position}(으)로 이동합니다.")
        self.position = new_position
        
    def draw(self):
        """적을 화면에 그리기"""
        if self.is_shaking:
            elapsed_time = time.time() - self.shake_start_time
            # 흔들림 위치 계산: sin 함수로 위아래로 움직임
            self.y = self.base_y + self.shake_amplitude * (-1 if int(elapsed_time * 10) % 2 == 0 else 1)
        self.image.draw(self.x, self.y, self.width, self.height)
        
        
        # 체력바 그리기
        bar_width = 40
        bar_height = 5
        hp_ratio = self.current_hp / self.max_hp
        filled_width = int(bar_width * hp_ratio)
        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.height // 2 + 5

        draw_rectangle(bar_x, bar_y, bar_x + filled_width, bar_y + bar_height)
