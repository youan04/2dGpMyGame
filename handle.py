from pico2d import *

def handle_event(event, current_scene):
    if event.type == SDL_QUIT:  # 종료 이벤트 처리
        return False
    elif event.type == SDL_KEYDOWN:  # 키 다운 이벤트 처리
        if event.key == SDLK_ESCAPE:  # ESC 키 처리
            return False
        elif event.key == SDLK_1:  # '1' 키 처리
            import scene_main
            current_scene.change_scene(scene_main.SceneMain())  # 메인 씬으로 전환
        elif event.key == SDLK_2:  # '2' 키 처리
            import scene_character
            current_scene.change_scene(scene_character.SceneCharacter())  # 캐릭터 씬으로 전환
        elif event.key == SDLK_3:  # '3' 키 처리
            import scene_select
            current_scene.change_scene(scene_select.SceneSelect())  # 선택 씬으로 전환
        elif event.key == SDLK_4:  # '4' 키 처리
            import scene_ingame
            current_scene.change_scene(scene_ingame.SceneIngame())  # 게임 씬으로 전환
    return True