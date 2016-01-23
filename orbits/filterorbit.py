
word = 'TROUBLE'
word = 'OKLAHOMA'
word = 'DIVORCE'
word = 'MICKEYMOUSE'
word = 'METHODOFLOVE'
word = 'LIFEGOESON'
word = 'BINGO'
word = 'YMCA'


ring = []
sync = True
occurence = 0
lastgood = 0
doskip = 0
with open('orbits.txt') as f:
    for lineno, line in enumerate(f):
        line = line[:-1]
        ring.append(line)

        if sync and not doskip:
            i = 0
            if word[i] in line:
                sync = False
            else:
                #print "SYNC", line
                if occurence > 0:
                    print word, occurence
                occurence = 0

        if not sync:
            if word[i] in line:
                i += 1
                if i == len(word):
                    sync = True
                    occurence += 1
                    skipped = lineno - lastgood - len(word)
                    if skipped > 0:
                        ok = False
                        if skipped == len(word)-1:
                            ok = True
                            for c, oldline in zip(word[1:], ring[-skipped:]):
                                if c not in oldline:
                                    ok = False
                                    break
                            if ok:
                                print "\tMISSED HEAD!!!!!!"

                        if not ok:
                            print "  skip", skipped
                            print '\t' + '\n\t'.join(ring[-skipped:])
                    print word, occurence
                    lastgood = lineno
            else:
                #print "RESYNC no", word[i], 'in', line
                sync = True
                occurence = 0
