import global_state

class Boss:
    def __init__(self, name, hp, atk, atk_spd):
        self.name = name
        self.hp = hp / 5 * global_state.map_level
        self.atk = atk
        self.atk_spd = atk_spd
        self.special_attacks = []  # 특수 공격 목록

    def receive_attack(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} took {damage} damage. Health remaining: {self.health}")

    def attack_player(self, player):
        special_attack = self.choose_special_attack()
        damage = self.calculate_damage(special_attack, player)
        player.take_damage(damage)
        print(f"{self.name} used {special_attack} on {player.name}!")

    def choose_special_attack(self):
        # 특수 공격을 랜덤으로 선택
        from random import choice
        return choice(self.special_attacks)

    def calculate_damage(self, special_attack, player):
        # 특수 공격에 따른 피해 계산 (예시)
        if special_attack == "Fireball":
            return self.attack * 1.5 - player.defense
        elif special_attack == "Earthquake":
            return self.attack * 2 - player.defense
        elif special_attack == "Lightning Strike":
            return self.attack * 1.2 - player.defense
        return self.attack - player.defense

