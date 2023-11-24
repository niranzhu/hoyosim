from character import Character, D
import worldtree as w
import random


class Clorinde(Character):
    def __init__(self, priority=0, name='克洛琳德', ai=True, max_hp=28, force=1, defense=7):
        super().__init__(priority, name, ai)
        self.element = 'Electro'
        self.ammunition, self.ammunition_name = 5, '始基力弹药'

    def skill1(self):
        # 奉辞罚罪：a时，消耗1-2弹，每D4雷一类。CD=1
        skill_name = '奉辞罚罪'
        if self.get_state('behavior') == 'rounds_begin' and self.skill1_cd:  # cd刷新
            self.skill1_cd -= 1
        if self.get_state('behavior') != 'normal_attack_begin' \
                or self.get_state('source') != self or self.skill1_cd:  # 时机判断
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = 0
        target = self.get_state('target')
        if not target or not self.ammunition:
            return
        if self.ai:  # ai 积极发动
            to_use = min(self.ammunition, 2)
        else:
            while True:
                print(f'持{self.ammunition}{self.ammunition_name}且至多用2')
                to_use = self.release(skill_name, data_type=int, cost=self.ammunition_name)
                if self.ammunition >= to_use >= 0 and to_use < 3:
                    break
        if to_use:
            self.ammunition -= to_use
            self.skill1_cd = 1
            a = []
            for i in range(to_use):
                a.append(D(4))
            print(f'{self.name}{skill_name}：{to_use}#D4={a}')
            new_state = {'source': self, 'behavior': 'release_skill',
                         'name': skill_name, 'a': a}
            self.change_event(new_state)
            self.modify_last_event({'ban': True})
            critical = self.get_state('critical')
            a, b, c, d = D(10), D(10) * critical, self.force, sum(a)
            normal_power = a + b + c + d
            print(f'{self.name}投掷：D10={a}+暴击={b}+{self.force}={c}+{skill_name}={d}={normal_power}')
            add_state = {'element': 'Electro',
                         'normal_power': normal_power,
                         'fixed_power': 0,
                         'breakthrough': False,
                         'behavior': 'normal_attack_generate_power'}
            self.modify_event(add_state)
            add_state['behavior'] = 'face_power'
            self.modify_event(add_state)

    def skill2(self):
        # 雨夜的大清洗：技能。all弹，每D5雷一类。得6-all
        name = '雨夜的大清洗'
        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill2_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        target = self.select_target()
        if not target:
            return
        if self.ai:  # ai 积极发动
            to_use = True
        else:
            print(f'持{self.ammunition}{self.ammunition_name}')
            to_use = self.release(name)
        if to_use:
            self.skill2_cd = 1
            if self.ammunition:
                a = []
                for i in range(self.ammunition):
                    a.append(D(5))
                print(f'{self.name}{name}{self.ammunition}#D5={a}')
            normal_power = sum(a)
            new_state = {'source': self, 'behavior': 'release_skill',
                         'name': name, 'normal_power': normal_power,
                         'target': target, 'element': 'Electro'}
            self.change_event(new_state)
            print(f'{self.name}：你这虫留在世上只会把米吃贵！')
            new_state['behavior'] = 'face_power'
            self.change_event(new_state)
        else:
            new_state = {'source': self, 'behavior': 'release_skill', 'name': name}
            self.change_event(new_state)
            print(f'{self.name}：你这虫留在世上只会把米吃贵！')
        self.ammunition = 6 - self.ammunition
