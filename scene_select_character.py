from pico2d import *

class SceneCharacter:
    def __init__(self):
        # 캐릭터 씬 이미지 로드
        self.image = load_image('resource/image/door.png')  
        self.knight_button = load_image('resource/image/knight.png')
        self.archer_button = load_image('resource/image/archer.png')
        self.mage_button = load_image('resource/image/mage.png')
        self.priest_button = load_image('resource/image/priest.png')
        self.guard_button = load_image('resource/image/guard.png')

        # 각 캐릭터별 프레임 초기화
        self.frame_button = {
            'knight_button': 0,
            'archer_button': 0,
            'mage_button': 0,
            'priest_button': 0,
            'guard_button': 0
        }
        self.frame_speed = 1 # 초당 프레임 갱신 속도 설정 (FPS)

    def update(self):
        # 각 버튼의 프레임 업데이트
        for key in self.frame_button:
            self.frame_button[key] = (self.frame_button[key] + self.frame_speed * (1 / 60)) % 12  # 각 캐릭터는 12 프레임으로 구성

    def draw_button(self, image, frame, x, y, width, height):
        total_columns = 3
        total_rows = 4
        frame_int = int(frame)
        frame_width = image.w // total_columns
        frame_height = image.h // total_rows
        # current_column = frame_int % total_columns
        # current_row = total_rows - 1 - (frame_int // total_columns)
        
        #맨 위 가로줄(첫 번째 행)의 프레임만 사용
        current_column = frame_int % total_columns  # 열 번호는 0~2로 순환
        current_row = total_rows - 1  # 맨 위 행 고정

        # 버튼 애니메이션 그리기
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
        button_size = 125
        # 각 버튼 애니메이션 그리기
        self.draw_button(self.knight_button, self.frame_button['knight_button'], 0*button_size+75, 700-button_size, button_size, button_size)
        self.draw_button(self.archer_button, self.frame_button['archer_button'], 1*button_size+75, 700-button_size, button_size, button_size)
        self.draw_button(self.mage_button, self.frame_button['mage_button'], 2*button_size+75, 700-button_size, button_size, button_size)
        self.draw_button(self.priest_button, self.frame_button['priest_button'], 0*button_size+75, 700-2*button_size, button_size, button_size)
        self.draw_button(self.guard_button, self.frame_button['guard_button'], 1*button_size+75, 700-2*button_size, button_size, button_size)

    def change_scene(self, new_scene):
        self.__class__ = new_scene.__class__  # 새로운 씬으로 클래스 변경
        self.__dict__ = new_scene.__dict__  # 새로운 씬의 속성 복사

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, 700 - event.y  # y 좌표 반전 (캔버스 높이에 맞게)

        return self  # 기본적으로 현재 씬 유지
