import numpy as np


def npDTypeToNative(value) -> tuple[any, bool]:
    if isinstance(value, np.generic):
        return value.tolist(), True
    return value, False