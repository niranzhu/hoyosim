from character import Character, D
import worldtree as w
import random


class Clara(Character):
    def __init__(self, priority=0, name='克拉拉', ai=True, max_hp=40, force=1, defense=6):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = ''
        self.amplification = 0

    def skill1(self):
        # 我们是家人：史瓦罗强化每回合开始减1
        if self.get_state('behavior') == 'rounds_begin' and self.amplification:
            self.amplification -= 1

    def skill2(self):
        # 史瓦罗在看着你。反伤D10。CD=0
        skill_name = '史瓦罗在看着你'
        if self.get_state('behavior') != 'damage_end' or \
                self.get_state('target') != self or self.hp <= 0:  # 时机判断
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        target = self.get_state('source')
        if not target or target == self:
            return
        normal_power = 0
        if self.amplification:
            normal_power = D(15)
            print(f'离开克拉拉：#D15={normal_power}')
        else:
            normal_power = D(10)
            print(f'{skill_name}：#D10={normal_power}')
        new_state = {'source': self, 'behavior': 'release_skill',
                     'name': skill_name, 'a': normal_power}
        self.change_event(new_state)
        add_state = {'element': '',
                     'normal_power': normal_power,
                     'behavior': 'face_power',
                     'source': self,
                     'target': target}
        self.modify_event(add_state)

    def skill3(self):
        # 是约定不是命令：技能。强化。CD=3
        skill_name = '是约定不是命令'
        if self.get_state('behavior') == 'rounds_begin' and self.skill3_cd:  # cd刷新
            self.skill3_cd -= 1
        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill3_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        if self.ai:  # ai 积极发动
            to_use = True
        else:
            to_use = self.release(skill_name)
        if to_use:
            self.skill3_cd = 3
            self.amplification = 2
            new_state = {'source': self, 'behavior': 'release_skill', 'name': skill_name}
            self.change_event(new_state)
            print(f'{self.name}：帮帮我，史瓦罗先生！')

