from pico2d import *

class Character:
    def __init__(self, name, image_path, x, y):
        self.name = name  # 캐릭터 이름
        self.image = load_image(image_path)  # 스프라이트 시트 로드
        self.x, self.y = x, y  # 캐릭터 위치
        self.width, self.height = 50, 50  # 캐릭터 크기
        self.state = "idle_down"  # 초기 상태 (가만히 아래를 보고 있음)
        self.frame = 0  # 현재 애니메이션 프레임
        self.frame_speed = 0.1  # 프레임 갱신 속도

    def set_state(self, new_state):
        """상태 변경 함수"""
        if self.state != new_state:
            self.state = new_state
            self.frame = 0  # 상태 전환 시 프레임 초기화

    def update(self):
        """애니메이션 프레임 업데이트"""
        if "walk" in self.state:  # 걷는 상태일 때만 프레임 갱신
            self.frame = (self.frame + self.frame_speed) % 3  # 걷기 프레임은 0, 1, 2
        else:
            self.frame = 0  # 정지 상태는 첫 번째 프레임 유지

    def draw(self):
        """현재 상태에 따라 스프라이트 시트에서 프레임 추출 및 그리기"""
        total_columns = 3  # 각 줄의 열 개수
        total_rows = 4  # 스프라이트 시트의 총 행 개수
        frame_int = int(self.frame)  # 현재 프레임 정수화
        frame_width = self.image.w // total_columns
        frame_height = self.image.h // total_rows

        # 상태에 따른 행(row) 선택
        if self.state == "idle_down" or self.state == "walk_down":
            current_row = 3  # 아래 방향 (4번째 행)
        elif self.state == "idle_right" or self.state == "walk_right":
            current_row = 2  # 오른쪽 방향 (3번째 행)
        elif self.state == "idle_left" or self.state == "walk_left":
            current_row = 1  # 왼쪽 방향 (2번째 행)
        elif self.state == "idle_up" or self.state == "walk_up":
            current_row = 0  # 위 방향 (1번째 행)

        # 정지 상태는 첫 번째 열(열 번호 0), 걷기 상태는 현재 프레임
        if "idle" in self.state:
            current_column = 0  # 정지 상태
        else:
            current_column = frame_int  # 걷기 상태

        # 스프라이트 시트에서 해당 프레임 추출 및 그리기
        self.image.clip_draw(
            frame_width * current_column,
            frame_height * current_row,
            frame_width,
            frame_height,
            self.x, self.y, self.width, self.height
        )
