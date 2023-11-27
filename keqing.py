from character import Character, D
import worldtree as w
import random


class Keqing(Character):
    def __init__(self, priority=0, name='刻晴', ai=True, max_hp=25, force=5, defense=5):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Electro'
        self.seal = False  # 雷锲

    def skill1(self):
        # 星斗归位：a后。下次受伤抵消6点；或对敌D10雷。CD=3
        skill_name = '星斗归位'
        if self.get_state('behavior') == 'rounds_begin' and self.skill1_cd:  # cd刷新
            self.skill1_cd -= 1
        if self.get_state('behavior') != 'normal_attack_end' \
                or self.get_state('source') != self or self.skill1_cd:  # 时机判断
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = 0
        target = self.get_state('target')
        if not target:
            return
        if self.ai:  # ai 随机发动
            to_use = random.randint(1, 2)
        else:
            while True:
                try:
                    to_use = int(input(f'{self.name}{skill_name}：1.存留；2.引爆；0.取消 '))
                except ValueError:
                    print('输入数字')
                    continue
                if 2 >= to_use >= 0:
                    break
        if to_use:
            self.skill1_cd = 3
            new_state = {'source': self, 'behavior': 'release_skill',
                         'name': skill_name, 'choice': to_use}
            self.change_event(new_state)
        if to_use == 1:
            self.seal = True
            print(f'{self.name}存留雷锲')
        elif to_use == 2:
            print(f'{self.name}引爆雷锲')
            normal_power = D(10)
            print(f'{self.name}{skill_name}：#D10={normal_power}')
            new_state = {'element': 'Electro',
                         'normal_power': normal_power,
                         'behavior': 'face_power',
                         'source': self,
                         'target': target}
            self.change_event(new_state)

    def skill2(self):
        # 玉衡之贵：雷锲减6伤
        if self.get_state('behavior') != 'reduce_defense_end' \
                or self.get_state('target') != self or not self.seal \
                or self.get_state('damage', int) <= 0:
            return
        print(f'{self.name}雷锲减伤')
        self.modify_last_event({'new_damage': self.get_state('damage', int) - 6})
        self.modify_event({'new_damage': self.get_state('damage', int) - 6}, notify=False)
        self.seal = False

    def skill3(self):
        # 天街巡游：技能。7#D7二类
        name = '天街巡游'
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
            string = random.choice(['剑出，影随！', '剑光如我，斩尽芜杂！'])
            print(f'{self.name}：{string}')
            for i in range(7):
                if not target or self.hp < 0:
                    return
                normal_power = D(7)
                print(f'{self.name}D7={normal_power}')
                new_state = {'source': self, 'behavior': 'release_skill',
                             'name': name, 'normal_power': normal_power,
                             'target': target, 'element': 'Electro'}
                self.change_event(new_state)
                new_state['behavior'] = 'face_power'
                self.change_event(new_state)

