from math import sqrt
from statistics import mean, mode, median, stdev, variance


class DataAnalysisSystem:
    __globals = {
            '__builtins__': None,  # Required for safety
            'abs'         : abs,
            'min'         : min,
            'max'         : max,
            'sum'         : sum,
            'round'       : round,
            'int'         : int,
            'float'       : float,
            'len'         : len,
            'sqrt'        : sqrt,
            'average'     : mean,
            'mean'        : mean,
            'mode'        : mode,
            'median'      : median,
            'stdev'       : stdev,
            'variance'    : variance
    }

    # It is vitally important that no external input is passed to this method as it is impossible to fully prevent
    # certain (obscure) attacks.
    @staticmethod
    def process(expression: str, data: dict, simple: bool = True, return_debug: bool = False):
        if not simple: raise NotImplementedError("not implemented yet")

        result = None
        debug = []

        if simple:
            try:
                result = eval(expression, DataAnalysisSystem.__globals, data)
            except Exception as e:
                debug.append(e)
        else:
            try:
                result = eval(compile(expression, '<string>', 'exec'), DataAnalysisSystem.__globals, data)
            except Exception as e:
                debug.append(e)

        if return_debug:
            return result, debug
        return result
