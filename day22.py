import itertools, copy 
from random import gauss

def game_over(player, boss):
    return player["hp"] <= 0 or boss["hp"] <= 0


def sim(player, boss, spells):
    print("Player: " + str(player))
    print("Boss: " + str(boss))
    print("Spell list: " + str(spells))

    state = {"player_turn": True, "active_spells": [], "next_spells": spells}
    while not game_over(player, boss):
        turn(player, boss, state)
        print(state)
        state["player_turn"] = not state["player_turn"]

    if boss["hp"] <= 0:
        print("We win!")
        return True
    print("We lose!")
    return False


def cast_spell(player, boss, state):
    if not state["next_spells"]:
        # Fake lose if we don't have a spell
        player["hp"] = 0
        return

    next_spell = state["next_spells"].pop()
    if player["mana"] < SPELLS[next_spell]:
        # Fake lose if we don't have a spell
        print("Player can't cast " + next_spell + "!!!")
        player["hp"] = 0
        return

    print("Player casts " + next_spell)
    player["mana"] -= SPELLS[next_spell]
    if next_spell == "mm":
        boss["hp"] -= 4
    elif next_spell == "drain":
        boss["hp"] -= 2
        player["hp"] += 2
    elif next_spell == "shield":
        if not "shield" in [s["name"] for s in state["active_spells"]]:
            player["arm"] = 7
            state["active_spells"].append({"name": "shield", "duration": 6})
    elif next_spell == "poison":
        if not "poison" in [s["name"] for s in state["active_spells"]]:
            state["active_spells"].append({"name": "poison", "duration": 6})
    elif next_spell == "recharge":
        if not "recharge" in [s["name"] for s in state["active_spells"]]:
            state["active_spells"].append({"name": "recharge", "duration": 5})
    else:
        a += 1


def do_effects(player, boss, state):
    for a in state["active_spells"]:
        a["duration"] -= 1
        if a["name"] == "poison":
            boss["hp"] -= 3
        elif a["name"] == "recharge":
            player["mana"] += 101

    for a in state["active_spells"]:
        if a["name"] == "shield" and a["duration"] == 0:
            player["arm"] = 0
    state["active_spells"] = list(
        filter(lambda x: x["duration"] > 0, state["active_spells"])
    )

    #print(str(state["active_spells"]))


def turn(player, boss, state):
    if state["player_turn"]:
        print("\n--- PLAYER TURN ---")
    else:
        print("\n--- BOSS TURN ---")
    do_effects(player, boss, state)
    #print("EFFECTS OK")
    if boss["hp"] <= 0:
        return
    if state["player_turn"]:
        cast_spell(player, boss, state)
        #print("SPELL OK")
    else:
        dmg = boss["dmg"]
        arm = player["arm"]
        do_dmg = dmg - arm
        if do_dmg <= 0:
            do_dmg = 1
        player["hp"] -= do_dmg

        s = "The Boss deals {dmg}-{arm} = {do_dmg} damage; the player goes down to {hp} hit points.".format(
            dmg=dmg, arm=arm, do_dmg=do_dmg, hp=player["hp"],
        )
        print(s)
    print(
        format("Player HP/mana: {0}/{1}, Boss HP: {2}").format(
            player["hp"], player["mana"], boss["hp"]
        )
    )


SPELLS = {
    "mm": 53,
    "drain": 73,
    "shield": 113,
    "poison": 173,
    "recharge": 229,
}


def get_combination_cost(spells):
    return sum(SPELLS[s] for s in spells)


def get_spell_names(items):
    return ", ".join([s for s in items])


# A* implementation from https://nbviewer.jupyter.org/url/norvig.com/ipython/Advent%20of%20Code.ipynb
from heapq       import heappop, heappush

def astar_search(start, h_func, moves_func):
    "Find a shortest sequence of states from start to a goal state (a state s with h_func(s) == 0)."
    frontier  = [(h_func(start), start)] # A priority queue, ordered by path length, f = g + h
    previous  = {str(start): None}  # start state has no previous state; other states will
    path_cost = {str(start): 0}     # The cost of the best path to a state.
    while frontier:
        
        (f, s) = heappop(frontier)
        if h_func(s) == 0:
            return Path(previous, s)
        for s2 in moves_func(s):
            
            new_cost = path_cost[str(s)] + 10
            if str(s2) not in path_cost or new_cost < path_cost[str(s2)]:
                hf = h_func(s2) + gauss(0, 1)
                heappush(frontier, (new_cost + hf, s2))
                path_cost[str(s2)] = new_cost
                previous[str(s2)] = s
    return dict(fail=True, front=len(frontier), prev=len(previous))   

def Path(previous, s): 
    "Return a list of states that lead to state s, according to the previous dict."
    return ([] if (s is None) else Path(previous, previous[str(s)]) + [s])        

def state_cost(state):
    value = gauss(0, 1)
    
    if state['player']['hp'] <=0:
        return 9999 + value
    if state['player']['mana'] <=0:
        return 9999 + value
    if state['boss']['hp'] <= 0:
        return 0

    score = state['player']['mana']/5 + state['player']['hp'] + 25*state['player']['arm'] - 5*state['boss']['hp']
    if "poison" in [s["name"] for s in state["active_spells"]]:
        score+=50
    if "recharge" in [s["name"] for s in state["active_spells"]]:
        score+=10
    
    return 300 - score  + value
    

def do_effects2(old_state):
    state = copy.deepcopy(old_state)
    for a in state["active_spells"]:
        a["duration"] -= 1
        if a["name"] == "poison":
            state['boss']["hp"] -= 3
        elif a["name"] == "recharge":
            state['player']["mana"] += 101
        elif a["name"] == "shield" and a["duration"] == 0:
            state['player']["armor"] = 0
    
    state["active_spells"] = list(
        filter(lambda x: x["duration"] > 0, state["active_spells"])
    )
    
    return state 


def cast_spell2(next_spell, old_state):
    state = copy.deepcopy(old_state)

    state['player']["mana"] -= SPELLS[next_spell]
    state['casted_spells'].append(next_spell)
    if next_spell == "mm":
        state['boss']["hp"] -= 4
    elif next_spell == "drain":
        state['boss']["hp"] -= 2
        state['player']["hp"] += 2
    elif next_spell == "shield":
        state['player']["arm"] = 7
        state["active_spells"].append({"name": "shield", "duration": 6})
    elif next_spell == "poison":
        state["active_spells"].append({"name": "poison", "duration": 6})
    elif next_spell == "recharge":
        state["active_spells"].append({"name": "recharge", "duration": 5})
    else:
        a += 1
    
    return state 


def get_next_states(old_state):
    state = do_effects2(old_state)
    #print("PT " + str(state["player_turn"]))
    
    if state['boss']["hp"] <= 0:
        return []
    if state['player']["hp"] <= 0:
        return []
    if state['player']["mana"] <= 0:
        return []
    print("CHECK ME: " + str(state["player_turn"]))
    if state["player_turn"]:
        print("CHECK ME: PT")
        new_states = []
        state["player_turn"] = not state["player_turn"]
        for spell in SPELLS.keys():
            if SPELLS[spell] <= state['player']['mana']:
                # print(spell, [s["name"] for s in state["active_spells"]])
                if not spell in [s["name"] for s in state["active_spells"]]:
                    new_states.append(cast_spell2(spell, state))
        
        return new_states
    else:
        print("CHECK ME: BT")
        dmg = state['boss']["dmg"]
        arm = state['player']["arm"]
        do_dmg = dmg - arm
        if do_dmg <= 0:
            do_dmg = 1
        state['player']["hp"] -= do_dmg
        state["player_turn"] = not state["player_turn"]
        
        return [state]

def part1():
    from random import seed
    seed(1)

    state1 = {
        'player': {
            'hp': 10,
            'mana': 250,
            'arm': 0,
        },
        'boss': {
            'hp': 14,
            'dmg': 8,
        },
        'player_turn': True,
        'active_spells': [],
        'casted_spells': []
    }

    state = {
        'player': {
            'hp': 50,
            'mana': 500,
            'arm': 0,
        },
        'boss': {
            'hp': 58,
            'dmg': 9,
        },
        'player_turn': True,
        'active_spells': [],
        'casted_spells': []
    }

    r = astar_search(state, lambda s: state_cost(s), lambda s: get_next_states(s))
    
    print(r)
    casted_spells = r[-1]['casted_spells']
    print(casted_spells)
    print(sum(SPELLS[c] for c in casted_spells))
    for z in r:
        print(z['casted_spells'], state_cost(z))
    return r

def part1sim():
    spells = list(SPELLS.keys())

    spell_combinations = [
        list(['shield', 'mm', 'mm', 'recharge', 'poison', 'mm', 'recharge', 'poison', 'mm', 'mm', 'mm'])
    ]
    i = 0
    for ic in spell_combinations:

        print("Cost is " + str(get_combination_cost(ic)))

        print("Will run with {0}".format(ic))
        boss = {
            "hp": 58,
            "dmg": 9,
        }
        player = {"hp": 50, "mana": 500, "arm": 0}

        if sim(player, boss, list(reversed(ic))):
            print("*** We win!")
        else:
            print("We lost...")


if __name__ == "__main__":
    print("Starting A")
    part = "a"
    if part == "a":
        part1()
    else:
        part2()

