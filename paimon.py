from character import Character, D
import worldtree as w
import random


class Paimon(Character):
    def __init__(self, priority=0, name='派蒙', ai=True, max_hp=30, force=3, defense=3):
        super().__init__(priority, name)

    def skill1(self):
        # 技能阶段发动。对前台敌方角色造成D5随机元素伤害。CD=2

        if self.get_state('behavior') == 'rounds_begin' and self.skill1_cd:  # cd刷新
            self.skill1_cd -= 1
        if self not in w.front_end or self.get_state('behavior') != 'skill':  # 时机判断
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        target = None  # 查询敌人
        for character in w.front_end:
            if w.find_character_in_camp(character) != w.find_character_in_camp(self):
                target = character
                break
        if not target:
            return
        if self.ai:  # ai 积极发动
            if random.randint(1, 100) > 2:
                to_use = True
        else:
            to_use = self.release('随机元素伤害')
        if to_use:
            self.skill1_cd = 2
            a, element = D(5), random.choice(w.elements)
            # element = random.choice(['Electro', 'Dendro'])
            print(f'{self.name}发动随机元素投掷：D5={a} {element}')
            new_state = {'source': self, 'behavior': 'release_skill',
                         'name': '随机元素伤害', 'normal_power': a,
                         'target': target, 'element': element}
            self.change_event(new_state)
            new_state['behavior'] = 'face_power'
            self.change_event(new_state)

