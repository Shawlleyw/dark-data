#!/usr/bin/python3

import matplotlib.pyplot as plt
import json
import numpy as np
import sys


def str_to_vec3(hue):
    vec3 = hue.split(';')
    return (int(vec3[0].strip())/255, int(vec3[1].strip())/255, int(vec3[2].strip())/255)


genres = []
sizes = []
rgbs = [[], [], [], []]

for line in sys.stdin:
    item = json.loads(line)
    genre = item.get('genre')
    size = int(item.get('size'))
    hues = item.get('hues')

    i = 0
    for hue in hues:
        rgbs[i].append(str_to_vec3(hue))
        i += 1
    genres.append(genre)
    sizes.append(size)

plt.xticks(fontsize=12, rotation=90)
width = [0.32, 0.24, 0.16, 0.08]
# print(genres, sizes)
x = list(range(len(genres)))
plt.bar(x, sizes,  width=width[0], color=rgbs[0])

y = [i + 0.28 for i in x]
plt.bar(y, sizes, width=width[1], tick_label=genres, color=rgbs[1])

z = [i + 0.2 for i in y]
plt.bar(z, sizes, width=width[2], color=rgbs[2])

t = [i + 0.12 for i in z]
plt.bar(t, sizes, width=width[3], color=rgbs[3])
plt.subplots_adjust(bottom=0.35)
plt.savefig('./res.png')
