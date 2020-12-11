import numpy as np

from .svy21 import SVY21

svy21 = SVY21()


latlg_lst = [    
    1.297621, 103.774091,
    1.299145, 103.771294,
]

lat_lst = latlg_lst[::2]
lg_lst = latlg_lst[1::2]


lat = lat_lst[0]
lg = lg_lst[0]
x1, y1 = svy21.computeSVY21(lat, lg)

lat = lat_lst[1]
lg = lg_lst[1]
x2, y2 = svy21.computeSVY21(lat, lg)

print(np.sqrt((x1-x2)**2 + (y1-y2)**2))
