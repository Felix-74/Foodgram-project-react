from utils.const import IntConst

def min_max_small_int(num):
    if isinstance(num, int):
        return num < IntConst.MIN_SMALL or num > IntConst.MAX_SMALL
    return False
    