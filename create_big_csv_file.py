import pandas as pd
import numpy as np


def rand_date():
    return f"{np.random.randint(1,12)}/{np.random.randint(1,20)}"


print("Id,Date,Transaction")
for i in range(0, 10000):
    sign = np.random.choice(["-", "+"])
    print(f"{i},{rand_date()},{sign}{np.random.randint(1,100000)/100}")
