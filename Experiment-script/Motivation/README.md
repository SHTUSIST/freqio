Before you do experiment:


For experiments on motivation section: 

# Fig 1.a: 
```python3 /toolScripts/run.py```


The variable you may need to change: file_dir. 
You should also pay attention to fstrim in run.py. 
Be attention to the file_size. No spare space make the experiment fail. 

# Fig 1.b
bash fix_seq.sh To set the frequency. Change line 124 : 
```python
    type_list = ["performance-i", "powersave-i"]
```
into 
```python
type_list = ["userspace"]
```

``` python3 /toolScripts/run.py ```

# Fig 1.c
You should run ``` bash toolScripts/monitor.sh & ``` in one shell. monitor.sh monitor the iowait number of core 0 by default. 

``` taskset -c 0 python3 /toolScripts/run.py ``` runs in another shell. The result is in mobitor.out.

# Fig 1.d
This result is counted from the output of fio. 

# Fig 2.a

Same as Fig 1.c. You just record the result of frequency. 

# Fig 2.b
