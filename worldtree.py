import math

camp = [[], []]  # 双方阵营
front_end = [None, None]  # 前台角色
attacker = None  # 进攻方
defender = None  # 防御方
evaluate_values = []  # 鉴定值
rounds = 0  # 轮次
elements = ['Anemo', 'Geo', 'Electro', 'Dendro', 'Hydro', 'Pyro', 'Cryo']
other_elements = ['Quantum', 'Imaginary']


def restart():
    global camp, front_end, attacker, defender, evaluate_values, rounds, elements, other_elements
    camp = [[], []]  # 双方阵营
    front_end = [None, None]  # 前台角色
    attacker = None  # 进攻方
    defender = None  # 防御方
    evaluate_values = []  # 鉴定值
    rounds = 0
    elements = ['Anemo', 'Geo', 'Electro', 'Dendro', 'Hydro', 'Pyro', 'Cryo']
    other_elements = ['Quantum', 'Imaginary']


def switch_character():  # 切角上场
    global evaluate_values
    for i in range(len(camp)):
        front_end[i] = camp[i][0]  # 为方便测试


def find_character_in_camp(character):  # 查所在队伍
    index = -1
    for i, row in enumerate(camp):
        if character in row:
            index = i
            break
    return index


def check_win():  # 判赢
    non_empty_camp = [i for i, row in enumerate(camp) if any(row)]
    if len(non_empty_camp) == 1:
        print('team', non_empty_camp[0], 'win')
        return non_empty_camp[0]
    return -1


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def f(x):
    return 2 * sigmoid(sigmoid(x))
