#!/bin/bash

# install specific feasst version(s)
for version in v0.25.1; do
  git clone https://github.com/usnistgov/feasst feasst$version
  pushd feasst$version
    git checkout $version
    mkdir build
    pushd build
      cmake ..
      make -j24 install
    popd
  popd
done
