import random
import copy
# Code for part 2

def nextPosition(hashP, index,gen):
    szGen = len(gen)
    if(index >= szGen):
        index %= szGen
        
    value = int(gen[index],2)
    while(hashP[value] and index < szGen):        
        index = (index + 1) % szGen
        value = int(gen[index],2)
    
    return index

def previousPosition(hashP, index,gen):
    szGen = len(gen)
    if(index < 0):
        index %= szGen

    value = int(gen[index],2)
    while(hashP[value] and index >=0):
        index = (index -1) % szGen
        value = int(gen[index],2)
    
    return index

def transa(c1,c2):
    sz = len(c1)
    c3 = [0 for i in range(sz)]
    hashT = [False for i in range(sz+1)]
    ci1 = 0
    ci2 = sz-1
    for i in range(sz/2):
        ci1 = nextPosition(hashT,ci1, c1)
        if (ci1 < sz):
            c3[i] = c1[ci1]
            hashT[int(c1[ci1],2)] = True
    
    for i in range(sz/2):
        ci2 = previousPosition(hashT,ci2, c2)
        if (ci2 < sz):
            c3[sz-i-1] = c2[ci2]
            hashT[int(c2[ci2],2)] = True
 
    return c3

def crossOver(c1,c2):
    sz = len(c1)
    pos = random.randint(0,sz-1)
    c3 = []
    hashT = [False for i in range(sz+1)]
    index = pos + 1
    for i in xrange(0,sz):
        if (i <= pos):
            c3.append(c1[i])
            hashT[int(c1[i],2)] = True
        else:
            while hashT[int(c2[index],2)]:
                index = (index +1) % sz
            c3.append(c2[index])
            index = (index +1) % sz
            
    return c3
 

def fitness(gen):
    sz = len(gen)
    fit = 0
    for i in xrange(0,sz):
        vali = int(gen[i],2)
        for j in xrange(i,sz):
            valj = int(gen[j],2)
            valDiff = abs(valj - vali)
            indexDiff = (j - i)
            if(valDiff == indexDiff):
                fit += 1

    return fit
        

state = ['000','001','010','011','100','101','110','111']
population = []
 
for i in range(10):
    random.shuffle(state)
    population.append(copy.copy(state))
 
print population[1]
print fitness(population[1])
print population[2]
print fitness(population[2])

t1 = transa(population[1],population[2])
t2 = transa(population[2],population[1])

print t1
print fitness(t1)
print t2
print fitness(t2)

c1 = crossOver(population[1],population[2])
c2 = crossOver(population[2],population[1])

print c1
print fitness(c1)
print c2
print fitness(c2)
