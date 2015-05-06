#!/bin/bash
# Run map and reduce

cat input_test/* | python map.py | sort | python reduce.py > output/output.txt