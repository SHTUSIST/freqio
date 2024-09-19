#!/bin/bash


# This script output the iowait and frequency by sampling. 
prev_iowait=0

max_freq=16#$(sudo rdmsr --bitfield 15:8 0x000000ce)
cur_iowait=$(awk '/cpu0/ {print $6}' /proc/stat)

program_name=" fio"
output_file="monitor.out"
until $(top -bn 1 | grep -qE "${program_name}.*");
do
    sleep 0.1
done

echo "New start" >> ${output_file}

# Now read the stats from core 0. 
while $(top -bn 1 | grep -qE "${program_name}.*"); do

    prev_mperf=16#$(sudo rdmsr 0x000000e7)
    prev_aperf=16#$(sudo rdmsr 0x000000e8)
    prev_iowait=$(awk '/cpu0/ {print $6}' /proc/stat)
    sleep 1
    cur_mperf=16#$(sudo rdmsr 0x000000e7)
    cur_aperf=16#$(sudo rdmsr 0x000000e8)
    cur_iowait=$(awk '/cpu0/ {print $6}' /proc/stat)

    diff_iowait=$((cur_iowait - prev_iowait))
    cur_freq=$((max_freq * 10#100000 * (cur_aperf - prev_aperf) / (cur_mperf - prev_mperf)))

    echo " ${cur_freq} ${diff_iowait}" >> ${output_file}
    # echo "$" >> ${output_file}
    
done
echo "" >> ${output_file}