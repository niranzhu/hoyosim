from character import Character, D
import worldtree as w
import random


class Kokomi(Character):
    def __init__(self, priority=0, name='心海', ai=True, max_hp=50, force=1, defense=4):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Hydro'
        self.jellyfish, self.hagoromo = 0, 0  # 幻海月、仪来羽衣

    def skill1(self):
        # 波起云海：不暴。固伤3
        # 固伤若有衣，hp>20+1，hp>40+1
        # 结束若有月，回D10
        skill_name = '波起云海'
        if self.get_state('behavior') == 'normal_attack_begin' and \
                self.get_state('source') == self and self.get_state('critical', int):
            self.modify_last_event({'critical': 0})
            print(f'{self.name}{skill_name}抗拒暴击')
        if self.get_state('behavior') == 'face_power_begin' and \
                self.get_state('source') == self:
            fixed_power = self.get_state('fixed_power', int)
            fixed_power += 3
            if self.hp > 20 and self.hagoromo:
                fixed_power += 1
            if self.hp > 30 and self.hagoromo:
                fixed_power += 1
            print(f'{self.name}{skill_name}固伤{fixed_power}')
            self.modify_last_event({'fixed_power': fixed_power})
            self.modify_event({'fixed_power': fixed_power}, notify=False)

        skill_name = '幻海月'
        if self.get_state('behavior') == 'rounds_begin' and self.jellyfish:
            self.jellyfish -= 1
        if self.get_state('behavior') == 'rounds_end' and self.jellyfish:
            normal_power = D(10)
            print(f'{self.name}{skill_name}D10={normal_power}')
            self.change_event({'source': self, 'target': self, 'behavior': 'cure', 'normal_power': normal_power})

    def skill2(self):
        # 海月之誓：技能。2回合月。CD=3
        skill_name = '海月之誓'
        if self.get_state('behavior') == 'rounds_begin' and self.skill2_cd:  # cd刷新
            self.skill2_cd -= 1
        if self.get_state('behavior') != 'skill' \
                or self not in w.front_end or self.skill2_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        if self.ai:
            to_use = self.hp < self.max_hp - 5
        else:
            to_use = self.release(skill_name)
        if to_use:
            print(f'{self.name}{skill_name}')
            self.skill2_cd = 3
            new_state = {'source': self, 'behavior': 'release_skill', 'name': skill_name}
            self.change_event(new_state)
            self.jellyfish = 2

    def skill3(self):
        # 海人化羽：技能。衣。
        skill_name = '海人化羽'
        if self.get_state('behavior') != 'skill' \
                or self not in w.front_end or self.skill3_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        if self.ai:
            to_use = True
        else:
            to_use = self.release(skill_name)
        if to_use:
            print(f'{self.name}{skill_name}')
            self.skill3_cd = 1
            new_state = {'source': self, 'behavior': 'release_skill', 'name': skill_name}
            self.change_event(new_state)
            self.hagoromo = 1

