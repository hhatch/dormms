"""
This module..
"""

import json

class ReferenceConfigurations:
    """ ... """
    def __init__(self):
        with open('lennard_jones/reference_configurations/data.json') as f:
            self._data = json.load(f)

    def data(self):
        """
        Return the data

        >>> from dormms import lennard_jones as lj
        >>> lj.ReferenceConfigurations().data()
        '1'
        """
        return self._data

if __name__ == "__main__":
    import doctest
    doctest.testmod()
