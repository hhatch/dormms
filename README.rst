******************************************************************************************
DORMMS - Database of Reproducible Models and Molecular Simulations
******************************************************************************************

DORMMS contains model and molecular simulation results from open-source software that are reproducible.
All results are organized by model and then technique and contain the BASH or Python scripts necessary to install, run and analyze the software.
Select results are further documented and displayed graphically as part of GORMMS (Graphics of Reproducible Models and Molecular Simulations).

.. note::

   Website: https://pages.nist.gov/dormms

   Code Repository: https://github.com/usnistgov/dormms

   Website: https://pages.nist.gov/gormms

   Code Repository: https://github.com/usnistgov/gormms

Installation
==============

.. code-block:: bash

    pip install dormms


Workflow for adding new results
====================================

Each model is placed in the src/dormms/ directory.
And each method is placed in a new directory therein, where the final post processing step should result in a single data.json file that will be imported by the Python module.

The scripts have the following requirements:

* File names begin with a number that corresponds with the order of running the scripts.
* BASH or Python extensions of .sh or .py, respectively.
* Before install, deactivate any Python virtual environments. The install should include all Python dependencies.
* Script output is recorded as "bash script.sh > script.sh.log 2>&1" or "python script.py > script.py.log 2>&1" (even if the output is empty).
* Usernames in log and output files are replaced with "user".
* Include assert checks for expected results.
* Package all data into a dictionary and write to file in JSON format as data.json.
* Verify results are reproduced by another researcher.
* Do not add large data files or external software to the repository.
* Temporary files are ones that are not added to the repository as final results.

After the data.json is created, then a [method].py file is created that matches the name of the data directory.
For example, src/dormms/lennard_jones.py imports src/dormms/lennard_jones/data.json.

.. include:: DISCLAIMER.rst

.. include:: LICENSE.rst
