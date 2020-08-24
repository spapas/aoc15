import itertools
from collections import deque
from dataclasses import dataclass

SPELLS = {
    "mm": 53,
    "drain": 73,
    "shield": 113,
    "poison": 173,
    "recharge": 229,
}

def push(dq, e):
    dq.append(e)

def pop(dq):
    return dq.popleft()

@dataclass(frozen=True)
class Character:
    hp: int
    mana: int = 0
    dmg: int = 0
    arm: int = 0

@dataclass(frozen=True)
class State:
    player: Character
    boss: Character
    player_turn: bool = True
    active_spells: tuple = ()
    casted_spells: tuple = ()

def part1():
    print("Z")



def get_next_states(old_state):
    state = do_effects2(old_state)
    # print("PT " + str(state["player_turn"]))

    if state["boss"]["hp"] <= 0:
        return []
    if state["player"]["hp"] <= 0:
        return []
    if state["player"]["mana"] <= 0:
        return []

    if state["player_turn"]:
        new_states = []
        state["player_turn"] = not state["player_turn"]
        for spell in SPELLS.keys():
            if SPELLS[spell] <= state["player"]["mana"]:
                # print(spell, [s["name"] for s in state["active_spells"]])
                if not spell in [s["name"] for s in state["active_spells"]]:
                    new_states.append(cast_spell2(spell, state))

        return new_states
    else:
        dmg = state["boss"]["dmg"]
        arm = state["player"]["arm"]
        do_dmg = dmg - arm
        if do_dmg <= 0:
            do_dmg = 1
        state["player"]["hp"] -= do_dmg
        state["player_turn"] = not state["player_turn"]

        return [state]



visited = list()
q = deque()
def bfs(node):
    visited.append(node)
    push(q, node)

    while q:
        s = pop(q)
        for neighbour in get_next_states(s):
            if neighbour not in visited:
            visited.append(neighbour)
            push(q, neighbour)



if __name__ == "__main__":
    print("Starting A")
    part = "a"
    if part == "a":
        part1()
    else:
        part2()

