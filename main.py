from event import Event
import worldtree as w


event = Event()


def start_a_war():
    winner = -1
    while w.rounds < 20:  # 20 轮强制结束
        w.attacker, w.defender = None, None
        w.rounds += 1
        print('rounds', w.rounds, 'begin')
        w.switch_character()  # 切人
        event.change_event({'behavior': 'rounds_begin'})
        event.change_event({'behavior': 'evaluate_begin'})
        for every_camp in w.camp:
            for character in every_camp:
                character.print_info()
        w.evaluate_values[:] = [0] * len(w.camp)
        while len(w.evaluate_values) != len(set(w.evaluate_values)):
            event.change_event({'behavior': 'evaluate'})
        for every_camp in w.camp:
            for character in every_camp:
                character.priority = 0
        w.attacker = w.front_end[w.evaluate_values.index(max(w.evaluate_values))]
        w.attacker.priority = 2
        w.defender = w.front_end[w.evaluate_values.index(min(w.evaluate_values))]
        w.defender.priority = 1
        critical = 0  # 暴击
        if max(w.evaluate_values) - min(w.evaluate_values) > 8:
            critical = 1
        event.change_event({'behavior': 'evaluate_end'})
        event.change_event({'behavior': 'fight_begin'})
        event.change_event({'behavior': 'normal_attack', 'source': w.attacker,
                            'target': w.defender, 'critical': critical})
        event.change_event({'behavior': 'fight_end'})
        event.change_event({'behavior': 'skill_begin'})
        event.change_event({'behavior': 'skill'})
        event.change_event({'behavior': 'skill_end'})
        event.change_event({'behavior': 'rounds_end'})
        winner = w.check_win()
        if winner != -1:  # 判是否分出胜负
            break
    return winner


from woodenstake import Woodenstake  # 木桩
from paimon import Paimon  # 高级派蒙
from character import Character  # 派蒙
from qingque import Qingque  # 青雀
from clorinde import Clorinde  # 克洛琳德
from clara import Clara  # 克拉拉
from keqing import Keqing  # 刻晴


if __name__ == '__main__':

    situation = []
    for i in range(100):
        w.camp[0].append(Paimon())
        w.camp[1].append(Keqing(ai=True))
        situation.append(start_a_war())
        w.restart()
    '''print(f'木桩胜率：{situation.count(0) / len(situation)} '
          f'评分：{w.f(situation.count(0) / len(situation))}')
    print(f'胜率：{situation.count(1) / len(situation)} '
          f'评分：{w.f(situation.count(1) / len(situation))}')
    print(f'平局率：{situation.count(-1) / len(situation)}')'''
    print(f'胜率：{situation.count(1) / len(situation)}')
