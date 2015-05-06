#!/bin/bash
# Run mapper only

cat input_test/* | python map.py | sort > output/output_mapper.txt