#character_class.py

from pico2d import *
import time
from projectile import Projectile
from skill import Skill


class Character:
    def __init__(self, name, image_path, x, y, nomal_atk_img, skill_button_img, skill_img, atk, atk_spd, atk_length, hp, speed, melee, skill_cool_down):
        self.name = name
        self.image = image_path 
        self.x, self.y = x, y
        self.position = (x, y)
        self.width, self.height = 50, 50
        self.state = "idle_up"
        self.frame = 0
        self.frame_speed = 1.0
        self.isSelected = False  # 선택된 상태를 추적
        self.target_x = self.x  # 이동 목표 x
        self.target_y = self.y  # 이동 목표 y
        self.nomal_atk_img = nomal_atk_img
        self.speed = speed  # 이동 속도 (픽셀/frame)
        self.max_hp = hp  # 최대 체력
        self.current_hp = hp  # 현재 체력
        self.is_dead = False  # 사망 상태 추적
        self.respawn_timer_start = None  # 부활 타이머 시작 시간
        self.respawn_duration = 30  # 부활에 걸리는 시간 (초)
        self.defense = 0
        self.atk = atk
        self.atk_speed = atk_spd
        self.atk_length = atk_length
        self.melee = melee
        self.skill_button_img = skill_button_img
        self.last_atk_time = 0
        
        self.is_using_skill = False  # 스킬 사용 여부
        self.skill_img = skill_img
        self.skill_start_time = None  # 스킬 발동 시간
        self.skill_effect_time = None
        self.skill_current_time = skill_cool_down
        self.skill_cool_down = skill_cool_down
        self.last_skill_time = 0  # last_skill_time을 0 또는 적절한 초기값으로 설정
        self.skill_duration = 5  # 스킬 지속 시간 (초)
        self.original_atk_spd = atk_spd  # 기본 공격 속도
        self.atk_spd = atk_spd  # 현재 공격 속도
        
        self.projectiles = []  # <--- 이 줄을 추가하여 투사체 리스트를 초기화합니다.
        
        self.skill_sound = load_music('resource/sound/skill_sound.wav')  # BGM 파일 로드
        self.skill_sound.set_volume(40)  # 볼륨 설정 (0~128)

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame = 0  # 상태 전환 시 프레임 초기화

    def update(self, enemies, boss):
        # 프레임 업데이트
        if "walk" in self.state:
            self.frame = (self.frame + self.frame_speed) % 3
        else:
            self.frame = 0

        if self.is_dead:
            # 부활 대기 중이라면 시간 확인
            if time.time() - self.respawn_timer_start >= self.respawn_duration:
                self.respawn()
            return

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
        
        # 적 탐색 및 공격
        if "idle" in self.state:
            current_time = time.time()
            if current_time - self.last_atk_time >= 1 / self.atk_speed:
                        self.normal_attack()
                        self.last_atk_time = current_time            
        
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.is_out_of_range():  # 범위를 벗어난 투사체는 제거
                self.projectiles.remove(projectile)
                
                
        for projectile in self.projectiles[:]:  # 투사체 리스트에서 복사본을 사용하여 중간에 삭제해도 문제가 없도록
            for enemy in enemies:
                if projectile.check_collision(enemy):  # 충돌 발생
                    enemy.receive_attack(projectile.damage)  # 적에게 피해를 주고
                    self.projectiles.remove(projectile)  # 투사체 제거
                    break  # 충돌한 첫 번째 적만 처리하고 투사체를 삭제한 후 더 이상 확인하지 않음
                
            if projectile.check_collision(boss):  # 충돌 발생
                boss.receive_attack(projectile.damage)  # 보스에게 피해를 주고
                self.projectiles.remove(projectile)  # 투사체 제거
                break
                # 충돌한 첫 번째 적만 처리하고 투사체를 삭제한 후 더 이상 확인하지 않음
                
                 
        
     
            
                    

    def draw(self):
        if self.is_dead:
            # 사망 상태에서는 부활 게이지 표시
            self.draw_respawn_gauge()
            return

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

        self.calculate_cooldown()  # 남은 쿨타임 계산
        
        if self.name == "knight" and self.skill_effect_time and time.time() - self.skill_effect_time >= 5:
            self.atk_speed /= 2  # 공격속도 원래대로 복구
            self.skill_effect_time = 0
            self.is_using_skill = False
            print(f"{self.name}의 스킬이 종료되었습니다. 공격속도가 원래대로 돌아갔습니다.")
            
        elif self.name == "archer" and self.skill_effect_time and time.time() - self.skill_effect_time >= 5:
            self.atk_speed /= 2  # 공격속도 원래대로 복구
            self.skill_effect_time = 0
            self.is_using_skill = False
            print(f"{self.name}의 스킬이 종료되었습니다. 공격속도가 원래대로 돌아갔습니다.")

        elif self.name == "guard" and self.skill_effect_time and time.time() - self.skill_effect_time >= 5:
            self.defense = self.base_defense  # 방어력 원래대로 복구
            self.skill_effect_time = 0
            self.is_using_skill = False
            print(f"{self.name}의 스킬이 종료되었습니다. 방어력이 원래대로 돌아갔습니다.")
            
            
        if self.name == "guard" and self.is_using_skill == True:
            self.skill_img.draw(self.x, self.y, 30, 30)  # 캐릭터 위에 방패 표시
            
        if self.name == "knight" and self.is_using_skill == True:
            self.skill_img.draw(self.x, self.y-20, 50, 10)  # 캐릭터 위에 방패 표시
            
        # 체력바 그리기
        self.draw_health_bar()
        
        for projectile in self.projectiles:
            projectile.draw()


        # 선택된 캐릭터는 빨간색 테두리로 강조 표시
        if self.isSelected:
            draw_rectangle(self.x - self.width // 2, self.y - self.height // 2,
                           self.x + self.width // 2, self.y + self.height // 2)  # 빨간 사각형 그리기

    def draw_health_bar(self):
        """체력바 그리기"""
        bar_width = 40
        bar_height = 5
        hp_ratio = self.current_hp / self.max_hp
        filled_width = int(bar_width * hp_ratio)
        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.height // 2 + 5

        # 체력 바의 현재 체력 (녹색)
        draw_rectangle(bar_x, bar_y, bar_x + filled_width, bar_y + bar_height)
        
        
    def draw_skill_button(self, button_x_start, button_y, button_width, button_height):
        self.skill_button_img.clip_draw(self.image.w // 3*1 ,self.image.h // 4*3,self.image.w // 3,self.image.h // 3,button_x_start, button_y, button_width, button_height)
        
        


    def draw_respawn_gauge(self):
        """부활 게이지 표시"""
        gauge_width = 50
        gauge_height = 10
        elapsed_time = time.time() - self.respawn_timer_start
        fill_ratio = elapsed_time / self.respawn_duration
        filled_width = int(gauge_width * fill_ratio)

        gauge_x = self.x - gauge_width // 2
        gauge_y = self.y

        # 게이지 배경 (회색)
        draw_rectangle(gauge_x, gauge_y, gauge_x + gauge_width, gauge_y + gauge_height)

        # 현재 게이지 상태 (노란색)
        draw_rectangle(gauge_x, gauge_y, gauge_x + filled_width, gauge_y + gauge_height)

    def move_to(self, target_x, target_y, grid_size, y_offset):
        """캐릭터 이동 목표 설정"""
        if self.is_dead:
            return  # 사망 상태에서는 이동 불가

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
        """적으로부터 공격을 받아 HP 감소 (방어력 적용)"""
        if self.current_hp > 0:
            # 방어력에 따른 데미지 감소 (50% 방어력인 경우, 데미지 절반)
            reduced_damage = damage * (1 - self.defense / 100)

            # 실제 데미지가 0 이하로 내려가지 않도록 보정
            if reduced_damage < 0:
                reduced_damage = 0

            self.current_hp -= reduced_damage
            print(f"{self.name}이(가) {reduced_damage:.2f}의 피해를 입었습니다! (남은 체력: {self.current_hp})")
            
            if self.current_hp <= 0:
                self.current_hp = 0
                print(f"{self.name}이(가) 쓰러졌습니다!")
                self.die()
                
    def normal_attack(self):
        """투사체를 생성하여 발사"""
        current_time = time.time()
        if current_time - self.last_atk_time < 1 / self.atk_speed:
            return  # 공격 속도에 맞춰 공격을 제한

        # 투사체의 방향 설정
        if "right" in self.state:
            direction_x = 1
            direction_y = 0
        elif "left" in self.state:
            direction_x = -1
            direction_y = 0
        elif "up" in self.state:
            direction_x = 0
            direction_y = 1
        elif "down" in self.state:
            direction_x = 0
            direction_y = -1

        # 투사체 생성 (현재 위치에서 방향, 속도, 범위 등 설정)
        projectile = Projectile(self.x, self.y, direction_x, direction_y, 2, self.atk_length, self.atk, self.state, self.nomal_atk_img)
        self.projectiles.append(projectile)
        
        self.last_atk_time = current_time  # 공격한 시간 갱신

            
    # def find_target(self, enemies):
    #     """인접한 타일에 있는 적 중 체력이 가장 낮은 적 선택"""
    #     min_distance = float('inf')
    #     target_enemy = None

    #     for enemy in enemies:
    #         dx = abs(enemy.x - self.x)
    #         dy = abs(enemy.y - self.y)
    #         distance = (dx ** 2 + dy ** 2) ** 0.5
    #         if distance <= 50 and enemy.current_hp > 0:  # 공격 가능한 범위 내
    #             if distance < min_distance:
    #                 min_distance = distance
    #                 target_enemy = enemy

    #     return target_enemy
    
    def use_skill(self, target=None):
        """스킬 발동"""
        if self.is_dead:
            print(f"{self.name}은(는) 사망 상태에서 스킬을 사용할 수 없습니다.")
            return

        self.skill_current_time = time.time()
        
        if self.skill_current_time - self.last_skill_time < self.skill_cool_down:
            print(f"스킬은 아직 쿨타임 중입니다. 남은 시간: {int(self.skill_cool_down - (self.skill_current_time - self.last_skill_time))}초")
            return

        self.is_using_skill = True
        self.last_skill_time = self.skill_current_time
        
        print(f"{self.name}이(가) 스킬을 사용했습니다!")
 
        # 캐릭터 이름에 따라 스킬 효과 다르게 적용
        if self.name == "knight":
            self.knight_skill()
        elif self.name == "archer":
            self.archer_skill()
        elif self.name == "mage":
            self.mage_skill()
        elif self.name == "priest":
            self.priest_skill(target)
        elif self.name == "guard":
            self.guard_skill()

        

        
    def knight_skill(self):
        """기사 스킬: 5초 동안 공격속도 100% 증가"""
        self.atk_speed *= 2  # 공격속도 두 배 증가
        self.skill_effect_time = time.time()  # 스킬 효과 발동 시간 기록
        #self.skill_sound.play(1)
        print(f"{self.name}의 스킬 발동! 5초 동안 공격속도 100% 증가!")
        
    def guard_skill(self):
        """수호자 스킬: 5초 동안 방어력 50 증가"""
        self.base_defense = self.defense  # 기존 방어력 백업
        self.defense += 50  # 방어력 50 증가
        
        self.skill_effect_time = time.time()  # 스킬 효과 발동 시간 기록
       # self.skill_sound.play(1)
        print(f"{self.name}의 스킬 발동! 5초 동안 방어력 50 증가!")
        
    def archer_skill(self):
        """궁수 스킬: 5초 동안 공격속도 100% 증가"""
        self.atk_speed *= 2  # 공격속도 두 배 증가
        self.skill_effect_time = time.time()  # 스킬 효과 발동 시간 기록
        #self.skill_sound.play(1)
        print(f"{self.name}의 스킬 발동! 5초 동안 공격속도 100% 증가!")
        
    def mage_skill(self):
        """마법사 스킬: 거대한 투사체"""
        
        # 마법사 스킬 발사 (큰 투사체 발사)
        direction_x, direction_y = 0, 0
        if "right" in self.state:
            direction_x = 1
        elif "left" in self.state:
            direction_x = -1
        elif "up" in self.state:
            direction_y = 1
        elif "down" in self.state:
            direction_y = -1

        # 큰 투사체 생성
        projectile = Projectile(self.x, self.y, direction_x, direction_y, 1, 200, self.atk * 2, self.state, self.skill_img, 70, 70)  # 데미지가 두 배인 큰 투사체
        self.projectiles.append(projectile)
        self.is_using_skill = False
        #self.skill_sound.play(1)
        print(f"{self.name}의 스킬이 발동되어 큰 투사체를 발사했습니다!")
        
    def priest_skill(self, allies):
        """프리스트 스킬: 모든 아군의 체력 100 회복"""
        healing_amount = 200
        for ally in allies:
            if ally.current_hp < ally.max_hp and ally.is_dead == False:  # 아군의 체력이 최대 체력보다 낮으면
                ally.current_hp += healing_amount
                if ally.current_hp > ally.max_hp:  # 체력이 최대치를 초과하지 않도록 제한
                    ally.current_hp = ally.max_hp
                    
                print(f"{ally.name}의 체력이 {healing_amount}만큼 회복되었습니다. 현재 체력: {ally.current_hp}")
            else:
                print(f"{ally.name}의 체력은 이미 최대입니다!")
                
        #self.skill_sound.play(1)
        self.is_using_skill = False
                
    def calculate_cooldown(self):
        """남은 스킬 쿨타임 계산"""
        self.skill_current_time = time.time()
        self.remaining_cooldown = max(0, self.skill_cool_down - (self.skill_current_time - self.last_skill_time))
        
    def die(self):
        """캐릭터 사망 처리"""
        self.is_dead = True
        self.respawn_timer_start = time.time()  # 부활 타이머 시작
        self.current_hp = 0  # 체력 0으로 설정

    def respawn(self):
        """캐릭터 부활"""
        print(f"{self.name}이(가) 부활했습니다!")
        self.is_dead = False
        self.current_hp = self.max_hp // 2  # 체력의 50%로 부활
