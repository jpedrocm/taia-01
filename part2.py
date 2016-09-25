import random
import math

NUM_BITS = 3
POPULATION_SIZE = 100
NUM_EVALUATIONS = 10000
NUM_ITERATIONS = 1000
EVALUATION_COUNTER = 0
GEN_CACHE = {}
RANK_SIZE = 5
REPRODUCTION_FOR_CYCLE = 100
CROSSOVER_PROBABILITY = 1
MUTATION_PROBABILITY = 0.3
MUTATION_SIZE = 4
ITERATIONS_PER_EXECUTION = []
CONVERGENT_EXECUTIONS = 0
CONVERGENT_INDIVIDUALS_PER_EXECUTION = []
MEAN_FITNESS_PER_EXECUTION = []
ALL_POP_CONVERGED = []
FITNESS_AVAL_PER_EXECUTION = []

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
        for i in xrange(1,MUTATION_SIZE):
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
        parentRank = [x for x in random.sample(combined_population, RANK_SIZE)]
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
    solutions = 0
    for genome in genomes:
        genome = [int(x, 2) for x in genome]
        solutions += evaluate_genome(genome)
    return solutions
        
def begin_iterations():
    global CONVERGENT_EXECUTIONS
    population = generate_population()
    iteration_counter = 0
    found_solution = False
    while (EVALUATION_COUNTER < NUM_EVALUATIONS and iteration_counter < NUM_ITERATIONS):
        iteration_counter += 1
        parents = select_parents(population)
        children = []
        for i in xrange(1,REPRODUCTION_FOR_CYCLE):
            recombinationResult = crossover(parents[0], parents[1])
            mutation(recombinationResult[0])
            mutation(recombinationResult[1])
            children.append(recombinationResult[0])

        population = select_survivors(population, children)
        number_of_solutions = check_for_solution(population)
        if number_of_solutions and not found_solution:
            found_solution = True
            CONVERGENT_EXECUTIONS += 1
            ITERATIONS_PER_EXECUTION.append(iteration_counter)
            CONVERGENT_INDIVIDUALS_PER_EXECUTION.append(number_of_solutions)
            population_fitness = mean(map(lambda x : fitness(x), population))
            MEAN_FITNESS_PER_EXECUTION.append(population_fitness)
            FITNESS_AVAL_PER_EXECUTION.append(EVALUATION_COUNTER)
            print "Solution found! Stopping after " + str(EVALUATION_COUNTER) + " evaluations and " + str(iteration_counter) + " iterations"
            print "The population mean fitness was " + str(population_fitness)
            print "There were " + str(number_of_solutions) + " convergent individuals"
        if number_of_solutions == len(population):
            ALL_POP_CONVERGED.append(iteration_counter)
            print "All population converged in " + str(iteration_counter) + " iterations"
            return

    print "No solution found after " + str(EVALUATION_COUNTER) + " evaluations and "+ str(iteration_counter) + " iterations"
    ALL_POP_CONVERGED.append(iteration_counter)
    print "Population did not converge"

def mean(list_items):
    return sum(list_items)/len(list_items)

def std_dev(list_items, mean_items):
    variance_list = map(lambda x : pow(x-mean_items, 2), list_items)
    return math.sqrt(sum(variance_list)/len(list_items))

def test_and_evaluate():
    global EVALUATION_COUNTER
    print "PARTE 2"
    for j in range(0, 30):
        print "Execution " + str(j+1)
        EVALUATION_COUNTER = 0
        begin_iterations()
        print " "
    mean_iterations = mean(ITERATIONS_PER_EXECUTION)
    std_dev_iterations = std_dev(ITERATIONS_PER_EXECUTION, mean_iterations)
    mean_individuals = mean(CONVERGENT_INDIVIDUALS_PER_EXECUTION)
    std_dev_individuals = std_dev(CONVERGENT_INDIVIDUALS_PER_EXECUTION, mean_individuals)
    mean_fitness = mean(MEAN_FITNESS_PER_EXECUTION)
    std_dev_fitness = std_dev(MEAN_FITNESS_PER_EXECUTION, mean_fitness)
    mean_converged_population = mean(ALL_POP_CONVERGED)
    std_dev_converged_population = std_dev(ALL_POP_CONVERGED, mean_converged_population)
    mean_fitness_aval = mean(FITNESS_AVAL_PER_EXECUTION)
    std_dev_fitness_aval = std_dev(FITNESS_AVAL_PER_EXECUTION, mean_fitness_aval)
    print "There were " + str(CONVERGENT_EXECUTIONS) + " convergent executions"
    print "Mean of iterations: " + str(mean_iterations)
    print "Standard deviation of iterations: " + str(std_dev_iterations)
    print "Mean of fitness: " + str(mean_fitness)
    print "Standard deviation of fitness: " + str(std_dev_fitness)
    print "Mean of convergent individuals: " + str(mean_individuals)
    print "Standard deviation of individuals: " + str(std_dev_individuals)
    print "Mean of converged population: " + str(mean_converged_population)
    print "Standard deviation of converged population: " + str(std_dev_converged_population)
    print "Mean of fitness avaliation: " + str(mean_fitness_aval)
    print "Standard deviation of fitness avaliation: " + str(std_dev_fitness_aval)

test_and_evaluate()