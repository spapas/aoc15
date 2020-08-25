import itertools
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Optional

SPELLS = {
    "mm": 53,
    "drain": 73,
    "shield": 113,
    "poison": 173,
    "recharge": 229,
}


@dataclass(frozen=True)
class Character:
    hp: int
    mana: int = 0
    dmg: int = 0
    arm: int = 0


@dataclass(frozen=True)
class ActiveSpell:
    name: str
    duration: int


@dataclass(frozen=True)
class State:
    player: Character
    boss: Character
    active_spells: Tuple[ActiveSpell, ...]
    casted_spells: Tuple[str, ...]
    player_turn: bool = True
    parent: Optional["State"] = None


@dataclass(frozen=True)
class Queue:
    _dq = deque()

    def push(self, e: State):
        self._dq.append(e)

    def pop(self,) -> State:
        return self._dq.popleft()
        # return self._dq.pop()

    def __len__(self):
        return len(self._dq)


def do_effects(st: State) -> State:
    dec_active_spells = [ActiveSpell(a.name, a.duration - 1) for a in st.active_spells]

    boss_hp = st.boss.hp
    player_mana = st.player.mana
    player_arm = st.player.arm

    for a in dec_active_spells:
        if a.name == "poison":
            boss_hp -= 3
        elif a.name == "recharge":
            player_mana += 101
            # print(a.name, a.duration)
        elif a.name == "shield" and a.duration == 0:
            player_arm = 0

    active_spells = tuple(filter(lambda x: x.duration > 0, dec_active_spells))


    return State(
        player=Character(hp=st.player.hp, mana=player_mana, arm=player_arm),
        boss=Character(hp=boss_hp, arm=st.boss.arm, dmg=st.boss.dmg),
        active_spells=active_spells,
        casted_spells=st.casted_spells,
        player_turn=st.player_turn,
    )


def cast_spell(spell: str, st: State) -> State:
    player_mana = st.player.mana - SPELLS[spell]
    casted_spells = st.casted_spells + (spell,)
    boss_hp = st.boss.hp
    player_hp = st.player.hp
    player_arm = st.player.arm
    active_spells = st.active_spells
    if spell == "mm":
        boss_hp -= 4
    elif spell == "drain":
        boss_hp -= 2
        player_hp += 2
    elif spell == "shield":
        player_arm = 7
        active_spells = active_spells + (ActiveSpell(name="shield", duration=6),)
    elif spell == "poison":
        active_spells = active_spells + (ActiveSpell(name="poison", duration=6),)
    elif spell == "recharge":
        active_spells = active_spells + (ActiveSpell(name="recharge", duration=5),)
    else:
        raise Exception

    return State(
        player=Character(hp=player_hp, mana=player_mana, arm=player_arm),
        boss=Character(hp=boss_hp, arm=st.boss.arm, dmg=st.boss.dmg),
        active_spells=active_spells,
        casted_spells=casted_spells,
        player_turn=False,
    )


mm = 99999


def chkwin(s: State) -> bool:
    global mm

    if s.boss.hp <= 0:
        #print("Found winning")
        #print(str(s.casted_spells))
        local_min = sum(SPELLS[z] for z in s.casted_spells)
        if local_min < mm:
            print("Found global min " + str(local_min))
            print(str(s.casted_spells))
            print(s)
            mm = local_min
        return True
    return False


def get_next_states(st: State) -> List[State]:
    efst = do_effects(st)
    if chkwin(efst):
        return []
    if efst.player_turn:
        new_states = []
        for spell in SPELLS.keys():
            if SPELLS[spell] <= efst.player.mana:
                if not spell in [z.name for z in efst.active_spells]:
                    ns = cast_spell(spell, efst)
                    if not chkwin(ns):
                        new_states.append(ns)

        return new_states

    else:  # boss turn
        dmg = efst.boss.dmg
        arm = efst.player.arm
        do_dmg = dmg - arm
        if do_dmg <= 0:
            do_dmg = 1
        player_hp = efst.player.hp - do_dmg
        if player_hp <= 0:
            # print("Found lost")
            # print(str(s.casted_spells))
            return []
        return [
            State(
                player=Character(
                    hp=player_hp, mana=efst.player.mana, arm=efst.player.arm
                ),
                boss=Character(hp=efst.boss.hp, arm=efst.boss.arm, dmg=efst.boss.dmg),
                active_spells=efst.active_spells,
                casted_spells=efst.casted_spells,
                player_turn=True,
            )
        ]


visited = list()
q = Queue()


def bfs(node: State):
    visited.append(node)
    q.push(node)

    while q:
        s = q.pop()
        ns = get_next_states(s)
        
        for neighbour in ns:
            
            q.push(
                State(
                    player=neighbour.player,
                    boss=neighbour.boss,
                    player_turn=neighbour.player_turn,
                    casted_spells=neighbour.casted_spells,
                    active_spells=neighbour.active_spells,
                    parent=s,
                )
            )


def part1():
    initial = State(
        player=Character(hp=50, mana=500, arm=0),
        boss=Character(hp=58, arm=0, dmg=9, mana=0),
        active_spells=tuple(),
        casted_spells=tuple(),
        player_turn=True,
    )

    initial1 = State(
        player=Character(hp=10, mana=250, arm=0),
        boss=Character(hp=14, arm=0, dmg=8, mana=0),
        active_spells=tuple(),
        casted_spells=tuple(),
        player_turn=True,
    )
    bfs(initial)


if __name__ == "__main__":
    print("Starting A")
    part = "a"
    if part == "a":
        part1()
    else:
        part2()

