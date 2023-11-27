from character import Character, D
import worldtree as w
import random

from woodenstake import Woodenstake  # 木桩
from paimon import Paimon  # 高级派蒙
from character import Character  # 派蒙
from qingque import Qingque  # 青雀
from clorinde import Clorinde  # 克洛琳德
from clara import Clara  # 克拉拉
from keqing import Keqing  # 刻晴
from kokomi import Kokomi  # 心海


def create_random_pet(source=None):
    pet_classes = [
        Woodenstake,
        Paimon,
        Qingque,
        Clorinde,
        Clara,
        Keqing,
        Kokomi,
        Dottore  # 多托雷
    ]
    return (random.choice(pet_classes))()


class Dottore(Character):
    def __init__(self, priority=0, name='多托雷', ai=True, max_hp=50, force=5, defense=0):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Cryo'
        self.small_Dottore = None  # 切片
        self.seal = False

    def skill1(self):
        # 切片实验：把人做成切片
        if self.get_state('behavior') != 'rounds_begin' or self.small_Dottore:
            return
        self.hp -= 20
        self.small_Dottore = create_random_pet()
        print(f'切片实验：{self.small_Dottore.name}')
        self.small_Dottore.hp = 20
        self.small_Dottore.ai = self.ai
        w.camp[w.find_character_in_camp(self)].append(self.small_Dottore)

    def skill2(self):
        # 随机组合实验：
        return
        if self.get_state('behavior') != 'reduce_defense_end' \
                or self.get_state('target') != self or not self.seal \
                or self.get_state('damage', int) <= 0:
            return
        print(f'{self.name}雷锲减伤')
        self.modify_last_event({'new_damage': self.get_state('damage', int) - 6})
        self.modify_event({'new_damage': self.get_state('damage', int) - 6}, notify=False)
        self.seal = False

    def skill3(self):
        # 周末的疯狂实验：技能。对手武力+7并自残
        skill_name = '周末的疯狂实验'
        if self not in w.front_end or self.get_state('behavior') != 'skill' or self.skill3_cd:
            return
        self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
        if self.get_state('ban', bool):
            return
        to_use = False
        target = self.select_target()
        if not target:
            return
        if self.ai:  # ai 随机发动
            if random.randint(1, 5) > 1:
                to_use = True
        else:
            to_use = self.release(skill_name)
        if to_use:
            self.skill3_cd = 1
            target.force += 7
            output = random.choice([f'与我对话最好用更恭敬的口吻，{target.name}。你很有用，可那并不意味着你能不灭。',
                                    f'大家已经想好让你牺牲了，{target.name}，带上它，去为你的狐狸同伴而死吧。',
                                    f'我将亲自参与治疗，帮助{target.name}康复，这样如何呢？'])
            print(f'{self.name}{skill_name}：{output}')
            self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})
            self.change_event({'behavior': 'normal_attack', 'source': target,
                               'target': target, 'critical': 0})
