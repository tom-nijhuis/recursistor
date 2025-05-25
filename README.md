# recursistor
Calculating possible resistor networks from a given set of base resistors


### Object `ResNet`
- Recursively defines series / parallel combinations of resistors
- Implements binary operators `+` and `|` to combine resistors in series and parallel.
- Calculates equivalent value
- Implements `draw()` to draw as ascii-art.
```
S = ((R(2) | (R(2) + (R(1) |  R(2) + R(3))))+R(1))

┳━━━━━━2Ω━━━━━━┳━1Ω━
┗━2Ω━┳━━━1Ω━━━┳┛
     ┗━2Ω━━3Ω━┛
```


### function `get_combinations`
- Enumerates all possible combinations for a given set of resistors.

