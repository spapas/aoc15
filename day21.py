import itertools

ITEMS = """Dagger        8     4       0  W
Shortsword   10     5       0  W
Warhammer    25     6       0  W
Longsword    40     7       0  W
Greataxe     74     8       0  W
Leather      13     0       1  A
Chainmail    31     0       2  A
Splintmail   53     0       3  A
Bandedmail   75     0       4  A
Platemail   102     0       5  A
Damage +1    25     1       0  R 
Damage +2    50     2       0  R
Damage +3   100     3       0  R
Defense +1   20     0       1  R
Defense +2   40     0       2  R
Defense +3   80     0       3  R"""


def parse_item(item):
    parts = [z.strip() for z in item.split("  ") if z]
    return {
        "name": parts[0],
        "cost": int(parts[1]),
        "dmg": int(parts[2]),
        "arm": int(parts[3]),
        "kind": parts[4],
    }


def read_items():
    lines = ITEMS.split("\n")
    return [parse_item(i) for i in lines]


def game_over(player, boss):
    return player["hp"] <= 0 or boss["hp"] <= 0


def sim(player, boss):
    print("Player: " + str(player))
    print("Boss: " + str(boss))
    player_turn = True
    while not game_over(player, boss):
        turn(player, boss, player_turn)
        player_turn = not player_turn
    if boss["hp"] <= 0:
        return True
    return False


def turn(player, boss, player_turn):
    if player_turn:
        f = player
        t = boss
    else:
        f = boss
        t = player

    dmg = f["dmg"]
    arm = t["arm"]
    do_dmg = dmg - arm
    if do_dmg <= 0:
        do_dmg = 1
    t["hp"] -= do_dmg

    s = "The {who} deals {dmg}-{arm} = {do_dmg} damage; the {other} goes down to {hp} hit points.".format(
        who="player" if player_turn else "boss",
        dmg=dmg,
        arm=arm,
        do_dmg=do_dmg,
        other="boss" if player_turn else "player",
        hp=t["hp"],
    )
    print(s)


def get_combination_cost(items):
    return sum(i["cost"] for i in items)


def update_player_stats(player, items):
    for item in items:
        player["dmg"] += item["dmg"]
        player["arm"] += item["arm"]


def get_item_names(items):
    return ", ".join([s["name"] for s in items])

def allowed_combination(items):
    weapon_count = len([w for w in items if w['kind'] == 'W' ])
    if weapon_count != 1:
        return False
    armor_count = len([w for w in items if w['kind'] == 'A' ])
    if armor_count > 1:
        return False
    ring_count = len([w for w in items if w['kind'] == 'R' ])
    if ring_count > 2:
        return False
    return True 


def part1():
    # test run
    player = {"hp": 8, "dmg": 5, "arm": 5}
    boss = {"hp": 12, "dmg": 7, "arm": 2}
    # sim(player, boss)

    items = read_items()
    print(items)

    item_combinations = itertools.chain(
        itertools.combinations(items, 1),
        itertools.combinations(items, 2),
        itertools.combinations(items, 3),
        itertools.combinations(items, 4),
        itertools.combinations(items, 5),
        itertools.combinations(items, 6),
        itertools.combinations(items, 7),
        itertools.combinations(items, 8),
        itertools.combinations(items, 9),
        itertools.combinations(items, 10),
    )
    min_winnable_cost = 999
    min_items = None

    for ic in item_combinations:
        if get_combination_cost(ic) > min_winnable_cost:
            #print("Too much cost! Continuing")
            continue
        if not allowed_combination(ic):
            continue
        print("Will run with {0}".format(get_item_names(ic)))
        boss = {"hp": 100, "dmg": 8, "arm": 2}
        player = {"hp": 100, "dmg": 0, "arm": 0}
        update_player_stats(player, ic)
        if sim(player, boss):
            print("*** We win!")
            min_winnable_cost = get_combination_cost(ic)
            min_items = ic
        else:
            print("We lost...")

    print(
        "Min cost is {0} with items {1}".format(
            min_winnable_cost, get_item_names(min_items)
        )
    )



def part2():
    # test run
    player = {"hp": 8, "dmg": 5, "arm": 5}
    boss = {"hp": 12, "dmg": 7, "arm": 2}
    # sim(player, boss)

    items = read_items()
    print(items)

    item_combinations = itertools.chain(
        itertools.combinations(items, 1),
        itertools.combinations(items, 2),
        itertools.combinations(items, 3),
        itertools.combinations(items, 4),
        itertools.combinations(items, 5),
        itertools.combinations(items, 6),
        itertools.combinations(items, 7),
        itertools.combinations(items, 8),
        itertools.combinations(items, 9),
        itertools.combinations(items, 10),
    )
    max_lossable_cost = -1
    max_items = None

    for ic in item_combinations:
        if get_combination_cost(ic) < max_lossable_cost:
            #print("Too much cost! Continuing")
            continue
        if not allowed_combination(ic):
            continue
        print("Will run with {0}".format(get_item_names(ic)))
        boss = {"hp": 100, "dmg": 8, "arm": 2}
        player = {"hp": 100, "dmg": 0, "arm": 0}
        update_player_stats(player, ic)
        if not sim(player, boss):
            print("*** We lose!")
            max_lossable_cost = get_combination_cost(ic)
            max_items = ic
        else:
            print("We win...")

    print(
        "Max cost is {0} with items {1}".format(
            max_lossable_cost, get_item_names(max_items)
        )
    )    


if __name__ == "__main__":
    print("Starting")
    part = "b"
    if part == "a":
        part1()
    else:
        part2()

