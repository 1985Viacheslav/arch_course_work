### Without cash
```
Running 15s test @ http://127.0.0.1:8000/user/23
  2 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   365.23ms  515.40ms   2.00s    79.45%
    Req/Sec    54.04     30.71   220.00     66.91%
  9198 requests in 15.09s, 1.73MB read
  Socket errors: connect 0, read 0, write 0, timeout 901
Requests/sec:    609.71
Transfer/sec:    117.30KB

```


### With cache
```
Running 15s test @ http://127.0.0.1:8000/user/23
  2 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   470.64ms  515.71ms   1.99s    83.21%
    Req/Sec   384.47     91.15   660.00     78.77%
  11231 requests in 15.05s, 2.71MB read
  Socket errors: connect 0, read 0, write 0, timeout 448
Requests/sec:    746.25
Transfer/sec:    184.38KB

```

