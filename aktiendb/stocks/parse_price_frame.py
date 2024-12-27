import numpy as np
from ..utils.np_to_native import npDTypeToNative
from pandas import DataFrame

def parsePriceFrame(dataframe: DataFrame):
    print(dataframe)