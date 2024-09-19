import argparse
import os 
import subprocess

governor_setting_path = "./set_freq.sh"
passive_setting_path = "./set_passive.sh"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the script in different modes.")
    parser.add_argument("governor", choices=["performance-i","powersave-i","powersave", "performance", "schedutil","ondemand"], help="Mode to run the script in.")
    args = parser.parse_args()
    sys_type = args.governor
    if sys_type.endswith("-i"):
        os.system("echo active | sudo tee /sys/devices/system/cpu/intel_pstate/status")
        os.system(governor_setting_path + " " + sys_type[:-2])
        
    else:
        os.system("echo passive | sudo tee /sys/devices/system/cpu/intel_pstate/status")
        os.system(governor_setting_path + " " + sys_type)