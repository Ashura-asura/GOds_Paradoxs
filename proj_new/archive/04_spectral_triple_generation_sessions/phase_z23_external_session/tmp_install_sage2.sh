#!/bin/bash
set -x
cd /root
export MAMBA_ROOT_PREFIX=/root/micromamba
./bin/micromamba create -y -n sage -c conda-forge sage
echo SAGE_INSTALL_EXIT=$?
