#!/usr/bin/python3
from sklearn.cluster import KMeans
from io import BytesIO
from PIL import Image
import requests
import numpy
import json
import sys


def GetHttpsUrl(url):
    return 'https://' + url.split("://")[-1]

def GetImageFromHttpsUrl(httpsUrl):
    resp = requests.get(httpsUrl)
    img = Image.open(BytesIO(resp.content)).resize((64, 64)).convert('RGB')
    return img
    

for line in sys.stdin:
    meta = json.loads(line)
    httpsUrl = GetHttpsUrl(meta['imUrl'])
    genre = meta['root-genre']
    img = GetImageFromHttpsUrl(httpsUrl)  
    rgbs = numpy.array(img)
    rgbs_vec = rgbs.reshape((rgbs.shape[0] * rgbs.shape[1], 3))
    # print(img)  
    clt = KMeans(n_clusters=2, max_iter = 10)
    clt.fit(rgbs_vec)
    print(clt.cluster_centers_)    




