from .svy21 import SVY21

svy21 = SVY21()

coord_lst = [
    31273.667, 21106.114, 70.796,
    31272.198, 21106.782, 70.818,
    31271.809, 21105.964, 70.814,
    31273.195, 21105.261, 70.805,
]
N_lst = coord_lst[::3]
E_lst = coord_lst[1::3]

for i, N in enumerate(N_lst):
    E = E_lst[i]
    print(*svy21.computeLatLon(N, E))

# N = sum(N_lst)/len(N_lst)
# E = sum(E_lst)/len(E_lst)

# print(N, E)
# print(*svy21.computeLatLon(N, E))
