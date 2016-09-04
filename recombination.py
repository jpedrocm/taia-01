import random
import copy
# Code for part 2

def nextPosition(hashP, index,gen):
    szGen = len(gen)
    if(index < szGen):
        value = int(gen[index],2)
    else:
        return index

    while(hashP[value] and index < szGen):        
        index+=1
        value = int(gen[index],2)
    
    return index

def previousPosition(hashP, index,gen):
    szGen = len(gen)
    if(index >= 0):
        value = int(gen[index],2)
    else:
        return index
    while(hashP[value] and index >=0):
        index-=1
        value = int(gen[index],2)
    
    return index

def transa(c1,c2):
    sz = len(c1)
    c3 = [0 for i in range(sz)]
    hashT = [False for i in range(sz+1)]
    ci1 = 0
    ci2 = sz - 1
    for i in range(4):
        ci1 = nextPosition(hashT,ci1, c1)
        if (ci1 < sz):
            c3[i] = c1[ci1]
            hashT[int(c1[ci1],2)] = True
        ci2 = previousPosition(hashT,ci2, c2)
        if (ci2 < sz):
            c3[sz-i-1] = c2[ci2]
            hashT[int(c2[ci2],2)] = True
 
    return c3

def crossOver(c1,c2):
    pos = random.randint(0,7)
    c3 = []
    for i in xrange(0,8):
        if (i < pos):
            c3.append(c1[i])
        else:
            c3.append(c2[i])

    return c3

       


 
state = ['000','001','010','011','100','101','110','111']
population = []
 
for i in range(10):
    random.shuffle(state)
    population.append(copy.copy(state))
 
print population[1]
print population[2]
print transa(population[1],population[2])
print transa(population[2],population[1])

print crossOver(population[1],population[2])
print crossOver(population[2],population[1])