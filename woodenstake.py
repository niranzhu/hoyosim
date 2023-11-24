from character import Character, D
import worldtree as w
import random


class Woodenstake(Character):
    def __init__(self, priority=0, name='木桩', ai=True, max_hp=25, force=5, defense=5):
        super().__init__(priority, name)
        self.element = 'Pyro'

    def skill1(self):
        # 技能阶段发动。对前台敌方角色造成D10火元素伤害。CD=1

        if self.get_state('behavior') == 'rounds_begin' and self.skill1_cd:  # cd刷新
            self.skill1_cd -= 1
        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill1_cd:  # 时机判断
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
            to_use = self.release('木桩着火')
        if to_use:
            self.skill1_cd = 1
            a, element = D(10), 'Pyro'
            print(f'{self.name}着火：D10={a} {element}')
            new_state = {'source': self, 'behavior': 'release_skill',
                         'name': '木桩着火', 'normal_power': a,
                         'target': target, 'element': element}
            self.change_event(new_state)
            new_state['behavior'] = 'face_power'
            self.change_event(new_state)

    def skill2(self):
        # 技能阶段发动。对前台敌方角色造成2词D8火元素伤害。CD=1

        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill2_cd:  # 时机判断
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
            to_use = self.release('木桩大着火')
        if to_use:
            self.skill2_cd = 1
            for i in range(2):
                a, element = D(10), 'Pyro'
                print(f'{self.name}着大火：D8={a} {element}')
                new_state = {'source': self, 'behavior': 'release_skill',
                             'name': '木桩着大火', 'normal_power': a,
                             'target': target, 'element': element}
                self.change_event(new_state)
                new_state['behavior'] = 'face_power'
                self.change_event(new_state)

