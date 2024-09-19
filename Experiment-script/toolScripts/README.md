**Brief description of scripts:** 
- set_passive.sh: Accepts "active" or "passive" as an argument. Switch between intel_pstate/CPUFreq drivers.
- monitor-power.sh: Computes the power usage for a single Fio run. 
- monitor.sh: Monitors frequency and I/O wait information every second for an Fio run.
- set_governor.sh: Accepts a governor as an argument to set CPU scaling. You should set the correct core number before your first run. 
- fix_freq.sh: Takes a frequency argument and sets all cores to that frequency. You should set the correct core number before your first run. 
- changeState.py: Accepts a governor as an argument. Modifies the CPU current policy for all cores. Refer to "Setting Policies" for policy setting rules. 
- run.py: The primary script for executing FIO tests. Refer to "Setting Policies" for policy setting rules. 
**Setting Policies:**

- For policies associated with `intel_pstate`, the policy name will include the suffix `-i`. For example:
  - `performance-i`
  - `powersave-i`
- For policies associated with `CPUFreq`, the policy name remains unchanged. For example:
  - `performance`
  - `powersave`
  - `schedutil`
  - `ondemand`
  - `userspace`