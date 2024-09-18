"""
This module..
"""

from importlib.resources import files
import json

class ReferenceConfigurations:
    """ ... """
    def __init__(self):
        with open(files('dormms').joinpath('lennard_jones/reference_configurations/data.json')) as f:
            self._data = json.load(f)

    def data(self):
        """
        Return the data

        >>> from dormms import lennard_jones as lj
        >>> data = lj.ReferenceConfigurations().data()['cubic4']
        >>> data['N']
        30
        >>> data['L']
        8
        >>> data['L']
        8
        """
        return self._data

if __name__ == "__main__":
    import doctest
    doctest.testmod()
