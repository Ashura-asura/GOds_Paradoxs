#!/bin/bash
echo "Print(Version);" | gap -q
echo "---"
echo "LoadPackage(\"hap\");" | gap -q
echo "---"
lie -s -e "setdefault E8; dim(R)"
echo "---"
echo "TEST"
