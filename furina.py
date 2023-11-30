from character import Character, D
import worldtree as w
import random


class Furina(Character):
    def __init__(self, priority=0, name='芙宁娜', ai=True, max_hp=50, force=0, defense=5):
        self._pet = Singer(priority, name+'的歌者', ai, max_hp=max_hp, force=force, defense=defense)
        self.not_pet_hp = max_hp
        self.theater = 0
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Hydro'
        self.huangmang = '荒'

    @property
    def hp(self):
        if self._pet:
            self.not_pet_hp = self._pet._hp
            return self._pet._hp
        else:
            return self.not_pet_hp

    @hp.setter
    def hp(self, value):
        if self.theater and value != self.not_pet_hp:
            self.force += 1
            print(f'{self.name}万众狂欢增加武力值至{self.force}')
        if self._pet:
            self._pet._hp = value
        self.not_pet_hp = value

    @property
    def pet(self):
        return self._pet

    def skill1(self):
        # 深海沙龙
        if self.get_state('behavior') == 'rounds_begin' and self._pet and \
                w.find_character_in_camp(self._pet) == -1:
            print(f'{self._pet.name}亮相')
            w.camp[w.find_character_in_camp(self)].append(self._pet)

    def skill2(self):
        # 孤心沙龙：技能。切荒芒。CD=1。结束。荒：allD8水；芒：allD8治
        skill_name = '孤心沙龙'
        if self.get_state('behavior') == 'rounds_begin':
            self.skill2_cd = 0 if self.skill2_cd < 2 else self.skill2_cd - 1

        if self in w.front_end and self.get_state('behavior') == 'skill' and not self.skill2_cd:
            self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
            if self.get_state('ban', bool):
                return
            to_use = False
            if self.ai:
                aim = '荒'
                for character in w.camp[w.find_character_in_camp(self)]:
                    if character.max_hp - character.hp > 8:
                        aim = '芒'
                if self.huangmang != aim:
                    to_use = True
            else:
                to_use = self.release(f'{skill_name}替换当前的{self.huangmang}')
            if to_use:
                self.skill2_cd = 1
                self.huangmang = '荒' if self.huangmang == '芒' else '芒'
                print(f'{self.name}{skill_name}切换为{self.huangmang}')
                self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})

        if self.get_state('behavior') == 'rounds_end' and self._pet:
            normal_power = D(8)
            print(f'{self._pet.name}{skill_name}{self.huangmang}性：D8={normal_power}')
            if self.huangmang == '荒':
                for every_camp in w.camp:
                    if self in every_camp:
                        continue
                    for target in every_camp:
                        self.change_event({'behavior': 'face_power', 'source': self._pet,
                                           'element': 'Hydro', 'normal_power': normal_power,
                                           'target': target})
            elif self.huangmang == '芒':
                for target in w.camp[w.find_character_in_camp(self)]:
                    self.change_event({'behavior': 'cure', 'source': self._pet,
                                       'normal_power': normal_power, 'target': target})

    def skill3(self):
        # 万众狂欢：鉴定开始。2回hp变武+1
        if self.get_state('behavior') == 'rounds_begin' and self.theater:
            self.theater -= 1
        skill_name = '万众狂欢'
        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill3_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        if self.ai:
            to_use = True
        else:
            to_use = self.release(skill_name)
        if to_use:
            self.skill3_cd = 1
            self.theater = 2
            print(f'{self.name}{skill_name}')
            self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})


class Singer(Character):
    def __init__(self, priority=0, name='芙宁娜', ai=True, max_hp=50, force=0, defense=5):
        self._hp = max_hp
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

if __name__ == '__main__':
    furina = Furina()
    print("Furina的血量为：", furina.hp)
    print("Pet的血量为：", furina.pet.hp)

    furina.hp += 1
    print("Furina的血量为：", furina.hp)
    print("Pet的血量为：", furina.pet.hp)

    furina.pet.hp += 1
    print("Furina的血量为：", furina.hp)
    print("Pet的血量为：", furina.pet.hp)

    furina._pet = None
    furina.hp += 9
    print("Furina的血量为：", furina.hp)
    # print("Pet的血量为：", furina.pet.hp)
