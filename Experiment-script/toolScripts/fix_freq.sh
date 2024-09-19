#!/bin/bash
FREQ=$1
echo "passive" | sudo tee /sys/devices/system/cpu/intel_pstate/status

for i in {0..71}
do
    sudo cpufreq-set -g userspace -c $i
    sudo cpufreq-set -f  $FREQ -c $i 
    sudo cpufreq-set -u  $FREQ -c $i 
    sudo cpufreq-set -d  $FREQ -c $i 

done