import subprocess
import os
import signal
import time
from multiprocessing import Process
import datetime
import sys


# Define the file path

# The directory you are testing.
file_dir = "/tmp/"

# Where your result is located. 
result_dir = ""

# Below are fio setting.
rand = "" #rand

timebased = 1
runtime = 600
file_size = "100g"
bs="4k"

# You might want to use FIO with minimal open file descriptors for simpler data management. 
minimal = False

# ioengine this script support. sync2: direct I/O, io_uring2: io_uring with sqpoll=1
fdatasync_dict={"mmap": "1", "libaio": "1", "posixaio":"1", "sync":"1", "psync":"1", "io_uring":"1", "sync2": "1", "io_uring2": "1", "psync": "1"}

direct_dict = {"mmap": "0", "libaio": "1", "posixaio":"0", "sync":"0", "psync":"0", "io_uring":"0", "sync2": "1", "io_uring2": "0", "psync": "0"}


def run_fio(mix_proportion, io_engine, io_depth, sys_type, numjobs:int = 1):
    # Construct the fio command
    # Redirect output to file
    file_path = file_dir + datetime.datetime.now().strftime('%H%M%S') + ".txt"
    output_file = f"{sys_type}_{io_engine}_{mix_proportion}_{io_depth}_{numjobs}.txt"
    output_file = os.path.join(result_dir, output_file)
    direct = direct_dict[io_engine]
    sqthread_poll = 0
    fio_command = []
    if io_engine == "sync2":
        io_engine = "sync"
    elif io_engine == "io_uring2":
        io_engine = "io_uring"
        sqthread_poll = 1
        
    if mix_proportion == 100:
        read_type = rand + "read"
        fio_command = [
            "fio",
            "--name=" + str(read_type),
            "--filename=" + file_path,
            "--ioengine=" + str(io_engine),
            "--direct=" + str(direct),
            "--rw=" + read_type,
            "--bs=" + bs,
            "--size=" + str(file_size),
            "--iodepth=" + str(io_depth),
            "--numjobs=" + str(numjobs),
            "--fdatasync=" + fdatasync_dict[io_engine],
            "--unlink=1",
            "--time_based=" + str(timebased),
            "--runtime=" + str(runtime),
            "--group_reporting=1",

        ]
    elif mix_proportion == 0:
        read_type = rand + "write"
        fio_command = [
            "fio",
            "--name=" + str(read_type),
            "--filename=" + file_path,
            "--ioengine=" + io_engine,
            "--direct="+ str(direct),
            "--rw=" + read_type,
            "--bs=" + bs,
            "--size=" + str(file_size),
            "--iodepth=" + str(io_depth),
            "--numjobs=" + str(numjobs),
            "--fdatasync=" + fdatasync_dict[io_engine],
            "--unlink=1",
            "--time_based=" + str(timebased),
            "--runtime=" + str(runtime),
            "--group_reporting=1",

        ]
    else:
        read_type = rand + "rw"
        fio_command = [
            "fio",
            "--name="+ str(read_type) + str(mix_proportion),
            "--filename=" + file_path,
            "--ioengine=" + io_engine,
            "--direct=" + str(direct),
            "--rw=" + read_type,
            "--rwmixread=" + str(mix_proportion),
            "--rwmixwrite=" + str(100 - mix_proportion),
            "--bs=" + bs,
            "--size=" + str(file_size),
            "--iodepth=" + str(io_depth),
            "--numjobs=" + str(numjobs),
            "--unlink=1",
            "--fdatasync=" + fdatasync_dict[io_engine],
            "--time_based=" + str(timebased),
            "--runtime=" + str(runtime),
            "--group_reporting=1",

        ]
    if io_engine == "io_uring" and sqthread_poll:
        fio_command.append("--sqthread_poll=1")
    if minimal: 
        fio_command.append("--minimal")
    with open(output_file, "w") as out:
        subprocess.run(fio_command, stdout=out)
        for fio_cmd in fio_command:
            out.write(fio_cmd + " ")

if __name__ == "__main__":
    # Define the read proportions to test
    proportions = [0] 
    
    # The io_engine you are going to test. 
    io_engine_list = ["sync"] 
    result_dir = datetime.datetime.now().strftime('%m%d-%H%M')
    
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # valid type list: "performance-i","powersave-i", "performance","powersave", "schedutil", "ondemand" 
    type_list = ["performance-i", "powersave-i"] 
    numjob_list = [1] 
    for sys_type in type_list: 
        if sys_type == "userspace":
            print("sys type: userspace")
            os.system("cpufreq-info -c 0")
        elif sys_type.endswith("-i"):
            os.system("bash ./set_passive.sh active")
            os.system("bash ./set_governor.sh " + sys_type[:-2])
        else:
            os.system("bash ./set_passive.sh passive")
            os.system("bash ./set_governor.sh " + sys_type)
        for numjob in numjob_list:
            for io_engine in io_engine_list:
                for proportion in proportions:
                    for io_depth in [1]: #  2,128  , 8, 16  2,8, 64, 128
                        os.system("echo 3 | sudo tee /proc/sys/vm/drop_caches")
                        # os.system("fstrim -v /tmp/")
                        os.system("sleep 1s")
                        fio_process = Process(target=run_fio, args=(proportion, io_engine, io_depth, sys_type, numjob))
                        fio_process.start()
                        fio_process.join()
    os.system("chown -R x:x " + result_dir)