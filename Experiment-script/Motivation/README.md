Before you move on, please read README.md  in toolScripts directory. 

# Experiments for the Motivation Section:

## Fig 1.a: 
Run the following command:
```python3 /toolScripts/run.py```


The variable you may need to change: file_dir. 
You should also pay attention to fstrim in run.py. 
Be attention to the file_size. No spare space make the experiment fail. 

## Fig 1.b
To set the frequency, execute:
```
bash fix_seq.sh 
```

Then, change line 124 from:
```python
    type_list = ["performance-i", "powersave-i"]
```
into 
```python
type_list = ["userspace"]
```
Now run:
``` python3 /toolScripts/run.py ```

## Fig 1.c
In one terminal, run:
``` bash toolScripts/monitor.sh & ``` 

This command monitors the I/O wait time of core 0 by default. In another terminal, execute:

``` taskset -c 0 python3 /toolScripts/run.py ``` 
The results will be saved in monitor.out.
You should change
```python file_dir = "/tmp/"``` into your target directory to test different devices. 

## Fig 1.d
This result is derived from the output of FIO.

## Fig 2.a

Follow the same procedure as in Fig 1.c.

## Fig 2.b

Follow the same procedure as in Fig 1.c, but record the frequency results.