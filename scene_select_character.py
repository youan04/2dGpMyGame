from pico2d import *

class SceneCharacter:
    def __init__(self):
        # 캐릭터 씬 이미지 로드
        self.image = load_image('resource/image/door.png')  
        self.knight = load_image('resource/image/knight.png')
        self.archer = load_image('resource/image/door.png')
        self.mage = load_image('resource/image/door.png')
        self.priest = load_image('resource/image/door.png')
        self.guard = load_image('resource/image/door.png')

        # 각 캐릭터별 프레임 초기화
        self.frame = {
            'knight': 0,
            'archer': 0,
            'mage': 0,
            'priest': 0,
            'guard': 0
        }
        self.frame_speed = 1 # 초당 프레임 갱신 속도 설정 (FPS)

    def update(self):
        # 각 캐릭터의 프레임 업데이트
        for key in self.frame:
            self.frame[key] = (self.frame[key] + self.frame_speed * (1 / 60)) % 12  # 각 캐릭터는 12 프레임으로 구성

    def draw_character(self, image, frame, x, y, width, height):
        total_columns = 3
        total_rows = 4
        frame_int = int(frame)
        frame_width = image.w // total_columns
        frame_height = image.h // total_rows
        # current_column = frame_int % total_columns
        # current_row = total_rows - 1 - (frame_int // total_columns)
        
        # 맨 위 가로줄(첫 번째 행)의 프레임만 사용
        current_column = frame_int % total_columns  # 열 번호는 0~2로 순환
        current_row = total_rows - 1  # 맨 위 행 고정

        # 캐릭터 애니메이션 그리기
        image.clip_draw(
            frame_width * current_column,
            frame_height * current_row,
            frame_width,
            frame_height,
            x, y, width, height
        )

    def draw(self):
        clear_canvas()  # 화면 지우기

        # 배경 이미지 그리기
        self.image.draw(200, 350, 400, 700)

        # 각 캐릭터의 애니메이션 그리기
        self.draw_character(self.knight, self.frame['knight'], 50, 650, 50, 50)
        self.draw_character(self.archer, self.frame['archer'], 125, 650, 50, 50)
        self.draw_character(self.mage, self.frame['mage'], 200, 650, 50, 50)
        self.draw_character(self.priest, self.frame['priest'], 50, 575, 50, 50)
        self.draw_character(self.priest, self.frame['guard'], 125, 575, 50, 50)

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전 (캔버스 높이에 맞게)

        return self  # 기본적으로 현재 씬 유지
