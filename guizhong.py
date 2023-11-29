from character import Character, D
import worldtree as w
import random


class Guizhong(Character):
    def __init__(self, priority=0, name='归终', ai=True, max_hp=55, force=2, defense=2):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Dust'
        self.pet = []

    def skill1(self):
        # 仙法·机关千奇：技能。召6hp。CD=3。风倾：allD8风；霜降：D12冰
        skill_name = '仙法·机关千奇'
        if self.get_state('behavior') == 'rounds_begin':
            self.skill1_cd = self.skill1_cd - 1 if self.skill1_cd > 0 else 0
        if self.get_state('behavior') == 'skill' and self in w.front_end and not self.skill1_cd:
            self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
            if self.get_state('ban', bool):
                return
            to_use = False
            if self.ai:  # ai 积极发动
                to_use = 2
                fengqing_count = sum([isinstance(pet, Fengqing) for pet in self.pet])
                shuangjiang_count = sum([isinstance(pet, Shuangjiang) for pet in self.pet])
                if fengqing_count < shuangjiang_count:
                    to_use = 1
            else:
                while True:
                    try:
                        to_use = int(input(f'{self.name}{skill_name}：1.风倾；2.霜降；0.取消 '))
                    except ValueError:
                        print('输入数字')
                        continue
                    if 2 >= to_use >= 0:
                        break
            if to_use:
                self.skill1_cd = 3
                self.pet.append(Fengqing(ai=self.ai) if to_use == 1 else Shuangjiang(ai=self.ai))
                self.pet[-1].name = f'{self.name}的{len(self.pet)}号机关{self.pet[-1].name}'
                w.camp[w.find_character_in_camp(self)].append(self.pet[-1])
                print(f'{self.name}{skill_name}：召唤{self.pet[-1].name}')
                self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})

    def skill2(self):
        # 仙法·运化万端：技能。allD8风。机关+
        skill_name = '仙法·运化万端'
        if self.get_state('behavior') == 'skill' and self in w.front_end and not self.skill2_cd:
            self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
            if self.get_state('ban', bool):
                return
            target = self.select_target()
            if not target:
                return
            to_use = False
            if self.ai:
                to_use = random.choice([True, False])
            else:
                to_use = self.release(skill_name)
            if to_use:
                self.skill2_cd = 1
                print(f'{self.name}{skill_name}')
                for source in [self] + self.pet:
                    if source and source.hp > 0:
                        normal_power = D(8)
                        print(f'{source.name}{skill_name}：D8={normal_power}')
                        for every_camp in w.camp:
                            for target in every_camp:
                                if source and target and target.hp > 0 and \
                                        w.find_character_in_camp(target) != w.find_character_in_camp(self):
                                    self.change_event({'source': source, 'target': target,
                                                       'normal_power': normal_power, 'element': 'Anemo',
                                                       'behavior': 'face_power', 'name': skill_name})
                self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})


class Fengqing(Character):
    def __init__(self, priority=0, name='风倾', ai=True, max_hp=6, force=0, defense=0):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Dust'

    def skill1(self):
        # 仙法·风倾：技能。allD8风
        skill_name = '仙法·风倾'
        if self.get_state('behavior') == 'skill' and self in w.front_end:
            self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
            if self.get_state('ban', bool):
                return
            to_use = False
            if self.ai:
                to_use = True
            else:
                to_use = self.release(skill_name)
            if to_use:
                normal_power = D(8)
                print(f'{self.name}{skill_name}：D8={normal_power}')
                for every_camp in w.camp:
                    for target in every_camp:
                        if target and target.hp > 0 and \
                                w.find_character_in_camp(target) != w.find_character_in_camp(self):
                            self.change_event({'source': self, 'target': target,
                                               'normal_power': normal_power, 'element': 'Anemo',
                                               'behavior': 'face_power', 'name': skill_name})
                self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})


class Shuangjiang(Character):
    def __init__(self, priority=0, name='霜降', ai=True, max_hp=6, force=0, defense=0):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Dust'

    def skill1(self):
        # 仙法·霜降：技能。D12冰
        skill_name = '仙法·霜降'
        if self.get_state('behavior') == 'skill' and self in w.front_end:
            self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
            if self.get_state('ban', bool):
                return
            target = self.select_target()
            if not target:
                return
            to_use = False
            if self.ai:
                to_use = True
            else:
                to_use = self.release(skill_name)
            if to_use:
                normal_power = D(12)
                print(f'{self.name}{skill_name}：D12={normal_power}')
                self.change_event({'source': self, 'target': target,
                                   'normal_power': normal_power, 'element': 'Cryo',
                                   'behavior': 'face_power', 'name': skill_name})
                self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})
