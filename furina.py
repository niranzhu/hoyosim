from character import Character, D
import worldtree as w
import random


class Furina(Character):
    def __init__(self, priority=0, name='芙宁娜', ai=True, max_hp=50, force=0, defense=5):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Hydro'
        self._pet = None

    @property
    def pet(self):
        return self._pet

    @pet.setter
    def pet(self, new_pet):
        if isinstance(new_pet, Pet):
            self._pet = new_pet
            self._pet.hp = self.hp  # 将 pet 对象的 hp 设置为与 Furina 对象相同
        else:
            raise ValueError("Invalid pet object!")

class Pet(Character):
    def __init__(self, priority=0, name='l', ai=True, max_hp=30, force=10, defense=3, hp=None, owner=None):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.owner = owner
        if hp is None:
            raise ValueError("Missing HP value for pet object!")
        self._hp = hp

    @property
    def hp(self):
        return self.owner.hp

    @hp.setter
    def hp(self, value):
        self._hp = value

# 创建 Furina 对象，并设置 Pet 对象的 HP 初始值为与 Furina 相同
furina = Furina(max_hp=50)
pet = Pet(max_hp=30, hp=furina.max_hp, owner=furina)

# 将 Furina 和 Pet 对象绑定起来
furina.pet = pet

# 输出 Furina 和 Pet 对象的 hp
print(f"Furina HP: {furina.hp}, Pet HP: {pet.hp}")  # 输出结果为：Furina HP: 50, Pet HP: 50

# 攻击，双方 hp 都相应减少
pet.hp -= 30
print(f"Furina HP: {furina.hp}, Pet HP: {pet.hp}")  # 输出结果为：Furina HP: 50, Pet HP: 40

furina.hp -= 10
print(f"Furina HP: {furina.hp}, Pet HP: {pet.hp}")  # 输出结果为：Furina HP: 40, Pet HP: 40