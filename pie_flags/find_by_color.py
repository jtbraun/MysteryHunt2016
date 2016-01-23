from PIL import Image
import glob
from itertools import *
import re

search = set()
#search.add((0xff, 0xff, 0xff, 0xff))
#search.add((0xf6, 0xc5, 0x0a, 0xff))
#search.add((0x2d, 0x55, 0x8e, 0xff))
#search.add((0xe2, 0x40, 0x1e, 0xff))


search.add((0xff,0xff,0xff,0xff))
search.add((0x74,0xac,0xdf,0xff))
search.add((0x00,0x80,0x33,0xff))

for f in glob.glob('*.*'):
    if not re.search(r'\.(png|svg)$', f, re.I):
        continue
    try:
        im = Image.open(f)
    except IOError:
        continue
    pix = im.load()

    found = set()
    for x, y in product(*[xrange(i) for i in im.size]):
        p = pix[x,y]
        if p in search:
            found.add(p)
        if len(found) == len(search):
            print f
            break
