from character import Character, D
import worldtree as w
import random


class Sucrose(Character):
    def __init__(self, priority=0, name='砂糖', ai=True, max_hp=30, force=3, defense=3):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Anemo'
        self.enchantment = 'Anemo'

    def skill1(self):
        # 小小的慧风：扩散固+2
        skill_name = '小小的慧风'
        if self.get_state('behavior') == 'face_power_begin' and self.get_state('source') == self and \
                self.get_state('element') == 'Anemo' and self.get_state('target'):
            if set(self.get_state('target').attachment).intersection({'Electro', 'Hydro', 'Pyro', 'Cryo'}):
                print(f'{self.name}{skill_name}扩散增2固伤')
                fixed_power = self.get_state('fixed_power', int)
                self.modify_last_event({'fixed_power': fixed_power + 2})
                self.modify_event({'fixed_power': fixed_power + 2}, notify=False)

    def skill2(self):
        # 风灵作成·陆叁零捌：技能。D8。选元。CD=2
        skill_name = '风灵作成·陆叁零捌'
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
        to_use = 0
        some_ele = ['Electro', 'Hydro', 'Pyro', 'Cryo', 'Anemo']
        if self.ai:
            if set(target.attachment).intersection(set(some_ele)):
                to_use = 5
            else:
                to_use = random.randint(1, 4)
        else:
            while True:
                try:
                    to_use = int(input(f'{self.name}{skill_name}：1.雷；2.水；3.火；4.冰；5.风；0.取消 '))
                except ValueError:
                    print('输入数字')
                    continue
                if 5 >= to_use >= 0:
                    break
        if to_use:
            self.skill2_cd = 2
            new_state = {'source': self, 'behavior': 'release_skill', 'name': skill_name, 'choice': to_use}
            self.change_event(new_state)
            normal_power = D(8)
            print(f'{self.name}{skill_name}：#D8={normal_power}{some_ele[to_use - 1]}')
            new_state = {'element': some_ele[to_use - 1],
                         'normal_power': normal_power,
                         'behavior': 'face_power',
                         'source': self,
                         'target': target}
            self.change_event(new_state)

    def skill3(self):
        # 风灵作成·柒伍同构贰型：技能。allD10风、D10附，牵引
        skill_name = '风灵作成·柒伍同构贰型'
        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill3_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        target = self.select_target()
        if not target:
            return
        if self.ai:
            if target.attachment or target.hp < 5:
                to_use = True
        else:
            to_use = self.release(skill_name)
        if to_use:
            self.skill3_cd = 1
            print(f'{self.name}：{skill_name}')
            self.change_event({'source': self, 'behavior': 'release_skill',
                               'name': skill_name, 'target': target})
            for character in w.camp[w.find_character_in_camp(target)]:
                for element in character.attachment:
                    normal_power = D(10)
                    print(f'{self.name}{skill_name}附加：D10={normal_power}')
                    self.change_event({'source': self, 'behavior': 'face_power',
                                       'name': skill_name, 'normal_power': normal_power,
                                       'target': character, 'element': element})
                normal_power = D(10)
                print(f'{self.name}{skill_name}原始：D10={normal_power}')
                self.change_event({'source': self, 'behavior': 'face_power',
                                   'name': skill_name, 'normal_power': normal_power,
                                   'target': character, 'element': 'Anemo'})
            if target and target.hp > 0:
                self.tug(source=self, target=target)
