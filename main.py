from pico2d import *

open_canvas(400, 700)
knight = load_image('knightBoy.png')
screen1 = load_image('blue_sky.png')

# 이미지를 중앙에 너비 500, 높이 500으로 그림
screen1.draw(200, 350, 400, 700)

# 캔버스를 업데이트하여 이미지를 화면에 표시
update_canvas()

delay(2)
close_canvas()