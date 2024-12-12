class Projectile:
    def __init__(self, x, y, direction_x, direction_y, speed, range, damage, direction, image, width = 50, height = 50):
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
        self.width = width
        self.height = height
        self.flip = 'w'  # 기본 반전 없이 출력
        self.image = image  # 투사체 이미지

    def update(self):
        """투사체 위치 업데이트"""
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        self.distance_travelled += self.speed
        
        # 방향에 맞게 각도 설정
        if self.direction == "idle_right":
            self.direction_x = 1
            self.direction_y = 0
            self.angle = 0  # 오른쪽 방향
            self.flip = 'w'
        elif self.direction == "idle_left":
            self.direction_x = -1
            self.direction_y = 0
            self.angle = 0  # 왼쪽 방향
            self.flip = 'h'  # 수평 반전
        elif self.direction == "idle_up":
            self.direction_x = 0
            self.direction_y = 1
            self.angle = 90  # 위 방향
            self.flip = 'w'
        elif self.direction == "idle_down":
            self.direction_x = 0
            self.direction_y = -1
            self.angle = 270 # 아래 방향
            self.flip = 'w'  # flip은 'w'로 설정하고, 회전만 처리

    def draw(self):
        """투사체 그리기"""
        # angle에 맞춰 회전된 이미지를 그린다.
        self.image.clip_composite_draw(0, 0, self.image.w, self.image.h, 
                                       self.angle, self.flip, self.x, self.y, self.width, self.height)

    def is_out_of_range(self):
        """투사체가 지정된 범위를 벗어나면 True"""
        return self.distance_travelled >= self.range * 50
    
    def check_collision(self, target):
        # 투사체 크기와 대상 크기를 고려한 충돌 감지
        if (self.x - self.width // 2 < target.x + target.width // 2 and
            self.x + self.width // 2 > target.x - target.width // 2 and
            self.y - self.height // 2 < target.y + target.height // 2 and
            self.y + self.height // 2 > target.y - target.height // 2):
            print("적과 충돌")
            return True
        return False
