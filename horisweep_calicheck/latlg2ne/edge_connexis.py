
from .svy21 import SVY21

svy21 = SVY21()

coord_lst = [
    31248.104, 22840.769, 17.019,
    31248.097, 22840.779, 17.039,
    31248.103, 22840.777, 17.034,
]
N_lst = coord_lst[::3]
E_lst = coord_lst[1::3]
ele_lst = coord_lst[2::3]

N = sum(N_lst)/len(N_lst)
E = sum(E_lst)/len(E_lst)
ele = sum(ele_lst)/len(ele_lst)

print(N, E, ele)
print(*svy21.computeLatLon(N, E), ele)


print('')

latlg_lst = [
    1.298679, 103.787901,
    1.29899, 103.787085,
    1.2998, 103.787608,
]

lat_lst = latlg_lst[::2]
lg_lst = latlg_lst[1::2]

for i, lat in enumerate(lat_lst):
    lg = lg_lst[i]
    print(*svy21.computeSVY21(lat, lg))
