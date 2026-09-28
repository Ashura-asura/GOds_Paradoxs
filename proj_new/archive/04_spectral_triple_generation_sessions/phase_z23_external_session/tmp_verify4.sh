#!/bin/bash
printf 'setdefault E8\nR = rootdatum(E8)\ndim(R)\ndim([1,0,0,0,0,0,0,0])\nquit\n' | lie
echo "--- branch adjoint ---"
printf 'setdefault E8\nbranch(E8,E7A1,[1,0,0,0,0,0,0,0])\nquit\n' | lie
