class Projectile:
    def __init__(self, x, y, direction_x, direction_y, speed, range, damage, direction, image):
        self.x = x
        self.y = y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = speed
        self.range = range
        self.damage = damage
        self.direction = direction
        self.distance_travelled = 0  # 투사체가 이동한 거리
        self.angle = 0  # 회전 각도
        self.image = image  # 투사체 이미지

    def update(self):
        """투사체 위치 업데이트"""
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        self.distance_travelled += self.speed
        
        # 방향에 맞게 각도 설정
        if self.direction == 'idle_right':
            self.direction_x = 1
            self.direction_y = 0
            self.angle = 0  # 오른쪽 방향
        elif self.direction == 'idle_left':
            self.direction_x = -1
            self.direction_y = 0
            self.angle = 180  # 왼쪽 방향
        elif self.direction == 'idle_up':
            self.direction_x = 0
            self.direction_y = 1
            self.angle = 90  # 위 방향
        elif self.direction == 'idle_down':
            self.direction_x = 0
            self.direction_y = -1
            self.angle = 270  # 아래 방향


    def draw(self):
        """투사체 그리기"""

        self.image.clip_composite_draw(0, 0, self.image.w, self.image.h, 
                                       self.angle, 'w', self.x, self.y, 50, 50)

    def is_out_of_range(self):
        """투사체가 지정된 범위를 벗어나면 True"""
        print("투사체 사라짐")
        return self.distance_travelled >= self.range * 50
       
