# coin_simulate
코인 데이터 지표 구하는 로직<br>
Index<br>
* [Directory](#directory)
* [Test](#test)
* [Result](#result)

## Directory
```
+- src
    +- C
        +- src : c source
        -- libcalculator.so
        -- Makefile
        -- simulation.py
    +- Python
        -- simulation.py
```

## Test
1. ` pip3 install -r requirements.txt `
### C
1. Move C directorty
2. `make`
3. `python3 -m unittest simulation.TestMacd.test_example`
### python
1. Move Python directory
2. `python3 -m unittest simulation.TestMacd.test_example`

## Result
![C](c_cProfile.png)
![Python](python_cProfile.png)