#!/bin/bash
printf "********\ndeactivate Python environments\n********\n"
deactivate
conda deactivate
printf "********\n/etc/os-release\n********\n"
more /etc/os-release
printf "********\npython environment and pip\n********\n"
python3 -m venv feasst_env
source feasst_env/bin/activate
python3 -m pip install --upgrade pip
pip install numpy pandas matplotlib
version=v0.25.1
printf "********\ninstall feasst version $version\n********\n"
git clone https://github.com/usnistgov/feasst feasst$version
pushd feasst$version
  git checkout $version
  mkdir build
  pushd build
    cmake ..
    make -j8 install
    pip install ../pyfeasst
  popd
popd

