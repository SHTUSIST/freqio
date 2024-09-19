Before you move on, please read README.md in toolScripts directory. 

# Fig 4: 
You should modify line 15 in run.py. 
```python 
rand = ""
``` 
into 
```python 
rand = "rand"
``` 
# Fig 5 & Fig 6

Install and run as paper stated. 

# Fig 7:
```redis-benchmark -r 1000000 -n 100000000 -t lpush -P 16 ```

# Fig 8:
```bash ./toolScripts/monitor-power.sh ```, it will output three value: unit, PKG power and DRAM power. 
power should be calculate by power = PKG(DRAM) power * 0.5 ^ (unit)

