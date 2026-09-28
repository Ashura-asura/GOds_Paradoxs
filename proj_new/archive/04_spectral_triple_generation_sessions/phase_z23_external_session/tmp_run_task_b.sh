#!/bin/bash
cd "$(dirname "$0")"
timeout 300 python3 -u tmp_task_b_so10_classes.sage.py > task_b_so10_classes_out.txt 2>&1
echo "PYEXIT=$?"
