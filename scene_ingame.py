#scene_ingame.py

from pico2d import *
from character_class import Character
import global_state  # global_state.py 임포트
import random
import time
from enemy import Enemy
import scene_game_end
from boss_class import Boss
from boss_dragon import Dragon  # Dragon 클래스를 임포트

class SceneIngame:
    def __init__(self):
        self.image = load_image('resource/image/boss_demon.png')
        self.tile = load_image('resource/image/stone_tile.png')
        self.font = load_font('C:/Windows/Fonts/Consola.ttf', 30)
        self.board_size = 8
        self.grid_size = 50
        
        self.start_time = time.time()  # 시작 시간
        self.time_limit = 180  # 제한 시간 (초)

        # 선택된 캐릭터를 기반으로 이미 global_state에서 캐릭터들이 존재하므로
        self.characters = global_state.selected_characters  # 이미 선택된 Character 객체를 그대로 사용
        start_x, start_y = 125, 225
        x_offset = self.grid_size

        # self.characters는 이미 Character 객체 리스트이므로, 별도로 추가할 필요 없음
        for i, character in enumerate(self.characters):  # global_state.selected_characters에서 직접 가져옴
            character.x = start_x + (i * x_offset)  # 캐릭터 위치 설정
            character.y = start_y  # y 좌표 설정
            character.target_x = character.x  # 목표 좌표도 초기화
            character.target_y = character.y  # 목표 좌표도 초기화
            character.set_state("idle_up")  # 초기 상태 설정
            character.is_dead = False
            character.current_hp = character.max_hp
            
        self.enemies = []  # 적 객체 리스트
        self.last_enemy_spawn_time = time.time()  # 마지막 적 생성 시간
        self.enemy_spawn_interval = 8  # 적 생성 간격 (초)
        
        self.spawn_boss()


    def update(self):
        #적 스폰
        current_time = time.time()
        elapsed_time = current_time - self.start_time  # 경과 시간
        remaining_time = self.time_limit - elapsed_time  # 남은 시간 계산
        
        if remaining_time <= 0:
            self.change_scene(scene_game_end.SceneGameEnd())  # 타이머가 끝나면 게임 종료 씬으로 변경

            
        if current_time - self.last_enemy_spawn_time >= self.enemy_spawn_interval:
            self.spawn_enemy()
            self.last_enemy_spawn_time = current_time
            
        for character in self.characters:
            character.update(self.enemies, self.boss)  # 각 캐릭터의 애니메이션 업데이트
            
        for enemy in self.enemies[:]:
            result = enemy.update(self.characters)
            if result == "remove":  # 적이 제거 대상이면
                self.enemies.remove(enemy)  # 리스트에서 제거
                
        if hasattr(self, 'boss'):  # 보스가 생성되었으면 업데이트
            self.boss.update(self.characters)
                

    def draw(self):
        clear_canvas()
        self.image.draw(200, 350, 400, 700)  # 배경 이미지
        
        current_time = time.time()
        time_left = max(0, int(self.time_limit - (current_time - self.start_time)))

        # 타이머 출력
        
        self.font.draw(10, 675, f"Time: {time_left}s", (255, 255, 255))

        # 보드판 그리기
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.grid_size + self.grid_size // 2
                y = row * self.grid_size + self.grid_size // 2 + 100
                self.tile.draw(x, y, self.grid_size, self.grid_size)

        # 선택된 캐릭터 그리기
        for character in self.characters:
            character.draw()
            
        for enemy in self.enemies:
            enemy.draw()
            
        if hasattr(self, 'boss'):  # 보스가 있다면
            self.boss.draw()
            
    def spawn_boss(self):
        """보스 생성 (selected_boss에 따라)"""
        if global_state.selected_boss == "dragon":
            self.boss = Dragon(
                name="Dragon",
                image_path=load_image("resource/image/boss_dragon.png"),  # 드래곤 이미지 경로
                x=200,
                y=570,
                hp=4000,
                atk=500,
                atk_speed=1.0
            )
            print(f"{self.boss.name}이(가) 생성되었습니다!")
            
    def spawn_enemy(self):
        """적 생성"""
        empty_tiles = self.get_empty_tiles()
        if empty_tiles:
            spawn_tile = random.choice(empty_tiles)
            spawn_x = spawn_tile[0] * self.grid_size + self.grid_size // 2
            spawn_y = spawn_tile[1] * self.grid_size + self.grid_size // 2 + 100

            new_enemy = Enemy(
                name="little_dragon",
                position=(spawn_tile[0], spawn_tile[1]),
                attack_power=30,
                attack_speed=0.5,
                hp=100
            )
            self.enemies.append(new_enemy)
            print(f"적 생성: {new_enemy.name} ({spawn_tile})")

    def get_empty_tiles(self):
        #비어 있는 타일 좌표 리스트 반환
        occupied_tiles = set()
        for character in self.characters:
            occupied_tiles.add(((character.x - self.grid_size // 2) // self.grid_size,
                                (character.y - 100 - self.grid_size // 2) // self.grid_size))

        for enemy in self.enemies:
            occupied_tiles.add(enemy.position)

        empty_tiles = [
            (col, row)
            for col in range(self.board_size)
            for row in range(self.board_size)
            if (col, row) not in occupied_tiles
        ]
        return empty_tiles

    def change_scene(self, new_scene):
        global_state.current_scene 
        global_state.current_scene = new_scene  # 전역 current_scene을 새로운 씬으로 교체
    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y
            grid_x = x // self.grid_size
            grid_y = (y - 100) // self.grid_size

            if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size:
                # 빈 땅인지 확인
                target_tile_empty = True
                clicked_character = None

                for character in self.characters:
                    if character.x == grid_x * self.grid_size + self.grid_size // 2 and \
                    character.y == grid_y * self.grid_size + self.grid_size // 2 + 100:
                        target_tile_empty = False
                        clicked_character = character
                        break

                # 선택된 캐릭터를 가져옴
                selected_character = None
                for character in self.characters:
                    if character.isSelected:
                        selected_character = character
                        break

                if selected_character:
                    if target_tile_empty:
                        # 빈 타일 클릭 시 선택된 캐릭터 이동
                        self.deselect_all_characters()
                        selected_character.move_to(grid_x, grid_y, self.grid_size, 100)
                    else:
                        # 다른 캐릭터 클릭 시 선택 캐릭터 변경
                        self.deselect_all_characters()
                        clicked_character.isSelected = True
                else:
                    # 선택된 캐릭터가 없는 경우, 클릭된 캐릭터 선택
                    if not target_tile_empty:
                        self.deselect_all_characters()
                        clicked_character.isSelected = True


    def deselect_all_characters(self):
        """모든 캐릭터의 선택 상태를 해제하는 함수"""
        for character in self.characters:
            character.isSelected = False