import random
import math

NUM_BITS = 3
POPULATION_SIZE = 100
NUM_ITERATIONS = 10000
RANK_SIZE = 5
CROSSOVER_PROBABILITY = 0.9
MUTATION_PROBABILITY = 0.4

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

def crossfill(parent, child, point):
    hashTable = buildChildHash(child)
    right = parent[point:]
    for i in range(len(right)):
        if not hashTable[int(right[i], 2)]:
            child.append(right[i])

    if len(child) != len(parent):
        left = parent[0:point]
        for i in range(len(left)):
            if not hashTable[int(left[i], 2)]:
                child.append(left[i])

def crossover(parent1, parent2):
    pc = random.random()
    if pc < CROSSOVER_PROBABILITY:
        crossoverPoint = random.randint(0, len(parent1))
        child1 = parent1[0:crossoverPoint]
        child2 = parent2[0:crossoverPoint]
        crossfill(parent1, child2, crossoverPoint)
        crossfill(parent2, child1, crossoverPoint)
        return [child1, child2]
    else:
        return [parent1, parent2]

def mutation(child):
    pm = random.random()
    if pm < MUTATION_PROBABILITY:
        bit1 = random.randint(0, len(child) - 1)
        bit2 = random.randint(0, len(child) - 1)
        child[bit1], child[bit2] = child[bit2], child[bit1]

def fitness(gen):
    sz = len(gen)
    fit = 0
    for i in xrange(0, sz):
        vali = int(gen[i],2)
        for j in xrange(i, sz):
            valj = int(gen[j], 2)
            valDiff = abs(valj - vali)
            indexDiff = (j - i)
            if(valDiff == indexDiff):
                fit += 1
    return fit

def select_survivors(population, children):
    new_population = population + children
    new_population.sort(key = lambda x : fitness(x), reverse=True)
    new_population = new_population[:-2]
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
    for i in range(NUM_ITERATIONS):
        parents = select_parents(population)
        children = crossover(parents[0], parents[1])
        mutation(children[0])
        mutation(children[1])
        if check_for_solution(children):
            print "Solution found! Stopping in iteration #" + i
            return
        population = select_survivors(population, children)
    print "No solution found after " + str(NUM_ITERATIONS) + " iterations"

begin_iterations()