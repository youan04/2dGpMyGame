from pico2d import *

open_canvas()
knight = load_image('knightBoy.png')
screen1 = load_image('screen1.png')
#knight.draw_now(400, 30)
screen1.draw_now(400,30)
frame = 0
# for x in range(0, 800, 10):
#     clear_canvas()
#     knight.clip_draw(frame * 100, 0, 100, 100, x, 90)
#     update_canvas()
#     frame = (frame + 1) % 8
#     delay(0.05)
close_canvas()