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
pip install numpy pandas
version=v0.25.3
printf "********\ninstall feasst version $version\n********\n"
wget https://github.com/usnistgov/feasst/archive/refs/tags/${version}.tar.gz
tar -xf ${version}.tar.gz --transform s/-/-v/
mkdir feasst-${version}/build; pushd $_
  cmake ..
  make install -j$(nproc)
  pip install ../pyfeasst
popd
