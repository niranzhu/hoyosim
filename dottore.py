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
from rukkhadevata import Rukkhadevata  # 树王
from nahida import Nahida  # 纳西妲
from guizhong import Guizhong  # 归终
from sucrose import Sucrose  # 砂糖
from ayaka import Ayaka  # 绫华
from furina import Furina  # 芙宁娜


def create_random_pet(source=None):
    pet_classes = [
        Qingque,
        Clorinde,
        Clara,
        Keqing,
        Kokomi,
        Dottore,  # 博士
        Rukkhadevata,
        Nahida,
        Guizhong,
        Sucrose,
        Ayaka,
        Furina
    ]
    return (random.choice(pet_classes))()


class Dottore(Character):
    def __init__(self, priority=0, name='博士', ai=True, max_hp=50, force=5, defense=0):
        super().__init__(priority, name, ai, max_hp=max_hp, force=force, defense=defense)
        self.element = 'Cryo'
        self.small_Dottore, self.sliced = None, False  # 切片
        self.in_skill2_2, self.acted_in_skill2_2, self.with_skill2_3 = False, False, False

    def skill1(self):
        # 切片实验：把人做成切片
        if self.small_Dottore and self.small_Dottore.hp <= 0:
            self.small_Dottore = None
        if self.sliced or self.get_state('behavior') != 'rounds_begin' or self.small_Dottore:
            return
        self.sliced = True
        self.hp = self.hp - 20 if self.hp > 20 else 1
        self.small_Dottore = create_random_pet()
        print(f'{self.name}切片实验：{self.small_Dottore.name}')
        self.small_Dottore.name = self.name + '的切片' + self.small_Dottore.name
        self.small_Dottore.hp = 20
        self.small_Dottore.ai = self.ai
        w.camp[w.find_character_in_camp(self)].append(self.small_Dottore)

    def skill2(self):
        # 随机组合实验：技能。2次D3。1：D6冰；2.切片技能；3.对手物理。CD=2
        skill_name = '随机组合实验'
        if self in w.front_end and self.get_state('behavior') == 'skill' and not self.skill2_cd:
            self.modify_event({'behavior': 'release_begin', 'source': self})  # 冻结石化检测
            if self.get_state('ban', bool):
                return
            to_use = False
            if self.ai:
                to_use = True
            else:
                to_use = self.release(skill_name)
            if to_use:
                self.skill2_cd = 2
                for i in range(2):
                    a = D(3)
                    print(f'{self.name}{skill_name}第{i + 1}次D3={a}')
                    if a == 1:
                        normal_power = D(6)
                        print(f'{self.name}{skill_name}D6={normal_power}')
                        self.change_event({'source': self, 'behavior': 'release_skill', 'name': skill_name})
                        self.change_event({'behavior': 'face_power', 'source': self,
                                           'element': 'Cryo', 'normal_power': normal_power,
                                           'target': self.select_target()})
                    elif a == 2:
                        if not self.small_Dottore:
                            continue
                        self.in_skill2_2, self.acted_in_skill2_2 = True, False
                        w.front_end[w.find_character_in_camp(self)] = self.small_Dottore
                        skills_cd = [self.small_Dottore.skill1_cd, self.small_Dottore.skill2_cd,
                                     self.small_Dottore.skill3_cd]
                        self.small_Dottore.skill1_cd, self.small_Dottore.skill2_cd, \
                            self.small_Dottore.skill3_cd = 0, 0, 0
                        times = 0
                        while times < 900 and self.in_skill2_2:
                            times += 1
                            if not self.small_Dottore or None in w.front_end:
                                break
                            try:
                                behavior = random.choice(['evaluate_begin', 'evaluate_end',
                                                          'fight_begin', 'fight_end',
                                                          'skill_begin', 'skill', 'skill_end',
                                                          'normal_attack_begin', 'normal_attack_end',
                                                          'face_power_begin'])
                                self.change_event({'source': random.choice(w.front_end),
                                                   'target': random.choice(w.front_end),
                                                   'behavior': behavior})
                                self.in_skill2_2 = not self.acted_in_skill2_2
                            except Exception:
                                pass
                        if self.small_Dottore:
                            skills_cd2 = [self.small_Dottore.skill1_cd,
                                          self.small_Dottore.skill2_cd, self.small_Dottore.skill3_cd]
                            max_skills_cd = [max(skills_cd[i], skills_cd2[i]) for i in range(3)]
                            self.small_Dottore.skill1_cd, self.small_Dottore.skill2_cd, \
                                self.small_Dottore.skill3_cd = max_skills_cd[0], max_skills_cd[1], max_skills_cd[2]
                        if self:
                            w.front_end[w.find_character_in_camp(self)] = self
                            self.in_skill2_2 = False
                    elif a == 3:
                        self.with_skill2_3 = True

        if self.get_state('behavior') == 'rounds_begin':
            self.skill2_cd = 0 if self.skill2_cd < 2 else self.skill2_cd - 1
            self.with_skill2_3 = False

        if self.get_state('behavior') == 'release_begin' and self.in_skill2_2:
            if self.get_state('source') == self.small_Dottore and not self.acted_in_skill2_2:
                self.acted_in_skill2_2 = True
                self.modify_last_event({'ban': False})
            else:
                self.modify_last_event({'ban': True})

        if self.get_state('behavior') == 'face_power_begin' and self.with_skill2_3 and \
                w.find_character_in_camp(self.get_state('source')) != w.find_character_in_camp(self) and \
                self.get_state('element', str) != '':
            self.modify_last_event({'element': ''})
            print(f'{self.name}{skill_name}更改伤害为物理')

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
        if self.ai:
            if target.hp < 20:
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
