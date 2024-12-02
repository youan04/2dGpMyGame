#enemy.py
from pico2d import *
class Enemy:
    def __init__(self, name, position, attack_power, attack_speed, health):
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
        self.health = health
        self.image = load_image('resource/image/little_dragon.png')  # 적 이미지
        self.width, self.height = 50, 50
        self.x = position[0] * 50 + 50 // 2
        self.y = position[1] * 50 + 50 // 2 + 100

    def attack(self, targets, delta_time):
        """
        인접 타일의 적을 공격.
        :param targets: 적들이 위치한 딕셔너리 {(x, y): Enemy}
        :param delta_time: 게임 루프에서 지난 시간 (초)
        """
        # 공격 타이머 업데이트
        self.attack_timer += delta_time
        attack_interval = 1 / self.attack_speed  # 공격 속도에 따른 간격 계산

        if self.attack_timer >= attack_interval:
            self.attack_timer -= attack_interval
            x, y = self.position

            # 상하좌우 좌표
            adjacent_positions = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

            for pos in adjacent_positions:
                if pos in targets:  # 타겟이 있는 경우
                    target = targets[pos]
                    print(f"{self.name}이 {target.name}을(를) 공격합니다! (공격력: {self.attack_power})")
                    target.take_damage(self.attack_power)

    def take_damage(self, damage):
        """
        적이 피해를 입었을 때 호출.
        :param damage: 받은 피해량
        """
        self.health -= damage
        print(f"{self.name}이(가) {damage}의 피해를 입었습니다! (남은 체력: {self.health})")
        
        if self.health <= 0:
            self.die()

    def die(self):
        """
        적이 사망했을 때 호출.
        """
        print(f"{self.name}이(가) 사망했습니다!")

    def move_to(self, new_position):
        """
        적의 위치 이동.
        :param new_position: 새로운 위치 (x, y)
        """
        print(f"{self.name}이 위치를 {self.position}에서 {new_position}(으)로 이동합니다.")
        self.position = new_position
        
    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)
