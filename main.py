#main.py
from pico2d import *
import global_handle
import scene_main, scene_select_character, scene_select_map, scene_ingame
import character_class
import global_state

def main():
    open_canvas(400, 700)  # 캔버스 크기 설정
    global_state.current_scene = scene_main.SceneMain()  # 처음에 메인 씬으로 시작

    running = True
    while running:
        global_state.current_scene.update()  # 현재 씬 업데이트
        global_state.current_scene.draw()    # 현재 씬 그리기
        
        update_canvas()         # 캔버스 업데이트
        
        events = get_events()   # 이벤트 처리
        for event in events:
            
            running = global_handle.handle_event(global_state.current_scene, event)  # 이벤트 핸들러 호출
            global_state.current_scene.handle_event(event)
        
            if not running:
                break

    close_canvas()  # 캔버스 닫기

if __name__ == '__main__':
    main()  # 메인 함수 실행