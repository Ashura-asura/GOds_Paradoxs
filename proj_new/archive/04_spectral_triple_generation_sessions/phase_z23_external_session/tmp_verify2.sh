#!/bin/bash
echo "--- gap simple ---"
echo 'Print(123*456);' | gap -q
echo "--- gap banner ---"
gap -A -b -e 'Print(Version);' 2>&1 | head -2
echo "--- lie ---"
printf 'setdefault E8\ndim(R)\nquit\n' | lie
echo "--- lie version ---"
dpkg -l lie | tail -1
