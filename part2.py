import random
import math

NUM_BITS = 3
POPULATION_SIZE = 100
NUM_EVALUATIONS = 10000
EVALUATION_COUNTER = 0
GEN_CACHE = {}
RANK_SIZE = 5
REPRODUCTION_FOR_CYCLE = 10
CROSSOVER_PROBABILITY = 1
MUTATION_PROBABILITY = 0.4

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

def recombination(c1,c2):
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

def crossover(c1,c2):
    pc = random.random()
    if pc < CROSSOVER_PROBABILITY:
        return [recombination(c1,c2),recombination(c2,c1)]
    else:
        return [c1,c2]

def generate_chains(length, chain, chains):
    if length < 1:
        chains.append(chain)
    else:
        next = (chain + '0', chain + '1')
        generate_chains(length - 1, next[0], chains)
        generate_chains(length - 1, next[1], chains)
    
def generate_population():
    chains = list()
    generate_chains(NUM_BITS, '', chains)
    population = list()
    for i in range(POPULATION_SIZE):
        random.shuffle(chains)
        population.append(list(chains))
    return population

def select_parents(population):
    parentRank = [x for x in random.sample(population, RANK_SIZE)]
    parentRank.sort(key=lambda x : fitness(x), reverse=True)
    return parentRank[0:2]

def buildChildHash(child):
    maxValue = 2**NUM_BITS
    hashTable = [False for i in range(maxValue)]
    for i in range(len(child)):
        hashTable[int(child[i], 2)] = True
    return hashTable

def mutation(child):
    pm = random.random()
    if pm < MUTATION_PROBABILITY:
        bit1 = random.randint(0, len(child) - 1)
        bit2 = random.randint(0, len(child) - 1)
        child[bit1], child[bit2] = child[bit2], child[bit1]

def hashState(gen):
    string = ""
    sz = len(gen)
    for i in xrange(0,sz):
        string += gen[i]
    return string
        
def fitness(gen):
    global EVALUATION_COUNTER
    genHash = hashState(gen)
    if genHash in GEN_CACHE.keys():
        return GEN_CACHE[genHash]

    EVALUATION_COUNTER = EVALUATION_COUNTER + 1
    sz = len(gen)
    fit = 0
    for i in xrange(0, sz):
        vali = int(gen[i], 2)
        for j in xrange(i, sz):
            valj = int(gen[j], 2)
            valDiff = abs(valj - vali)
            indexDiff = (j - i)
            if(valDiff != indexDiff):
                fit += 1
    GEN_CACHE[genHash] = fit
    return fit

def select_survivors(population, children):
    combined_population = population + children
    combined_population.sort(key = lambda x : fitness(x), reverse=True)
    new_population = []
    for x in xrange(0,POPULATION_SIZE):
        parentRank = [x for x in random.sample(population, RANK_SIZE)]
        parentRank.sort(key=lambda x : fitness(x), reverse=True)
        new_population.append(parentRank[0])
    
    random.shuffle(new_population)
    return new_population

def evaluate_genome(genome):
    size = len(genome)
    for i in range(size):
        for j in range(i + 1, size):
            # By the problem definition, there won't be any queens
            # in the same line or column. Thus, we only check for
            # diagonals.
            if abs(genome[j] - genome[i]) == j - i:
                return False;
    return True;

def check_for_solution(genomes):
    for genome in genomes:
        genome = [int(x, 2) for x in genome]
        if evaluate_genome(genome):
            return True
    return False
        
def begin_iterations():
    population = generate_population()
    iteration_counter = 0
    while (EVALUATION_COUNTER < NUM_EVALUATIONS):
        iteration_counter += 1
        parents = select_parents(population)
        children = []
        for i in xrange(1,REPRODUCTION_FOR_CYCLE):
            recombinationResult = crossover(parents[0], parents[1])
            mutation(recombinationResult[0])
            mutation(recombinationResult[1])
            children.append(recombinationResult[0])

        if check_for_solution(children):
            print "Solution found! Stopping after " + str(EVALUATION_COUNTER) + " evaluations and " + str(iteration_counter) + " iterations"
            return
        population = select_survivors(population, children)

    print "No solution found after " + str(EVALUATION_COUNTER) + " evaluations and "+ str(iteration_counter) + " iterations"

begin_iterations()