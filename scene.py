from pico2d import *

class MainScreen:
    def enter(self):
        self.background = load_image('main_screen.png')

    def exit(self):
        del self.background

    def update(self):
        pass  # 메인 화면에서 필요한 업데이트 로직

    def draw(self):
        clear_canvas()
        self.background.draw(1000, 400)
        update_canvas()

class CharacterScreen:
    def enter(self):
        self.background = load_image('character_screen.png')

    def exit(self):
        del self.background

    def update(self):
        pass  # 캐릭터 화면 로직

    def draw(self):
        clear_canvas()
        self.background.draw(1000, 400)
        update_canvas()

# 기타 화면 클래스도 같은 구조로 추가

# 메인 루프에서 화면 상태 관리
def main_loop():
    current_screen = MainScreen()
    current_screen.enter()

    running = True
    while running:
        current_screen.update()
        current_screen.draw()
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_1:
                    current_screen.exit()
                    current_screen = CharacterScreen()
                    current_screen.enter()

    current_screen.exit()
    close_canvas()

open_canvas(400, 700)
main_loop()