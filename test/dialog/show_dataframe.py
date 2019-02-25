from easygraphics.dialog import *
import numpy as np
import pandas as pd

df = pd.DataFrame(np.arange(10).reshape(2, 5),
                  columns=['a', 'b', 'c', 'd', 'e'])
show_objects(datas=df)
