from multiprocessing import Pool
from random import randint
from ast import literal_eval
import cycle as cycle
import portalocker

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def set_broadcast2(population, sortedEvaluatedPopulation, islandNumber, percentageOfBestIndividualsForMigrationPerIsland):   # Joon
    allBests = []
    for i in range(int((len(population))*percentageOfBestIndividualsForMigrationPerIsland)):
        allBests.append([population[sortedEvaluatedPopulation[i][5]], [sortedEvaluatedPopulation[i][0]]])
    file = open('island_files/broadcast.txt', 'r+')
    portalocker.lock(file, portalocker.LOCK_EX)
    prevBests = []
    for line in nonblank_lines(file):
        prevBests.append(literal_eval(line))
    prevBests.extend(allBests)
    for ini in range(len(prevBests)):
        file.write(str(prevBests[ini]) + '\n')
    file.close()

def creator(var):
    plot = open('island_files/plotting_{0}.txt'.format(var), 'w')
    plot.close()

def create_island(num_islands, num_threads):
    broad = open('island_files/broadcast.txt', 'w')
    broad.close()
    migra = open('island_files/migrationN.txt', 'w')
    migra.write(str(1) + '\n')
    migra.close()
    p = Pool(num_threads)
    p.map(creator, num_islands)
    p.close()

def isMigrationNeed():
    migraNeed = []
    with open('island_files/migrationN.txt', 'r') as f:
        for line in f:
            migraNeed.append(literal_eval(line))
    return migraNeed[0]

def reset_broadcast():
    file = open('island_files/broadcast.txt', 'w')
    file.close()

def mig_time():
    print('Migration time')
    return

def do_migration2(island_content, island_number, island_fitness, mig_policy_size):
    if isMigrationNeed() == 0:
        return
    else:
        best_gen_list = []
        with open('island_files/broadcast.txt', 'r') as broad2:
            for line in nonblank_lines(broad2):
                best_gen_list.append(literal_eval(line))
        broad2.close()
        worst_gen_list = []
        count = 0
        for individuo in range(len(island_fitness)):
            worst_gen_list.append([island_fitness[individuo], count])
            count += 1
        print('Migrating', island_number)
        sorted_worst_gen_list = sorted(worst_gen_list, reverse=False, key=cycle.takeFirst)
        iter = 0
        while iter < mig_policy_size*(len(island_content)):
            random_best_gen = randint(0, len(best_gen_list)-1)
            worst_fit = sorted_worst_gen_list[iter][0]
            best_fit = best_gen_list[random_best_gen][1]
            if worst_fit < best_fit[0]:
                island_content[sorted_worst_gen_list[iter][1]] = best_gen_list[random_best_gen][0]
            iter = iter + 1
        print('Migration', island_number, 'concluded')
        return