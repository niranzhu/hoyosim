from event import Event
from character import Character
import worldtree as w
from paimon import Paimon

event = Event()


def start_a_war():
    winer = -1
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
        winer = w.check_win()
        if winer != -1:  # 判是否分出胜负
            break
    return winer


if __name__ == '__main__':
    situation = []
    for i in range(9):
        w.camp[0].append(Character(name='派蒙'))
        w.camp[1].append(Paimon(name='高级派蒙'))
        situation.append(start_a_war())
        w.restart()
    print(f'派蒙胜率：{situation.count(0) / len(situation)}')
    print(f'高级派蒙胜率：{situation.count(1) / len(situation)}')
    print(f'平局率：{situation.count(-1) / len(situation)}')