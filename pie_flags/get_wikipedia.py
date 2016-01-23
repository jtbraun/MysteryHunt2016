import requests
from lxml import html
import urlparse
import re
import os


def getme(url):
    o = urlparse.urlparse(url)
    name = os.path.basename(o.path)
    name = name.replace(':', "_")
    name = name.replace('(', "_")
    name = name.replace(')', "_")
    name = name.replace('%', "_")
    print "GET %s" %  name
    #print name
    if not os.path.exists(name):
        r = requests.get(url)
        with open(name, 'wb') as f:
            f.write(r.content)


if __name__ == "__main__":
    import multiprocessing as mp
    pool = mp.Pool(processes=8)

    rooturl = 'https://en.wikipedia.org/wiki/Flags_of_country_subdivisions'
    r = requests.get(rooturl)
    tree = html.fromstring(r.content)
    urls = []
    # for img in tree.xpath('//img'):
    #     url = urlparse.urljoin(rooturl, img.attrib['src'])
    #     urls.append(url)
    for a in tree.xpath('//a'):
        try:
            url = urlparse.urljoin(rooturl, a.attrib['href'])
            if re.search(r'\.(svg|png)$', url, re.I):
                urls.append(url)
        except KeyError:
            pass
    work = []
    for url in urls:
        if re.search(r'Flag.*\.(png|svg)$', url, re.I):
            work.append(pool.apply_async(getme, [url]))
            pass
    for i in work:
        i.get()
