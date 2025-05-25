# recursistor
Calculating possible resistor networks from a given set of base resistors


## ResNet object
- Recursively defines series / parallel combinations of resistors
- Defines binary operators `+` and `|` to combine resistors in series and parallel.
- Calculates equivalent value
- Implements `draw()` to draw as ascii-art.
```
━1Ω━┳━━━━━━1Ω━━━━━━┳
    ┗━3Ω━━3Ω━┳━5Ω━┳┛
             ┗━6Ω━┛
Equivalent value: 1.897196261682243Ω
```


## get_combinations function
- Enumerates all possible combinations for a given set of resistors.

