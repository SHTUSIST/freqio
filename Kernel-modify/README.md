# Kernel modify

we modify two files of the linux kernel 6.5.5

They are  cpufreq_schedutil.c and 

Below are the difference:



**cat cpufreq_schedutil.c_diff.txt**

```c
 
186,187c186,187
<       // sg_cpu->iowait_boost = set_iowait_boost ? IOWAIT_BOOST_MIN : 0;
<       // sg_cpu->iowait_boost_pending = set_iowait_boost;
---
>       sg_cpu->iowait_boost = set_iowait_boost ? IOWAIT_BOOST_MIN : 0;
>       sg_cpu->iowait_boost_pending = set_iowait_boost;
189,198c189
<       if (!sg_cpu->iowait_boost_pending){
<               sg_cpu->iowait_boost_pending = true;
<       }
<       else{
<            sg_cpu->iowait_boost =
<                       max_t(unsigned int, sg_cpu->iowait_boost >> 1, 0);
<       }
<       return false;
<
<       // return true;
---
>       return true;
218,221d208
<       //iowait_boost from 0 to 128 to 1024
<       //set_iowait_boost, this function judge tick is ioboost or not
<       //iowait_boost_pending,  last tick ioboost or not
225,227c212,214
<       // if (sg_cpu->iowait_boost &&
<       //     sugov_iowait_reset(sg_cpu, time, set_iowait_boost))
<       //      return;
---
>       if (sg_cpu->iowait_boost &&
>           sugov_iowait_reset(sg_cpu, time, set_iowait_boost))
>               return;
230,231c217,218

---
>       if (!set_iowait_boost)
>               return;
234,236c221,223

---
>       if (sg_cpu->iowait_boost_pending)
>               return;
>       sg_cpu->iowait_boost_pending = true;
239,243c226,230

---
>       if (sg_cpu->iowait_boost) {
>               sg_cpu->iowait_boost =
>                       min_t(unsigned int, sg_cpu->iowait_boost << 1, SCHED_CAPACITY_SCALE);
>               return;
>       }
246,248c233
<       // sg_cpu->iowait_boost = IOWAIT_BOOST_MIN;
<       sg_cpu->iowait_boost_pending = false;
<       sg_cpu->iowait_boost = SCHED_CAPACITY_SCALE;
---
>       sg_cpu->iowait_boost = IOWAIT_BOOST_MIN;
278c263,265
<       sugov_iowait_reset(sg_cpu, time, false);
---
>       /* Reset boost if the CPU appears to have been idle enough */
>       if (sugov_iowait_reset(sg_cpu, time, false))
>               return;
280,293c267,276
---
>       if (!sg_cpu->iowait_boost_pending) {
>               /*
>                * No boost pending; reduce the boost value.
>                */
>               sg_cpu->iowait_boost >>= 1;
>               if (sg_cpu->iowait_boost < IOWAIT_BOOST_MIN) {
>                       sg_cpu->iowait_boost = 0;
>                       return;
>               }
>       }
295c278
<       // sg_cpu->iowait_boost_pending = false;
---
>       sg_cpu->iowait_boost_pending = false;

```





**cat inode.c_diff.txt**

```c
3347,3350d3346
<
<       current->in_iowait = 1;
<
3422,3423d3417
<       current->in_iowait = 0;
```

