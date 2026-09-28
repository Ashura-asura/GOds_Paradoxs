#!/bin/bash
set -x
cd /root
export MAMBA_ROOT_PREFIX=/root/micromamba
./bin/micromamba create -y -n sage -c conda-forge sagemath > /root/sage_install.log 2>&1
echo "SAGE_INSTALL_EXIT=$?" >> /root/sage_install.log
