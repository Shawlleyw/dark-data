#!/usr/bin/python3

import sys
from sklearn.cluster import KMeans
import numpy as np
import tqdm as tqdm
import json


def get_3dim_coords(coord_str):
    coords = coord_str.split(',')
    return [int(coords[0]), int(coords[1]), int(coords[2])]


def vec3d_to_str(vec3):
    return "%d;%d;%d" % (int(vec3[0]), int(vec3[1]), int(vec3[2]))


def dump_to_json(genre, length, vec3s):
    hues = []
    for vec3 in vec3s:
        hues.append(vec3d_to_str(vec3))

    jsonItem = {
        "genre": genre,
        "size": length,
        "hues": hues,
    }
    return json.dumps(jsonItem)


type_arr = dict()


for line in sys.stdin:
    type = line.split(':')[0].strip(' \t\n[](){}')
    # print(type)
    coords = line.split(':')[-1]
    coord_1 = get_3dim_coords(coords.split(';')[0].strip('\n[](){}'))
    coord_2 = get_3dim_coords(coords.split(';')[-1].strip('\n[](){}'))
    # print(coord_1, coord_2)
    if type_arr.get(type) == None:
        type_arr[type] = [coord_1, coord_2]
    else:
        type_arr[type].append(coord_1)
        type_arr[type].append(coord_2)


for type, list in type_arr.items():
    rgbs_vec = np.array(list)
    clt = KMeans(n_clusters=4, max_iter=100)
    clt.fit(rgbs_vec)
    print(dump_to_json(type, len(list), clt.cluster_centers_))
