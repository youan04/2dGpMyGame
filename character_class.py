from pico2d import *

class Character:
    def __init__(self, character_name, x, y, image_path):
        self.x = x
        self.y = y
        self.character_type = character_name  # 캐릭터 타입
        
        # 이미지 로드 시 오류 처리
        try:
            self.image = load_image(image_path)  # 이미지 로드
            print(f"Image {image_path} loaded successfully.")  # 로드 성공 시 메시지 출력
        except Exception as e:
            print(f"Error loading image: {image_path}. Exception: {e}")
            self.image = None  # 이미지가 로드되지 않으면 None 설정

    def draw(self):
        if self.image:  # 이미지가 로드된 경우에만 그리기
            self.image.draw(self.x * 50 + 25, self.y * 50 + 25, 50, 50)
        else:
            print(f"Image not loaded for {self.character_type}")  # 로드되지 않으면 경고 출력

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

# 캐릭터 객체 생성 시 이미지 경로를 함께 전달
knight = Character("knight", 0, 0, "resource\\image\\knight.png")
archer = Character("archer", 1, 0, "resource\\image\\archer.png")
mage = Character("mage", 2, 0, "resource\\image\\mage.png")
priest = Character("priest", 3, 0, "resource\\image\\priest.png")

# 객체들을 리스트나 딕셔너리로 관리할 수 있음
characters = {
    "knight": knight,
    "archer": archer,
    "mage": mage,
    "priest": priest
}

# 아래는 예시로 characters를 사용하여 그리기 등의 작업을 진행할 수 있음.
# 예를 들어, 게임 씬에서 캐릭터들을 그릴 때 characters 딕셔너리를 사용할 수 있습니다.

def draw_all_characters():
    for character in characters.values():
        character.draw()

# 캐릭터를 이동시킬 때
def move_character(character_name, new_x, new_y):
    if character_name in characters:
        characters[character_name].move(new_x, new_y)
