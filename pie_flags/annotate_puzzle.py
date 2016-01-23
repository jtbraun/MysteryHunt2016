from PIL import Image, ImageDraw, ImageFont
import glob
import sys
import numpy as np
from pprint import pprint
import os

R = 198
N = int(2*np.pi*R)*2
for name in glob.glob('L*.png'):
    print name
    im = Image.open(name)
    pix = im.load()

    theta = np.linspace(0, 2*np.pi, N, endpoint = False) + (2*np.pi/N/2)
    cos = np.cos(theta)
    sin = np.sin(theta)

    c = np.array(im.size) / 2
    coords = c + R * np.array([np.cos(theta), -np.sin(theta)]).T
    samples = {}
    last = None
    slist = []
    for x, y in coords:
        val = pix[x,y]
        samples.setdefault(val,0)
        if samples[val] == 0:
            slist.append(val)
        samples[val] += 1
    print samples

    im = im.copy()
    d = ImageDraw.Draw(im)
    y = 20
    x = 20
    B = 20

    #  fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)

    for sample in slist:
        print sample, samples[sample]
        d.rectangle(((x,y), (x+B,y+B)), fill=sample)
        d.rectangle(((x+B,y), (x+B+150,y+B)), fill=(0,0,0))
        d.text((x + int(B * 1.2),y), "%7.2f%% #%02x%02x%02x" % (float(samples[sample])*100/N, sample[0], sample[1], sample[2]), fill=(255,255,255))
        y += int(B * 1.2)

    im.save('anno_' + name)
