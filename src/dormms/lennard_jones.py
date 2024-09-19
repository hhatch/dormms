"""
The Lennard-Jones model is given by ...
"""

from importlib.resources import files
import json

class ReferenceConfigurations:
    """
    Reference configurations report energy to machine precision that can be used to model implementations.
    """
    def __init__(self):
        with open(files('dormms').joinpath('lennard_jones/reference_configurations/data.json')) as f:
            self._data = json.load(f)

    def data(self):
        """
        Return the data as follows:

        >>> from dormms import lennard_jones as lj
        >>> cubic = lj.ReferenceConfigurations().data()['cubic4']
        >>> cubic['number']
        30
        >>> cubic['pbc']['length']
        8
        >>> triclinic = lj.ReferenceConfigurations().data()['triclinic3']
        >>> triclinic['number']
        300
        """
        return self._data

class CanonicalMonteCarlo:
    """
    Canonical ensemble Metropolis Monte Carlo simulations with reported total potential energy and pressure.
    """
    def __init__(self):
        with open(files('dormms').joinpath('lennard_jones/canonical_monte_carlo/data.json')) as f:
            self._data = json.load(f)

    def data(self):
        """
        Return the data as follows:

        >>> from dormms import lennard_jones as lj
        >>> data = lj.CanonicalMonteCarlo().data()
        >>> data['number_simulations']
        20
        """
        return self._data

if __name__ == "__main__":
    import doctest
    doctest.testmod()
