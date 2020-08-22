doxeia = """33
14
18
20
45
35
16
35
1
13
18
13
50
44
48
6
24
41
30
42"""

doxeia =  map(int, doxeia.split('\n'))

import itertools

t = 0
found = False
for i in range(3, len(doxeia)):
    c = itertools.combinations(doxeia, i)
    if found:
        break

    print i

    for cc in c:
        if sum(cc) == 150:
            t+=1
            found = True

t = 0

c = itertools.combinations(doxeia, 4)
for cc in c:
    if sum(cc) == 150:
        t+=1

print t