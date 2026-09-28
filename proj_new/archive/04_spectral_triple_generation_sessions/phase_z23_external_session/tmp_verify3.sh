#!/bin/bash
printf 'setdefault E8\ndim(1,0,0,0,0,0,0,0)\nquit\n' | lie
echo "--- branch E8->E7xA1 of adjoint ---"
printf 'setdefault E8\nbranch(E8,E7A1,1,0,0,0,0,0,0,0)\nquit\n' | lie
