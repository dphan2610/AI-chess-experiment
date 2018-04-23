import time
from multiprocessing import Pool
from simulation_runner import run_simulation
from file_utility import combine
from analyzer import analyze

if __name__ == '__main__':
    processes = 9
    simulation_runs = 100000
    times = int(simulation_runs / processes)
    
    list = []
    name = 'chess-parallel-'
    for x in range(processes):
        list.append((times, name + str(x)))
        
    with Pool(processes) as p:
        times = int(simulation_runs / processes)
        
        start = time.time()
        p.starmap(run_simulation, list)
        
        end = time.time()
        print ('Time elapsed: ', end - start)

    f_list = []
    for x in list:
        f_list.append(x[1])
    print (f_list)
    combine(f_list, 'chess-simulation-records')
    analyze('chess-simulation-records')
