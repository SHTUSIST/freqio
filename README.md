# freqio good

Before you do experiments, make sure to install libs. 
```sudo apt install cpufrequtils
    sudo apt install fio
    sudo apt install msr-tools
```

You should either use 
``` lscpu ``` or ```cpufreq-info``` to check the core number of your machine. Modify the max core id in toolScripts/fix_freq.sh and toolScripts/set_freq.sh

If you are running run.py with root, you should better change the line chown x:x as you wanted. 