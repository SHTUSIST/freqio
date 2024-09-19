#!/bin/bash

# Assuming you have 72 cores, you would replace the range with the number of cores you have
for i in {0..71}
do
    sudo cpufreq-set -c $i -g $1

done
