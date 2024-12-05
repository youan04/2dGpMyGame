# boss_class.py

from pico2d import *
import time
from projectile import Projectile
from character_class import Character


class Boss(Character):
    def __init__(self, name, image_path, x, y, atk, atk_spd, hp, speed, special_attack_duration=5):
        super().__init__(name, image_path, x, y, None, atk, atk_spd, 0, hp, speed, False)
        self.special_attack_timer = 0  # 특수 공격 타이머
        self.special_attack_duration = special_attack_duration  # 특수 공격의 지속 시간
        self.special_attack_type = None  # 현재 발동한 특수 공격 종류
        self.special_attack_cooldown = 10  # 특수 공격 쿨타임
        self.last_special_attack_time = time.time()  # 마지막 특수 공격 시간
    
    def set_state(self, new_state):
        """보스의 상태를 설정 (특수 공격 준비 상태 등)"""
        super().set_state(new_state)
    
    def update(self, enemies):
        """보스 업데이트"""
        super().update(enemies)

        current_time = time.time()

        # 특수 공격 타이머 갱신
        if self.special_attack_type:
            if current_time - self.special_attack_timer >= self.special_attack_duration:
                self.special_attack_type = None  # 특수 공격 종료

        # 특수 공격 쿨타임을 고려하여 발동 가능 여부 확인
        if current_time - self.last_special_attack_time >= self.special_attack_cooldown:
            self.trigger_special_attack()

    def trigger_special_attack(self):
        """특수 공격을 트리거하는 메서드"""
        # 특수 공격 종류가 없다면 랜덤으로 선택
        if self.special_attack_type is None:
            self.special_attack_type = random.choice(["fireball", "laser", "summon_minions"])
            self.special_attack_timer = time.time()  # 특수 공격 타이머 시작
            self.last_special_attack_time = time.time()  # 특수 공격 시간 갱신

            print(f"{self.name}가 {self.special_attack_type} 특수 공격을 준비했습니다!")

    def perform_special_attack(self):
        """현재 설정된 특수 공격을 수행"""
        if self.special_attack_type == "fireball":
            self.fireball_attack()
        elif self.special_attack_type == "laser":
            self.laser_attack()
        elif self.special_attack_type == "summon_minions":
            self.summon_minions()

    def fireball_attack(self):
        """화염구 공격"""
        print(f"{self.name}가 화염구 공격을 발사합니다!")
        # 화염구 발사 로직을 구현 (적에게 피해를 주는 투사체 생성)
        # 예시로 한 방향으로 발사되는 화염구 생성
        direction_x = 1
        direction_y = 0
        projectile = Projectile(self.x, self.y, direction_x, direction_y, 1, 100, self.atk, "fireball", None)
        # 여기에 적들에 대한 피해 처리 추가

    def laser_attack(self):
        """레이저 공격"""
        print(f"{self.name}가 레이저 공격을 발사합니다!")
        # 레이저 공격 발사 로직을 구현 (장거리 공격)
        # 레이저 공격을 직선으로 발사하며 여러 적에게 피해를 주는 형태로 구현 가능
        pass

    def summon_minions(self):
        """미니언 소환"""
        print(f"{self.name}가 미니언을 소환합니다!")
        # 미니언 소환 로직 구현 (보스 주변에 미니언을 소환하여 적을 공격)
        pass

    def draw(self):
        """보스 캐릭터 그리기"""
        super().draw()  # 기본 캐릭터 그리기
        if self.special_attack_type:
            self.perform_special_attack()  # 특수 공격 수행

    def die(self):
        """보스 사망 처리"""
        super().die()
        print(f"{self.name}가 처치되었습니다!")
        # 보스 처치 시 처리 로직 (예: 보상 제공, 다음 단계로 넘어가기 등)
