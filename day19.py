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

def find(substring: str, string: str, idx: int=0) -> int:
    try:
        return string.index(substring, idx) 
    except ValueError:
        return -1

if __name__ == '__main__':
    print("Starting")
    mol, replacements = read_input()
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
    print(len(candidates))