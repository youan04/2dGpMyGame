from boss_class import Boss
from pico2d import *
import time
from projectile import Projectile

import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Boss 클래스를 상속받은 Dragon 클래스 정의
class Dragon(Boss):
    def __init__(self, name, image_path, x, y, hp, atk, atk_speed):
        super().__init__(name, image_path, x, y, hp, atk, atk_speed)
        self.last_skill_time = 0  # 마지막 스킬 사용 시간
        self.skill_cd = 20.0  # 스킬 사용 주기 (4초마다 사용)
        self.skill1_img = load_image(resource_path("resource/image/fireball1.png"))  # 파이어볼 이미지
        #self.danger_img = load_image(resource_path("resource/image/danger.png"))  # 위험 영역 이미지
        self.skill1_active = False  # 파이어볼 공격 활성화 체크
        self.skill1_time_left = 0  # 파이어볼 공격의 남은 시간
        self.skill1_target_tiles = []  # 발톱 공격의 대상이 되는 타일들
        self.projectiles = []  # 발사된 파이어볼들을 담을 리스트
        self.first_skill = True
        
    def update(self, characters):
        super().update(characters)  # 부모 클래스의 update 호출
        current_time = time.time()

        # 스킬 사용 주기 체크
        if current_time - self.last_skill_time >= self.skill_cd and self.first_skill == False:
            self.use_skill1()  
            self.last_skill_time = current_time
        elif current_time - self.last_skill_time >= self.skill_cd and self.first_skill == True:
            self.first_skill = False
            self.last_skill_time = current_time

        # 파이어볼 업데이트
        for projectile in self.projectiles:
            projectile.update()  # 파이어볼의 위치를 업데이트
            if projectile.is_out_of_range():  # 범위를 벗어나면 제거
                self.projectiles.remove(projectile)

            # 충돌 체크
            for character in characters:
                if character.is_dead == False and projectile.check_collision(character) :
                    character.receive_attack(self.atk)
                    self.projectiles.remove(projectile)
                    break  # 충돌한 파이어볼은 제거

    def use_skill1(self):
        """파이어볼 스킬 사용"""
        print(f"{self.name}이(가) 파이어볼 스킬을 사용합니다!")

        # 파이어볼 8개를 (50, 800)부터 발사
        for i in range(8):
            x = 25+i * 50  # x 좌표는 50씩 증가
            y =550  # y 좌표는 고정
            direction = "idle_down"  # 파이어볼은 아래로 날아감
            projectile = Projectile(x, y, 0, -1, 0.2, 800, self.atk, direction, self.skill1_img)
            self.projectiles.append(projectile)  # 리스트에 추가

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
            frame_width * frame_int + 15, frame_height // 24 * 3 + 20, frame_width, frame_height // 24,
            self.x, self.y, self.width, self.height
        )

        # 체력 바 그리기
        self.draw_health_bar()

        # 투사체 그리기 (파이어볼을 그리기)
        for projectile in self.projectiles:
            projectile.draw()  # 각 파이어볼을 화면에 그린다

