import re
import os
import glob
import natsort
import json
import colorsys
from lxml import html
import numpy as np
import matplotlib.pyplot as plt
#import spacex.mpl.utilities as sxmplu

outdir = 'luminance-cache'
data_hls = []
data_rgb = []
for path in natsort.natsorted(glob.glob(outdir + '/*')):
    with open(path) as f:
        els = html.fromstring(json.load(f)['rawhtml']).xpath('//td')
        styles = [el.attrib['style'] for el in els]
        styles = [re.sub(r'.*#([0-9A-Fa-f]{6}).*', r'\1', s) for s in styles]


        colors = [ (int(s[0:2], 16)/255., int(s[2:4], 16)/255., int(s[4:6], 16)/255.) for s in styles ]
        # ignore green, it's for ordering
        colorshls = [ colorsys.rgb_to_hls(c[0], 0., c[2]) for c in colors ]
        # for i, c in enumerate(colors):
        #     print c
        #     print "A", colorsys.rgb_to_hls(*c)
        #     print "B", colorsys.rgb_to_hls(c[0], c[1], c[2])
        #     print "C", colorshls[i]
        # print
        # print colorsys.hsv_to_rgb(0.5, 0.5, 0.4)
        # sys.exit()

        data_rgb.append(colors)
        data_hls.append(colorshls)
data_rgb = np.array(data_rgb)
data_hls = np.array(data_hls)



fig, axs_rgb = plt.subplots(3, 1, sharex=True)
plt.tight_layout()
fig, axs_hls = plt.subplots(3, 1, sharex=True)
plt.tight_layout()
for data, axs, labels in [(data_rgb, axs_rgb, ['red', 'green', 'blue']),
                          (data_hls, axs_hls, ['hue', 'luminance', 'saturation'])]:
    for index, (ax, label) in enumerate(zip(axs, labels)):
        dat = data[..., index]
        print dat.shape
        sq_start = 0
        sq_end = dat.shape[-1]
        sq_start = 6
        sq_end = sq_start + 3
        ax.set_ylabel(label)
        ax.set_ylim(0, 1)
        #ax.set_xticks(np.arange(dat.shape[0]), minor=True)

        for sq in xrange(sq_start, sq_end):
            ax.plot(dat[:,sq])

r_periods = np.array([[  36.,  321.,  369.,   17.,  221.,  272.,  392.,  476.],
                      [ 135.,  151.,  235.,  286.,  301.,  404.,  489.,  624.,],
                      [ 640.,   83.,  270.,  335.,  141.,  283.,  451.,   64.,],
                      [  18.,  267.,  321.,  438.,   51.,  129.,  244.,  412.,],
                      [ 502.,  333.,   97.,  154.,  133.,  205.,  205.,  257.,]])

r_periods = np.array([[  36.,   322.,   370.,    17.,   220.,   273.,   393.,   476.,],
                      [ 136.,   152.,   236.,   286.,   304.,   406.,   490.,   626.,],
                      [ 640.,    84.,   272.,   336.,   143.,   284.,   451.,    65., ],
                      [  18.,   268.,   322.,   439.,    52.,   129.,   245.,   413., ],
                      [ 500.,   333.,    98.,   156.,   135.,   206.,   206.,   258., ]])

# b_periods = np.array([[  36.,  321.,  369.,   17.,  219.,  272.,  392.,  476.,],
#                       [ 135.,  151.,  235.,  286.,  303.,  404.,  489.,  624.,],
#                       [ 641.,   83.,  270.,  335.,  142.,  283.,  451.,   64.,],
#                       [  18.,  267.,  321.,  438.,   51.,  129.,  244.,  412.,],
#                       [ 502.,  332.,   97.,  154.,  134.,  205.,  206.,  257.,]])


fig, axs = plt.subplots(5, 8, sharex=True, sharey=True)
axs = axs.ravel()
R = data_rgb[...,0]
G = data_rgb[...,1]
B = data_rgb[...,2]
given_periods = r_periods.ravel()
for sq, ax in enumerate(axs):
    r = R[...,sq]
    b = B[...,sq]
    per = given_periods[sq] * 2
    ax.plot(r[:per],b[:per])

fig, axs = plt.subplots(5, 8, sharex=True, sharey=True)
axs = axs.ravel()
for data_src, color, idx, given_periods in [
        #(data_rgb, 'red', 0, r_periods),
        #(data_rgb, 'blue', 2, b_periods),
        (data_hls, 'luminance', 1, r_periods)]:
    periods = []
    given_periods = given_periods.ravel()
    for sq, ax in enumerate(axs):
        # plot color data
        y = data_src[:,sq,idx]


        i = 5
        if False:
            ax.plot(y)
        elif False:
            z = []
            print "convolving", sq, len(y)
            for delay in xrange(1, len(y)/10):
                a = y[delay:]
                b = y[:-delay]
                z.append(np.dot(a,b)/len(a))
            ax.plot(z)

            baseline = z[0]
            assert z[i] < baseline
            # find the first min
            while z[i] > z[i+1]:
                i += 1
            # find first big hump
            while z[i] < .9 * z[0]:
                i += 1
            while z[i] <= z[i+1]:
                i += 1
            print "SQUARE", sq, "delay", i, given_periods[sq]
            ax.plot([i, i], [np.min(z), np.max(z)], 'ro-')
        elif False:
            # alternate period finding
            i = 0
            samples =[]
            m = np.min(y)
            try:
                while True:
                    while not np.isclose(y[i], m):
                        i += 1
                    while np.isclose(y[i], m):
                        i += 1
                    start = i
                    while not np.isclose(y[i], m):
                        i += 1
                    while np.isclose(y[i], m):
                        i += 1
                    end = i
                    samples.append(end-start)
            except IndexError:
                pass
            print "FOR SQUARE", sq, "DELAY", np.mean(samples), np.median(samples)
            i = np.median(samples)
            a = y[i:]
            b = y[:-i]
            for x in [a, b]:
                ax.plot(np.linspace(0, 1, 2*i), x[:2*i])
        elif True:
            align = True
            offset = 0
            m = np.min(y)
            if align:
                i = 5
                while not np.isclose(y[i], m):
                    i += 1
                while np.isclose(y[i], m):
                    i += 1
                offset = i
            i = given_periods[sq]
            a = y[i+offset:]
            b = y[offset:-i]
            linestyle = '-'
            if i < 50:
                linestyle += 'x'
            for x in [a, b]:
                ax.plot(np.linspace(0, 1, 3*i), x[:3*i], linestyle)

        periods.append(i)
    periods = np.array(periods, dtype=float)
    periods = periods.reshape((5, 8))
    print "PERIODS", color
    print periods
    print "NEW PERIODS"





rates = []
for i in xrange(G.shape[-1]):
    y = G[700:850,i]
    last = y[0]
    count = -1
    counts = []
    for j in y:
        if np.isclose(j, last):
            if count >= 0:
                count += 1
        else:
            if count >= 0:
                #print count,
                counts.append(count)
            count = 0
            last = j
    rate = np.median(counts)
    # print "CELL", i, "INCPERIOD", rate, counts
    rates.append(rate)
rates = np.array(rates).reshape((-1,8))
print "GREEN DELAYS"
print rates

plt.show()
