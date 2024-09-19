#!/bin/bash

MSR_PKG_ENERGY_STATUS_ADDR=0x611
MSR_DRAM_ENERGY_STATUS_ADDR=0x619 

MSR_RAPL_POWER_UNIT_ADDR=0x606

core=0

MSR_RAPL_POWER_UNIT=$(sudo rdmsr --bitfield 12:8 ${MSR_RAPL_POWER_UNIT_ADDR} -p ${core})

PKG_prev_energy=16#$(sudo rdmsr ${MSR_PKG_ENERGY_STATUS_ADDR} -p ${core})
DRAM_prev_energy=16#$(sudo rdmsr ${MSR_DRAM_ENERGY_STATUS_ADDR} -p ${core})


taskset -c 0 python3 run.py 

PKG_curr_energy=16#$(sudo rdmsr ${MSR_PKG_ENERGY_STATUS_ADDR} -p ${core})
DRAM_curr_energy=16#$(sudo rdmsr ${MSR_DRAM_ENERGY_STATUS_ADDR} -p ${core})

PKG_energy_diff=$((${PKG_curr_energy} - ${PKG_prev_energy}))
DRAM_energy_diff=$((${DRAM_curr_energy} - ${DRAM_prev_energy}))

echo "UNIT: ${MSR_RAPL_POWER_UNIT} PKG: ${PKG_energy_diff}, DRAM: ${DRAM_energy_diff}"
echo ""
