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

Workflow for adding new results
====================================

The scripts have the following requirements:

* File names begin with a number that corresponds with the order of running the scripts.
* BASH or Python extensions of .sh or .py, respectively.
* Script output is recorded as "bash script.sh > script.sh.log 2>&1" or "python script.py > script.py.log 2>&1" (even if the output is empty).
* Usernames in log and output files are replaced with "user".
* Include assert checks for expected results.
* Verify results are reproduced by another researcher.
* Do not add large data files or external software to the repository.
* Temporary files are ones that are not added to the repository as final results. All temporary file names should begin with the characters "tmp".

.. include:: DISCLAIMER.rst

.. include:: LICENSE.rst
