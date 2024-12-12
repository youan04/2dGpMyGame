#skill.py

import time
from projectile import Projectile

class Skill:
    def __init__(self, name, damage, cooldown, effect=None, projectile_speed=None, duration=None):
        """
        스킬 초기화
        :param name: 스킬 이름
        :param skill_type: 스킬 타입 ("damage", "heal", "projectile", "buff")
        :param damage: 스킬의 데미지 또는 회복량
        :param cooldown: 스킬 쿨타임 (초 단위)
        :param effect: 추가 효과 함수
        :param projectile_speed: 투사체 속도 (투사체 스킬의 경우)
        :param duration: 지속 시간 (버프 스킬의 경우)
        """
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.last_used = -cooldown  # 초기화 시 바로 사용 가능
        self.effect = effect
        self.projectile_speed = projectile_speed
        self.duration = duration

    def is_available(self):
        """스킬 사용 가능 여부"""
        return (time.time() - self.last_used) >= self.cooldown

    def use(self, caster, target=None, projectiles=None):
        """
        스킬 사용
        :param caster: 스킬 사용자
        :param target: 목표 (선택)
        :param projectiles: 투사체 리스트 (투사체 스킬의 경우)
        """
        if not self.is_available():
            print(f"{self.name} is on cooldown.")
            return False

        if self.skill_name == "speed_attack":
            # 공속증가
            if self.effect:
                self.effect(caster)
                if self.duration:
                    # 일정 시간 후 효과 종료
                    time.sleep(self.duration)
                    caster.attack_speed /= 2  # 공격속도 복원
                    direction = caster.facing_direction  # (dx, dy)

        elif self.skill_name == "power_shot":
            
            projectile = Projectile(
                x=caster.x,
                y=caster.y,
                direction=direction,
                speed=self.projectile_speed,
                damage=self.damage
            )
            if projectiles is not None:
                projectiles.append(projectile)

        self.last_used = time.time()
        return True