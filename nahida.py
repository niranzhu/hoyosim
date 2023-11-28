from character import Character, D
import worldtree as w
import random


class Nahida(Character):
    def __init__(self, priority=0, name='纳西妲', ai=True, max_hp=45, force=3, defense=3):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Dendro'
        self.dharma, self.with_skill2, self.maya = [], 0, False  # 蕴种印 余时 摩耶

    def skill1(self):
        # 梦境低语：技能。失15，D3=3
        skill_name = '梦境低语'
        if self.get_state('behavior') == 'rounds_begin':
            self.skill1_cd = self.skill1_cd - 1 if self.skill1_cd > 0 else 0
        if self.get_state('behavior') == 'skill' and self in w.front_end and not self.skill1_cd:
            self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
            if self.get_state('ban', bool):
                return
            target = self.select_target()
            if target and self.hp > 15:
                to_use = False
                if self.ai:  # ai 积极发动
                    to_use = True
                else:
                    to_use = self.release(skill_name)
                if to_use:
                    self.skill1_cd = 3
                    self.hp -= 15
                    a = D(3)
                    print(f'{self.name}{skill_name}：D3={a} 为3拉入')
                    self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})
                    if a == 3:
                        target.hp = 0
                        self.modify_event({'source': self, 'behavior': 'damage_end', 'name': skill_name})

    def skill2(self):
        # 所闻遍计：技能。2回内，所有敌受元素+D6破草。CD=2
        skill_name = '所闻遍计'
        if self.get_state('behavior') == 'skill' and self in w.front_end and not self.skill2_cd:
            self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
            if self.get_state('ban', bool):
                return
            to_use = False
            if self.ai:  # ai 积极发动
                to_use = True
            else:
                to_use = self.release(skill_name)
            if to_use:
                self.skill2_cd, self.with_skill2 = 2, 2
                print(f'{self.name}{skill_name}')
                self.dharma = w.camp[:w.find_character_in_camp(self)] + w.camp[w.find_character_in_camp(self) + 1:]
                self.dharma = [character for every_camp in self.dharma for character in every_camp]
                self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})

        if self.get_state('behavior') == 'rounds_begin':
            self.skill2_cd = self.skill2_cd - 1 if self.skill2_cd > 0 else 0
            # self.with_skill2 = self.with_skill2 - 1 if self.with_skill2 > 0 else 0
            if not self.with_skill2:
                self.dharma = []

        if self.get_state('behavior') == 'damage_end' and self.dharma and \
                self.get_state('target') in self.dharma and self.get_state('name') != '蕴种印' and \
                self.get_state('element', str):
            fixed_power = D(6)
            print(f'{self.name}{skill_name}：D6={fixed_power}')
            self.change_event({'source': self, 'behavior': 'face_power',
                               'name': '蕴种印', 'fixed_power': fixed_power,
                               'target': self.get_state('target'), 'element': 'Dendro'})

    def skill3(self):
        # 心景幻成：技能。己方免疫元素相关且每次至多受8至自身死
        skill_name = '心景幻成'
        if self in w.front_end and self.get_state('behavior') == 'skill' and not self.skill3_cd:
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
                print(f'{self.name}{skill_name}')
                self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})
                self.maya = True

        if self.get_state('behavior') == 'face_power_begin0' and self.maya and \
                w.find_character_in_camp(self.get_state('target')) == w.find_character_in_camp(self):
            if self.get_state('element', str):
                self.modify_last_event({'normal_power': 0, 'fixed_power': 0, 'element': ''})
                print(f'{self.name}{skill_name}抵挡元素')

        if self.get_state('behavior') == 'damage_begin' and self.maya and \
                w.find_character_in_camp(self.get_state('target')) == w.find_character_in_camp(self):
            if self.get_state('damage', int) > 8:
                self.modify_last_event({'begin_damage': 8 - self.get_state('damage', int)})
                print(f'{self.name}{skill_name}抵挡部分伤害')

