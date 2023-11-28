from character import Character, D
import worldtree as w
import random


class Rukkhadevata(Character):
    def __init__(self, priority=0, name='树王', ai=True, max_hp=45, force=6, defense=0):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element, self.enchantment = 'Dendro', 'Dendro'
        self.saptajnana, self.causality, self.dharma = True, 0, []  # 七识 因缘 法身之印
        self.with_skill2 = 0  # 月叶梦印余时
        self.skill3_killed = False

    def skill1(self):
        # 七识幻灭：受伤-3。结束D3!=3保留
        skill_name = '七识幻灭'
        if self.get_state('behavior') == 'face_power_begin' and self == self.get_state('target') \
                and self.saptajnana:
            self.modify_last_event({'fixed_power': self.get_state('fixed_power', int) - 3})
            self.modify_event({'fixed_power': self.get_state('fixed_power', int) - 3}, notify=False)
            print(f'{self.name}{skill_name}减3固伤')

        if self.get_state('behavior') == 'skill_end' and self.saptajnana:
            a = D(3)
            print(f'{self.name}{skill_name}：D3={a} 若为3失去七识幻灭')
            if a == 3:
                self.saptajnana = False

    def skill2(self):
        # 月叶梦印：技能。2回内，所有敌受、攻、技，因缘+1。因缘+2则防+1限3。CD=2
        skill_name = '月叶梦印'
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
            self.with_skill2 = self.with_skill2 - 1 if self.with_skill2 > 0 else 0
            if not self.with_skill2:
                self.dharma = []

        add = False
        if self.get_state('behavior') == 'damage_begin' and self.dharma and \
                self.get_state('target') in self.dharma:
            add = True
        elif self.get_state('behavior') == 'normal_attack_generate_power' and self.dharma and \
                self.get_state('source') in self.dharma:
            add = True
        elif self.get_state('behavior') == 'release_skill' and self.dharma and \
                self.get_state('source') in self.dharma:
            add = True
        if add:
            self.causality += 1
            print(f'{self.name}{skill_name}获得因缘')
            if self.causality in [2, 4, 6]:
                self.defense += 1


    def skill3(self):
        # 旧梦的残破：技能。所有敌D(8+因缘)草。杀则重
        skill_name = '旧梦的残破'
        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill3_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        if self.ai:
            if self.hp < 15 + self.causality:
                to_use = True
        else:
            to_use = self.release(skill_name)
        if to_use:
            self.skill3_cd = 1
            print(f'{self.name}{skill_name}')
            self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})
            self.skill3_killed = True
            while self.skill3_killed:
                self.skill3_killed = False
                for every_camp in w.camp:
                    for character in every_camp:
                        if character.hp > 0 and w.find_character_in_camp(character) != w.find_character_in_camp(self):
                            normal_power = D(8 + self.causality)
                            print(f'{self.name}{skill_name}：D(8+{self.causality})={normal_power}')
                            new_state = {'source': self, 'behavior': 'face_power',
                                         'name': skill_name, 'normal_power': normal_power,
                                         'target': character, 'element': 'Dendro'}
                            self.change_event(new_state)

        if self.get_state('behavior') == 'die' and self.get_state('name', str) == skill_name:
            self.skill3_killed = True



