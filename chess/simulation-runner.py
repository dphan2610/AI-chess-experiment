from utility import simulation
import sys

def run_simulation(times, file_output):
    f = open(file_output, 'w')
    sys.stdout = f
    simulation(times)
    f.close()
