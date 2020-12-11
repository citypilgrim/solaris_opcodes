
from .svy21 import SVY21

svy21 = SVY21()

coord_lst = [
    31263.123, 21110.868, 
    31272.298, 21105.860,
]
N_lst = coord_lst[::2]
E_lst = coord_lst[1::2]

for i, N in enumerate(N_lst):
    E = E_lst[i]

    print(*svy21.computeLatLon(N, E))
