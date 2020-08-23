def read_input():
    replacements = []
    
    with open("day19.txt", "r") as fin:
        lines = fin.read().split('\n')
        for idx, l in enumerate(lines):
            if l == '':
                mol = lines[idx+1]
                break
            replacements.append(l.split(' => '))

    return mol, replacements

# A* implementation from https://nbviewer.jupyter.org/url/norvig.com/ipython/Advent%20of%20Code.ipynb
from heapq       import heappop, heappush

def astar_search(start, h_func, moves_func):
    "Find a shortest sequence of states from start to a goal state (a state s with h_func(s) == 0)."
    frontier  = [(h_func(start), start)] # A priority queue, ordered by path length, f = g + h
    previous  = {start: None}  # start state has no previous state; other states will
    path_cost = {start: 0}     # The cost of the best path to a state.
    while frontier:
        (f, s) = heappop(frontier)
        if h_func(s) == 0:
            return Path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heappush(frontier, (new_cost + h_func(s2), s2))
                path_cost[s2] = new_cost
                previous[s2] = s
    return dict(fail=True, front=len(frontier), prev=len(previous))    

def Path(previous, s): 
    "Return a list of states that lead to state s, according to the previous dict."
    return ([] if (s is None) else Path(previous, previous[s]) + [s])

def find(substring: str, string: str, idx: int=0) -> int:
    try:
        return string.index(substring, idx) 
    except ValueError:
        return -1


def get_replacements_for_str(replacements, mol):
    candidates = set([])
    for r in replacements:
        f = r[0]
        t = r[1]
        i = find(f, mol)
        while(i>=0):
            new_i = i+len(f)
            new_mol = mol[:i] + t + mol[new_i:]
            candidates.add(new_mol)
            i = find(f, mol, new_i)
    return candidates

def get_reverse_replacements_for_str(replacements, mol):
    candidates = set([])
    for r in replacements:
        f = r[1]
        t = r[0]
        i = find(f, mol)
        while(i>=0):
            new_i = i+len(f)
            new_mol = mol[:i] + t + mol[new_i:]
            candidates.add(new_mol)
            i = find(f, mol, new_i)
    return candidates

def str_diff(s):
    l = len(s)-1
    if l == 0:
        return 0 if s == 'e' else 1
    return l

if __name__ == '__main__':
    print("Starting")
    mol, replacements = read_input()
    candidates = get_replacements_for_str(replacements, mol)
    print(len(candidates))

    r2 = [
        ['e', 'H'],
        ['e', 'O'],
        ['H', 'HO'],
        ['H', 'OH'],
        ['O', 'HH'],
    ]

    m2 = 'HOHOHO'

    r = astar_search(m2, lambda s: str_diff(s), lambda s: get_reverse_replacements_for_str(r2, s))
    print(r)
    print(len(r)-1)

    r = astar_search(mol, lambda s: str_diff(s), lambda s: get_reverse_replacements_for_str(replacements, s))
    print(len(r)-1)