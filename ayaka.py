from character import Character, D
import worldtree as w
import random


class Ayaka(Character):
    def __init__(self, priority=0, name='绫华', ai=True, max_hp=30, force=8, defense=1):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Anemo'
        self.enchantment, self.enchantment_time, self.frost, self.pre_front = '', 2, False, self

    def skill1(self):
        # 寒天宣命祝词：切角+D3冰、附2回合
        skill_name = '寒天宣命祝词'
        if self.get_state('behavior') == 'rounds_begin':
            if self.enchantment_time == 1 and self.enchantment == 'Cryo':
                self.enchantment = ''
                print(f'{self.name}{skill_name}冰附魔结束')
            self.enchantment_time = self.enchantment_time - 1 if self.enchantment_time > 0 else 0
            if self in w.front_end and self.pre_front != self:
                self.enchantment = 'Cryo'
                self.enchantment_time = 2
                print(f'{self.name}{skill_name}获得2回合冰附魔')

    def normal_attack(self):
        if not self.enchantment_time:
            return super().normal_attack()
        if self.get_state('behavior') != 'normal_attack' or self.get_state('source') != self:
            return
        self.modify_event({'behavior': 'normal_attack_begin'})
        if self.get_state('ban', bool):
            return
        critical = self.get_state('critical', int)
        a, b, c = D(13), D(13) * critical, self.force
        normal_power = a + b + c
        print(f'{self.name}投掷：D13={a}+暴击={b}+{self.force}={c}={normal_power}')
        add_state = {'element': self.enchantment,
                     'normal_power': normal_power,
                     'fixed_power': 0,
                     'breakthrough': False,
                     'behavior': 'normal_attack_generate_power'}
        self.modify_event(add_state)
        add_state['behavior'] = 'face_power'
        if self.enchantment == 'Cryo':
            self.enchantment = ''
        self.modify_event(add_state)
        self.modify_event({'behavior': 'normal_attack_end'})

    def skill2(self):
        # 神里流·冰华：D9+3。入场。CD=3
        skill_name = '神里流·冰华'
        if self.get_state('behavior') == 'rounds_begin' and self.skill2_cd:  # cd刷新
            self.skill2_cd -= 1
        if self.get_state('behavior') != 'skill' \
                or self not in w.front_end or self.skill2_cd:  # 时机判断
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        target = self.select_target()
        if not target:
            return
        to_use = False
        if self.ai:
            if len(w.camp[w.find_character_in_camp(self)]) > 1 or\
                    self.enchantment_time < 2 or self.hp < 15:
                to_use = True
            else:
                to_use = random.choice([True, False])
        else:
            to_use = self.release(skill_name)
        if to_use:
            self.skill2_cd = 3
            new_state = {'source': self, 'behavior': 'release_skill', 'name': skill_name}
            self.change_event(new_state)
            self.enchantment = 'Cryo'
            self.enchantment_time = 2
            print(f'{self.name}{skill_name}获得2回合冰附魔')
            normal_power = D(12)
            print(f'{self.name}{skill_name}：#D12={normal_power}')
            new_state = {'element': 'Cryo',
                         'normal_power': normal_power,
                         'behavior': 'face_power',
                         'source': self,
                         'target': target}
            self.change_event(new_state)

    def skill3(self):
        # 神里流·霜灭：技能。2回合D12+3。入场
        skill_name = '神里流·霜灭'
        target = self.select_target()
        if self.frost and self.get_state('behavior') == 'skill_begin' and target:
            self.frost = False
            normal_power = D(15)
            print(f'{self.name}{skill_name}第二段：#D15={normal_power}')
            new_state = {'element': 'Cryo',
                         'normal_power': normal_power,
                         'behavior': 'face_power',
                         'source': self,
                         'target': target}
            self.change_event(new_state)

        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill3_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        if not target:
            return
        if self.ai:
            if len(w.camp[w.find_character_in_camp(self)]) > 1 or \
                    self.enchantment_time < 2 or self.hp < 20:
                to_use = True
            else:
                to_use = random.choice([True, False])
        else:
            to_use = self.release(skill_name)
        if to_use:
            self.skill3_cd = 1
            new_state = {'source': self, 'behavior': 'release_skill', 'name': skill_name}
            self.change_event(new_state)
            self.enchantment = 'Cryo'
            self.enchantment_time = 2
            print(f'{self.name}{skill_name}获得2回合冰附魔')
            self.frost = True
            normal_power = D(15)
            print(f'{self.name}{skill_name}：#D15={normal_power}')
            new_state = {'element': 'Cryo',
                         'normal_power': normal_power,
                         'behavior': 'face_power',
                         'source': self,
                         'target': target}
            self.change_event(new_state)
