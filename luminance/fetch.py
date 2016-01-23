import time
import os
import requests
from lxml import html
url = 'http://ysera-iozyrwndwd.muttsteryhunt.com/puzzle/luminance_shift/'
url = 'http://dynamic.muttsteryhunt.com/dynamic/puzzle/luminance_shift/get_html'
outdir = 'luminance-cache'
if not os.path.exists(outdir):
    os.mkdir('luminance-cache')
last = None
counter = 0
while True:
    txt = requests.get(url).content
    if last != txt:
        name = os.path.join(outdir, '%d.json' % counter)
        with open(name, 'w') as f:
            counter += 1
            f.write(txt)
        last = txt
        print "WROTE", name
    else:
        print "SAME"
    time.sleep(0.1)
