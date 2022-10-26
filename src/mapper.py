#!/usr/bin/python3
from sklearn.cluster import KMeans
from io import BytesIO
from PIL import Image
import requests
import numpy
import json
import sys
import os
from tqdm import tqdm


def GetHttpsUrl(url):
    return 'https://' + url.split("://")[-1]


def GetImageFromHttpsUrl(httpsUrl):
    resp = requests.get(httpsUrl)
    img = Image.open(BytesIO(resp.content)).resize((64, 64)).convert('RGB')
    return img

lines = []

for line in sys.stdin:
    lines.append(line.strip())

imgFmts = ['jpg', 'jpeg', 'png']    
    
with open("err.log", "w") as f:
    for line in tqdm(lines):
        try: 
            meta = json.loads(line)
            httpsUrl = GetHttpsUrl(meta['imUrl'])
            genre = meta['root-genre']
            imgFmt = httpsUrl.split('.')[-1]
            if imgFmt not in  imgFmts:
                print("won't fetch " + imgFmt, file=sys.stderr)
                continue
            img = GetImageFromHttpsUrl(httpsUrl)
            rgbs = numpy.array(img)
            rgbs_vec = rgbs.reshape((rgbs.shape[0] * rgbs.shape[1], 3))
            # print(img)
            clt = KMeans(n_clusters=2, max_iter=10)
            clt.fit(rgbs_vec)
            res = clt.cluster_centers_
            print("%s:(%d,%d,%d);(%d,%d,%d)" % (genre, res[0][0], res[0][1], res[0][2], res[1][0], res[1][1], res[1][2]))
        except:
            f.write(httpsUrl+'\n')
