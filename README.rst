******************************************************************************************
DORMMS - Database of Reproducible Models and Molecular Simulations
******************************************************************************************

DORMMS contains model and molecular simulation results from open-source software that are reproducible.

All software installation instructions can be found in the software directory.
Each specific version of software used to generate the results has an accompanying BASH script named [software][version]_install.sh.

All results are organized by model in the models directory.
Within each model, the results are then organized by technique.
Each result must have a run.sh BASH script that generates the results using the specific software.
The results may also be analyzed with a post_process.sh BASH script.

Select results are further documented and displayed graphically as part of the GORMMS (Graphics of Reproducible Models and Molecular Simulations) project.

.. note::

   Website: https://pages.nist.gov/dormms

   Code Repository: https://github.com/usnistgov/dormms

   Website: https://pages.nist.gov/gormms

   Code Repository: https://github.com/usnistgov/gormms

.. include:: DISCLAIMER.rst

.. include:: LICENSE.rst
