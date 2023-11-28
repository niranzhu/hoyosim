from event import Event
from observer import Observer
import worldtree as w
from buff import Buff
import random
import os
import sys


def D(num):
    if num > 1:
        return random.randint(1, num)
    elif num == 1:
        return 1
    elif num == 0:
        return 0
    elif num == -1:
        return -1
    else:
        return - random.randint(1, -num)


class Character(Observer):
    def __init__(self, priority=0, name='NPC', ai=True, max_hp=30, force=3, defense=3):
        super().__init__(priority)
        self.name, self.ai = name, ai
        self.max_hp, self.force, self.defense = max_hp, force, defense
        # hp，元素力，附魔，附着
        self.hp, self.element, self.enchantment, self.attachment = self.max_hp, '?', '', []
        self.shield = 0  # 盾
        self.buff = []
        self.skill1_cd, self.skill2_cd, self.skill3_cd, = 0, 0, 0

    def print_info(self):
        print(f'{w.find_character_in_camp(self)}队 '
              f'{self.name} {self.hp}hp {self.force}攻 {self.defense}防 '
              f'{self.shield}盾 {self.enchantment}附魔 {self.attachment}附着 '
              f'{[buff.name for buff in self.buff]}加成')

    def normal_attack(self):
        if self.get_state('behavior') != 'normal_attack' or self.get_state('source') != self:
            return
        self.modify_event({'behavior': 'normal_attack_begin'})
        if self.get_state('ban', bool):
            return
        critical = self.get_state('critical', int)
        a, b, c = D(10), D(10) * critical, self.force
        normal_power = a + b + c
        print(f'{self.name}投掷：D10={a}+暴击={b}+{self.force}={c}={normal_power}')
        add_state = {'element': self.enchantment,
                     'normal_power': normal_power,
                     'fixed_power': 0,
                     'breakthrough': False,
                     'behavior': 'normal_attack_generate_power'}
        self.modify_event(add_state)
        add_state['behavior'] = 'face_power'
        self.modify_event(add_state)
        self.modify_event({'behavior': 'normal_attack_end'})

    def face_power(self):
        if self.get_state('behavior') != 'face_power' or self.get_state('target') != self:
            return
        self.modify_event({'behavior': 'face_power_begin'})
        normal_power = self.get_state('normal_power', int)
        fixed_power = self.get_state('fixed_power', int)
        element = self.get_state('element', str)
        breakthrough = self.get_state('breakthrough', bool)
        source = self.get_state('source')

        # 元素反应
        if not self.attachment and element \
                and element != 'Anemo' and element != 'Geo':
            self.attachment.append(element)
        elif self.attachment:
            remove_attachment = []
            for attachment in self.attachment:
                if set([attachment, element]) == set(['Pyro', 'Cryo']):  # 融
                    print('融化')
                    normal_power += D(5)
                    remove_attachment.append(attachment)
                elif set([attachment, element]) == set(['Pyro', 'Hydro']):  # 蒸
                    print('蒸发')
                    normal_power += D(5)
                    remove_attachment.append(attachment)
                elif set([attachment, element]) == set(['Electro', 'Cryo']):  # 导
                    print('超导')
                    fixed_power += 2
                    # 后台穿透
                    for character in w.camp[w.find_character_in_camp(self)]:
                        if character != self:
                            self.modify_event({'target': character,
                                               'normal_power': 0,
                                               'fixed_power': 2,
                                               'breakthrough': False,
                                               'element': ''})
                    remove_attachment.append(attachment)
                elif set([attachment, element]) == set(['Electro', 'Hydro']):  # 电
                    print('感电')
                    fixed_power += 2
                    # 后台穿透
                    for character in w.camp[w.find_character_in_camp(self)]:
                        if character != self:
                            self.modify_event({'target': character,
                                               'normal_power': 0,
                                               'fixed_power': 2,
                                               'breakthrough': False,
                                               'element': ''})
                elif set([attachment, element]) == set(['Pyro', 'Dendro']):  # 燃
                    print('燃烧')
                    self.buff.append(Buff(name='Burn', owner=self))
                    fixed_power += 2
                    remove_attachment.append(attachment)
                elif set([attachment, element]) == set(['Hydro', 'Cryo']):  # 冻
                    print('冻结')
                    self.buff.append(Buff(name='Freeze', owner=self))
                    remove_attachment.append(attachment)
                elif set([attachment, element]) == set(['Electro', 'Pyro']):  # 载
                    print('超载')
                    fixed_power += 2
                    remove_attachment.append(attachment)
                    # def 此处欠缺拉人
                elif set([attachment, element]) == set(['Dendro', 'Hydro']):  # 绽
                    print('绽放')
                    fixed_power += 2
                    self.modify_event({'target': source,
                                       'source': source,
                                       'normal_power': 5,
                                       'behavior': 'cure'})
                    remove_attachment.append(attachment)
                elif set([attachment, element]) == set(['Electro', 'Dendro']):  # 激
                    print('激化')
                    self.buff.append(Buff(name='Stimulate', owner=self))
                    fixed_power += 2
                    remove_attachment.append(attachment)
                elif element == 'Anemo' and attachment in ['Electro', 'Hydro', 'Pyro', 'Cryo']:  # 扩
                    print('扩散')
                    fixed_power += 2
                    # 后台穿透
                    for character in w.camp[w.find_character_in_camp(self)]:
                        if character != self:
                            self.modify_event({'target': character,
                                               'normal_power': 0,
                                               'fixed_power': 2,
                                               'breakthrough': False,
                                               'element': ''})
                    remove_attachment.append(attachment)
                elif element == 'Geo' and attachment in ['Electro', 'Hydro', 'Pyro', 'Cryo']:  # 结
                    print('结晶')
                    self.modify_event({'target': source,
                                       'source': source,
                                       'normal_power': 5,
                                       'behavior': 'get_shield'})
                    remove_attachment.append(attachment)
                elif element == 'Quantum':  # 纠
                    print('纠缠')
                    self.buff.append(Buff(name='Entanglement', owner=self))
                    fixed_power += 2
                    remove_attachment.append(attachment)
                elif element == 'Imaginary':  # 禁
                    print('禁锢')
                    self.buff.append(Buff(name='Confinement', owner=self))
                    fixed_power += 2
                    remove_attachment.append(attachment)
                elif element and element not in self.attachment:
                    self.attachment.append(element)
            if remove_attachment:
                for i in remove_attachment:
                    self.attachment.remove(i)

        damage = normal_power
        if not breakthrough:
            damage -= self.defense  # 防
            self.modify_event({'behavior': 'reduce_defense_end', 'damage': damage})
            new_damage = self.get_state('new_damage', int)
            damage = new_damage if new_damage > 0 else damage
        damage = max(0, damage) + fixed_power
        if not damage:
            print('未能破防')
            self.modify_event({'behavior': 'damage_less_defense'})
            return
        elif damage <= self.shield:
            print('未能破盾')
            self.modify_event({'behavior': 'damage_less_shield'})
            return
        elif self.shield:
            damage -= self.shield
            self.shield = 0
            self.modify_event({'behavior': 'damage_break_shield', 'damage': damage})
            damage += self.get_state('break_shield_damage', int)
        self.modify_event({'behavior': 'damage_begin', 'damage': damage})
        damage += self.get_state('begin_damage', int)
        self.hp -= damage
        print(f'{source.name}造成{damage}{element}给{self.name}'
              f'剩{self.hp}附着{self.attachment}')
        self.modify_event({'behavior': 'damage_end', 'damage': damage})

    def cure(self):
        if self.get_state('behavior') != 'cure' or self.get_state('target') != self:
            return
        self.modify_event({'behavior': 'cure_begin'})
        self.hp += self.get_state('normal_power', int) \
                   * (1 + self.get_state('efficiency', int))
        if self.hp >= self.max_hp:
            self.hp = self.max_hp
            self.modify_event({'behavior': 'cure_to_max'})
        print(f'{self.name}治疗至{self.hp}点')
        self.modify_event({'behavior': 'cure_end'})

    def get_shield(self):
        if self.get_state('behavior') != 'get_shield' or self.get_state('target') != self:
            return
        self.modify_event({'behavior': 'get_shield_begin'})
        if self.shield >= self.get_state('normal_power', int):
            self.modify_event({'behavior': 'remain_shield'})
        else:
            self.shield = self.get_state('normal_power', int)
            self.modify_event({'behavior': 'renew_shield'})
        print(f'{self.name}叠盾至{self.shield}点')
        self.modify_event({'behavior': 'get_shield_end'})

    def die(self):  # 判断死亡
        if self.get_state('behavior') != 'damage_end':
            return
        if self.hp <= 0:
            print(self.name, 'die')
            self.modify_event({'behavior': 'die', 'target': self})
            if self.buff:
                for every_buff in self.buff:
                    every_buff.owner = None
                    del every_buff
                self.buff.clear()
            for every_camp in w.camp:
                if self in every_camp:
                    every_camp.remove(self)
            if w.attacker == self:
                w.attacker = None
            if w.defender == self:
                w.defender = None
            if self in w.front_end:
                w.front_end[w.find_character_in_camp(self)] = None
            self.remove_observer(self)
            del self

    def evaluate(self):
        if self not in w.front_end or self.get_state('behavior') != 'evaluate':
            return

        self.change_event({'behavior': 'evaluate1', 'source': self})
        a, b = D(20), D(self.force)
        evaluate_value = a + b
        print(f'{self.name}投掷：D20={a}+D{self.force}={b}={evaluate_value}')
        self.change_event({'behavior': 'evaluate2', 'source': self, 'a': a, 'b': b})
        evaluate_value += self.get_state('c', int)
        w.evaluate_values[w.find_character_in_camp(self)] = evaluate_value
        self.change_event({'behavior': 'evaluate3', 'source': self, 'evaluate_value': evaluate_value})

    def select_target(self, aim='1enemy'):
        target = None
        if aim == '1enemy':
            for character in w.front_end:
                if w.find_character_in_camp(character) != w.find_character_in_camp(self):
                    return character
        return target

    def release(self, name='', data_type=bool, cost=''):
        if os.name == 'nt':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import termios
            termios.tcflow(sys.stdin, termios.TCIOFLUSH)
        if data_type == bool:
            return input(f'{self.name}是否发动{name} (y)').lower() == 'y'
        elif data_type == int:
            while True:
                num = 0
                try:
                    num = int(input(f'{self.name}花费多少{cost}发动{name} (0取消)'))
                except ValueError:
                    print('输入数字')
                    continue
                return num


    def skill1(self):
        pass

    def skill2(self):
        pass

    def skill3(self):
        pass

    def response_event(self):
        self.normal_attack()
        self.face_power()
        self.cure()
        self.get_shield()
        self.die()
        self.evaluate()
        self.skill1()
        self.skill2()
        self.skill3()

