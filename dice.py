"""
Created on 16 May 2020
@author: John Thomas
"""
import random
import re


def roll_pool(command):
    dice = int(re.search('[0-9]+', command).group())
    modifiers = list(command)
    pool = []
    hits = 0
    wild = False
    explode = False
    wild_val = 0
    twos_glitch = False
    explosions = 0
    if "w" in modifiers:
        wild = True
    if "e" in modifiers:
        explode = True
    if "!" in  modifiers:
        twos_glitch = True
    print("Wild: " + str(wild) + " Explode: " + str(explode) + " Twos Glitch: " + str(twos_glitch))
    for d in range(dice if wild == False else dice - 1):
        val = random.randint(1, 6)
        pool.append(val)
        if explode:
            while val == 6:
                explosions += 1
                val = random.randint(1, 6)
                pool.append(val)
    if wild:
        wild_val = random.randint(1, 6)
      
    pool.sort()
    hits = get_hits(pool, wild_val)
    print("Pool: " + str(pool) + " Wild: " + str(wild_val) + " Hits: "
         + str(hits) + " Explosions: " + str(explosions) + " Glitch: " + str(is_glitch(pool)))
    return pool, wild_val, hits, is_glitch(pool, "!" if twos_glitch else None)

def get_hits(pool, wild = 0):
    hits = 0
    for d in range(len(pool)):
        if pool[d] >= 5:
            hits += 1
    if wild >= 5:
        hits += 3
    return hits

def is_glitch(pool, *args):
    glitches = 0
    for d in range(len(pool)):
        if pool[d] == 1:
            glitches += 1
        if "!" in args and pool[d] == 2:
            glitches += 1
    print("Glitches: " + str(glitches))
    if glitches > len(pool) / 2:
        return True
    else:
        return False

#roll_pool("17w")
#s_glitch([1,2,2,3,4,5], "!")

            

