from boss_class import Boss
from pico2d import *
import time
import random
from projectile import Projectile

# Boss 클래스를 상속받은 Dragon 클래스 정의
class Dragon(Boss):
    def __init__(self, name, image_path, x, y, hp, atk, atk_speed):
        # 부모 클래스의 초기화 함수 호출
        super().__init__(name, image_path, x, y, hp, atk, atk_speed)
        
        # 드래곤 특화 변수들
        self.last_skill_time = 0  # 마지막 스킬 사용 시간
        self.skill_cd = 20.0  # 스킬 사용 주기 (20초마다 사용)
        
        # 스킬 이미지 추가
        self.skill1_img = load_image("resource\image\magic_crush.png")  # 스킬1 이미지
        self.skill2_img = load_image("resource\image\magic_crush.png")  # 스킬2 이미지
        self.skill3_img = load_image("resource\image\magic_crush.png")  # 스킬3 이미지

    def update(self, enemies):
        """보스 상태 업데이트 및 드래곤 특화 행동"""
        super().update(enemies)  # 부모 클래스의 update 호출
        
        current_time = time.time()

        # 스킬 사용 주기 체크
        if current_time - self.last_skill_time >= self.skill_cd:
            self.use_random_skill()  # 무작위 스킬 사용
            self.last_skill_time = current_time

    def use_random_skill(self):
        """20초마다 랜덤으로 스킬 사용"""
        skill_choice = random.choice([1, 2, 3])  # 1, 2, 3 중 하나 선택

        if skill_choice == 1:
            self.use_skill1()
        elif skill_choice == 2:
            self.use_skill2()
        elif skill_choice == 3:
            self.use_skill3()

    def use_skill1(self):
        """스킬1 사용"""
        print(f"{self.name}이(가) 스킬1을 사용합니다!")
        self.skill1_img.draw(self.x, self.y + 50)

    def use_skill2(self):
        """스킬2 사용"""
        print(f"{self.name}이(가) 스킬2을 사용합니다!")
        self.skill2_img.draw(self.x, self.y + 100)

    def use_skill3(self):
        """스킬3 사용"""
        print(f"{self.name}이(가) 스킬3을 사용합니다!")
        self.skill3_img.draw(self.x, self.y + 150)

    def draw(self):
        """드래곤 그리기 (보스와 비슷하게 그리되, 드래곤의 특수 효과 추가)"""
        if self.is_dead:
            return  # 죽은 상태에서는 그리지 않음

        # 보스 이미지 그리기
        total_columns = 5
        frame_int = int(self.frame)
        frame_width = self.image.w // total_columns
        frame_height = self.image.h

        self.image.clip_draw(
            frame_width * frame_int+15, frame_height//24*3+20 , frame_width, frame_height//24,
            self.x, self.y, self.width, self.height
        )

        # 체력 바 그리기
        self.draw_health_bar()

        # 투사체 그리기
        for projectile in self.projectiles:
            projectile.draw()
    