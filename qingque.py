from character import Character, D
import worldtree as w
import random


class Qingque(Character):
    def __init__(self, priority=0, name='青雀', ai=True, max_hp=30, force=2, defense=4):
        super().__init__(priority, name, ai)
        self.element = 'Quantum'

    def skill1(self):
        # 不求人：海底捞月后可以替换一次D2结果。2次

        if self.get_state('behavior') != 'release_skill' or self.skill1_cd < -1\
                or self.get_state('source') != self or self.get_state('name') != '海底捞月摸4':
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        a = self.get_state('a')
        if self.ai:
            if a.count(1) == 1 or a.count(2) == 1:
                to_use = True
        else:
            to_use = self.release(f'不求人（剩余{self.skill1_cd+2}次）')
            if to_use:
                if (self.skill1_cd < 0 and a.count(1) == 2) or a.count(1) == 0 or a.count(2) == 0:
                    print('不要浪费时间，朋友！')
                    to_use = False
                elif a.count(1) != 1 and a.count(2) != 1:
                    self.skill1_cd -= 1
        if to_use:
            if a.count(1) == 1:
                a = [2, 2, 2, 2]
            else:
                a = [1, 1, 1, 1]
            new_state = {'source': self, 'behavior': 'release_skill',
                         'name': '不求人', 'a': a}
            self.change_event(new_state)
            self.skill1_cd -= 1
            self.modify_last_event({'new_a': a})



    def skill2(self):
        # 海底捞月：a前用。4次D2，若相同，暴击且基础为2D15，量子。CD=1
        skill_name = '海底捞月'
        if self.get_state('behavior') == 'rounds_begin' and self.skill2_cd:  # cd刷新
            self.skill2_cd -= 1
        if self.get_state('behavior') != 'normal_attack_begin' \
                or self.get_state('source') != self or self.skill2_cd:  # 时机判断
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        target = self.get_state('target')
        if not target:
            return
        if self.ai:  # ai 积极发动
            to_use = True
        else:
            to_use = self.release(skill_name)
        if to_use:
            print(random.choice(['这是一场豪赌', '还能再赌一赌', '还有三次机会',
                                 '要不放手一搏', '都到这份上了']) + '，朋友！')
            self.skill2_cd = 1
            a = []
            for i in range(4):
                a.append(D(2))
            print(f'{self.name}海底捞月：4#D2={a}')
            new_state = {'source': self, 'behavior': 'release_skill',
                         'name': '海底捞月摸4', 'a': a}
            self.change_event(new_state)
            if self.get_state('new_a'):
                a = self.get_state('new_a')
            if a == [1, 1, 1, 1] or a == [2, 2, 2, 2]:
                print('和了！')
            else:
                print('输得一塌糊涂，朋友！')
                return
            self.modify_last_event({'ban': True})
            critical = 1
            a, b, c = D(15), D(15) * critical, self.force
            normal_power = a + b + c
            print(f'{self.name}投掷：D15={a}+暴击={b}+{self.force}={c}={normal_power}')
            add_state = {'element': 'Quantum',
                         'normal_power': normal_power,
                         'fixed_power': 0,
                         'breakthrough': False,
                         'behavior': 'normal_attack_generate_power'}
            self.modify_event(add_state)
            add_state['behavior'] = 'face_power'
            self.modify_event(add_state)

    def skill3(self):
        # 四幺暗时？和！：技能阶段。2D15+武力值的量子。
        name = '四幺暗时？和！'
        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill3_cd:
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
            to_use = self.release(name)
        if to_use:
            self.skill3_cd = 1
            a, b, c, element = D(15), D(15), self.force, 'Quantum'
            normal_power = a + b + c
            print(f'{self.name}拜托拜托：D15={a}+D15={b}+{c}={c}={normal_power} {element}')
            new_state = {'source': self, 'behavior': 'release_skill',
                         'name': name, 'normal_power': normal_power,
                         'target': target, 'element': element}
            self.change_event(new_state)
            new_state['behavior'] = 'face_power'
            self.change_event(new_state)

