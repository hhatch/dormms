import sys
import json
import subprocess
import unittest
import numpy as np
import pandas as pd

# Run a feasst simulation with the given parameters
def run_fst(params):
    with open("tmp_launch0.txt", "w") as myfile: myfile.write("""
MonteCarlo
Configuration {config_params}
Potential Model LennardJones
Potential VisitModel LongRangeCorrections
ThermoParams beta 1000000
Metropolis
Log output_file {output_file} max_precision true clear_file true
Run num_trials 1
""".format(**params))
    syscode = subprocess.call("feasstv0.25.1/build/bin/fst < tmp_launch0.txt > tmp_launch0.log", shell=True, executable='/bin/bash')
    if syscode > 0: sys.exit(1)

def srsw_ref_config4(data):
    """Test the LJ potential against a configuration of 30 particles.
    In particular, the 4th configuration of the LJ SRSW reference:
    https://www.nist.gov/mml/csd/chemical-informatics-research-group/lennard-jones-fluid-reference-calculations
    """
    config_file = 'lj_sample_config_periodic4.xyz'
    params = {"config_params": "cubic_side_length 8 particle_type0 /feasst/particle/lj.fstprt \
            xyz_file "+str(config_file),
           "output_file": "tmp_srsw_ref_config4.csv"}
    run_fst(params)
    output = pd.read_csv(params['output_file'])
    assert output['num_particles_of_type0'][0] == 30
    enlj = -16.790321304625856
    enlrc = -0.5451660014945704
    assert np.abs(enlj - output['LennardJones'][0]) < 1e-10
    assert np.abs(enlrc - output['LongRangeCorrections'][0]) < 1e-10
    assert np.abs(enlj + enlrc - output['energy'][0]) < 1e-10
    xyz = pd.read_csv(config_file, sep='\\s+', header=None, skiprows=2)
    data['cubic4'] = {'number': 30, 'pbc':{'length': 8}, 'U_lj': output['LennardJones'][0], 'U_lrc': output['LongRangeCorrections'][0],
        'U_total': output['LennardJones'][0]+output['LongRangeCorrections'][0],
        'x': xyz[1].tolist(), 'y': xyz[2].tolist(), 'z': xyz[3].tolist()}

def srsw_ref_config_triclinic3(data):
    """Test the LJ potential against a configuration of 300 particles in a trinclinic cell.
    In particular, the 3th configuration of the triclinic LJ SRSW reference:
    https://www.nist.gov/mml/csd/chemical-informatics-group/lennard-jones-fluid-reference-calculations-non-cuboid-cell
    """
    params = {'config_file': 'lj_triclinic_sample_config_periodic3.xyz'}
    params.update({'lx': 10.0, 'ly': 9.84807753012208, 'lz': 9.64974312607518,
        'xy': 1.7364817766693041, 'xz': 2.5881904510252074, 'yz': 0.42863479791864567})
    params['config_params'] = """side_length0 {lx} side_length1 {ly} side_length2 {lz} \
xy {xy} xz {xz} yz {yz} particle_type0 /feasst/particle/lj.fstprt \
xyz_file {config_file}""".format(**params)
    params['output_file'] = "tmp_srsw_ref_config_triclinic3.csv"
    run_fst(params)
    output = pd.read_csv(params['output_file'])
    assert output['num_particles_of_type0'][0] == 300
    enlj = -505.78567945268367
    enlrc = -29.37186430697248
    assert np.abs(enlj - output['LennardJones'][0]) < 1e-10
    assert np.abs(enlrc - output['LongRangeCorrections'][0]) < 1e-10
    assert np.abs(enlj + enlrc - output['energy'][0]) < 1e-10
    xyz = pd.read_csv(params['config_file'], sep='\\s+', header=None, skiprows=2)
    data['triclinic3'] = {'number': 300, 'pbc':{'length_x': params['lx'], 'length_y': params['ly'], 'length_z': params['lz'], \
        'tilt_xy': params['xy'], 'tilt_xz': params['xz'], 'tilt_yz': params['yz']}, 'U_lj': output['LennardJones'][0], 'U_lrc': output['LongRangeCorrections'][0],
        'U_total': output['LennardJones'][0]+output['LongRangeCorrections'][0],
        'x': xyz[1].tolist(), 'y': xyz[2].tolist(), 'z': xyz[3].tolist()}

if __name__ == '__main__':
    data = dict()
    srsw_ref_config4(data)
    srsw_ref_config_triclinic3(data)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
