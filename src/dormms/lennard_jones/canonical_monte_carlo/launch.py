"""
Example single-site Lennard-Jones canonical ensemble Monte Carlo simulation using FEASST.
Run multiple densities using multiple processors/nodes/restarts, and plot results.
Compare with T*=0.9 in https://mmlapps.nist.gov/srs/LJ_PURE/mc.htm.
Note that checkpoints and restarts happen quicker than usual in these tutorial for testing purposes.

Usage: python /path/to/feasst/tutorial/launch.py
Options: python /path/to/feasst/tutorial/launch.py --help
"""

import argparse
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from pyfeasst import fstio

# Parse arguments from command line or change their default values.
PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument('--feasst_install', type=str, default='feasstv0.25.1/build/',
                    help='FEASST install directory (e.g., the path to build)')
PARSER.add_argument('--fstprt', type=str, default='/feasst/particle/lj.fstprt',
                    help='FEASST particle definition')
PARSER.add_argument('--num_particles', type=int, default=500, help='number of particles')
PARSER.add_argument('--trials_per_iteration', type=int, default=int(1e5),
                    help='like cycles, but not necessary num_particles')
PARSER.add_argument('--equilibration_iterations', type=int, default=int(5e2),
                    help='number of iterations for equilibraiton')
PARSER.add_argument('--production_iterations', type=int, default=int(2.5e3),
                    help='number of iterations for production')
PARSER.add_argument('--hours_checkpoint', type=float, default=1, help='hours per checkpoint')
PARSER.add_argument('--hours_terminate', type=float, default=5*24, help='hours until termination')
PARSER.add_argument('--run_type', '-r', type=int, default=1,
                    help='0: run, 1: submit to queue, 2: post-process')
PARSER.add_argument('--seed', type=int, default=73867027,
                    help='Random number generator seed. If -1, assign random seed to each sim.')
PARSER.add_argument('--max_restarts', type=int, default=2, help='Number of restarts in queue')
PARSER.add_argument('--num_nodes', type=int, default=1, help='Number of nodes in queue')
PARSER.add_argument('--scratch', type=str, default=None,
                    help='Optionally write scheduled job to scratch/logname/jobid.')
PARSER.add_argument('--queue_flags', type=str, default="", help='extra flags for queue (e.g., for slurm, "-p queue")')
PARSER.add_argument('--node', type=int, default=0, help='node ID')
PARSER.add_argument('--queue_id', type=int, default=-1, help='If != -1, read args from file')
PARSER.add_argument('--queue_task', type=int, default=0, help='If > 0, restart from checkpoint')

# Convert arguments into a parameter dictionary, and add argument-dependent parameters.
ARGS, UNKNOWN_ARGS = PARSER.parse_known_args()
assert len(UNKNOWN_ARGS) == 0, 'An unknown argument was included: '+str(UNKNOWN_ARGS)
PARAMS = vars(ARGS)
PARAMS['prefix'] = 'lj'
PARAMS['script'] = __file__
PARAMS['sim_id_file'] = PARAMS['prefix']+ '_sim_ids.txt'
PARAMS['minutes'] = int(PARAMS['hours_terminate']*60) # minutes allocated on queue
PARAMS['hours_terminate'] = 0.99*PARAMS['hours_terminate'] - 0.0333 # terminate before queue
PARAMS['procs_per_sim'] = 1
PARAMS['temperatures'] = [0.85]*10+[0.9]*10
PARAMS['procs_per_node'] = len(PARAMS['temperatures'])
PARAMS['num_sims'] = PARAMS['num_nodes']*PARAMS['procs_per_node']
PARAMS['densities'] = [0.001, 0.003, 0.005, 0.007, 0.009, 0.776, 0.78, 0.82, 0.86, 0.9]*2
PARAMS['cubic_side_lengths'] = np.power(PARAMS['num_particles']/np.array(PARAMS['densities']), 1./3.).tolist()
def sim_node_dependent_params(params):
    """ Set parameters that depend upon the sim or node here. """
    params['cubic_side_length'] = params['cubic_side_lengths'][params['sim']]
    params['beta'] = 1./params['temperatures'][params['sim']]

def write_feasst_script(params, script_file):
    """ Write fst script for a single simulation with keys of params {} enclosed. """
    with open(script_file, 'w', encoding='utf-8') as myfile:
        myfile.write("""
MonteCarlo
RandomMT19937 seed {seed}
Configuration cubic_side_length {cubic_side_length} particle_type0 {fstprt}
Potential Model LennardJones
Potential VisitModel LongRangeCorrections
ThermoParams beta {beta} chemical_potential -1
Metropolis
TrialTranslate tunable_param 2 tunable_target_acceptance 0.2
Checkpoint checkpoint_file {prefix}{sim}_checkpoint.fst num_hours {hours_checkpoint} num_hours_terminate {hours_terminate}

# grand canonical ensemble initalization
TrialAdd particle_type 0
Run until_num_particles {num_particles}
RemoveTrial name TrialAdd

# canonical ensemble equilibration
Metropolis num_trials_per_iteration {trials_per_iteration} num_iterations_to_complete {equilibration_iterations}
Tune
CheckEnergy trials_per_update {trials_per_iteration} tolerance 1e-8
Log trials_per_write {trials_per_iteration} output_file {prefix}{sim}_eq.csv
Run until_criteria_complete true
RemoveModify name Tune
RemoveAnalyze name Log

# canonical ensemble production
Metropolis num_trials_per_iteration {trials_per_iteration} num_iterations_to_complete {production_iterations}
Log trials_per_write {trials_per_iteration} output_file {prefix}{sim}.csv
Energy trials_per_write {trials_per_iteration} output_file {prefix}{sim}_en.csv
PressureFromTestVolume trials_per_update 1e3 trials_per_write {trials_per_iteration} output_file {prefix}{sim}_pres.csv
Run until_criteria_complete true
""".format(**params))

def post_process(params):
    """ Summary ensemble average energy and block standard deviations """
    ens = np.zeros(shape=(params['num_sims'], 2))
    for sim in range(params['num_sims']):
        energy = pd.read_csv(params['prefix']+str(sim)+'_en.csv')
        ens[sim] = np.array([energy['average'][0],
                             energy['block_stdev'][0]])/params['num_particles']
    print(ens)
    data = {
        'number_particles': params['num_particles'],
        'number_simulations': params['num_sims'],
        'units': {'length': 'Lennard-Jones diameter (sigma)', 'energy': 'Lennard-Jones well depth (epsilon)'},
        'equilibration_trials': params['trials_per_iteration']*params['equilibration_iterations'],
        'production_trials': params['trials_per_iteration']*params['production_iterations'],
        'interaction_cutoff': 3,
        'temperature': params['temperatures'],
        'density': params['densities'],
        'energy_total': ens[:, 0].tolist(),
        'energy_total_blockstdev': ens[:, 1].tolist(),
    }
    print(data)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    fstio.run_simulations(params=PARAMS,
                          sim_node_dependent_params=sim_node_dependent_params,
                          write_feasst_script=write_feasst_script,
                          post_process=post_process,
                          queue_function=fstio.slurm_single_node,
                          args=ARGS)
