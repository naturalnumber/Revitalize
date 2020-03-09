from math import sqrt
from statistics import mean, mode, median, stdev, variance

print_debug = True

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

        if print_debug: print(f"DataAnalysisSystem.process({expression}, \n{data})")

        result = None
        debug = []

        if simple:
            try:
                result = eval(expression, DataAnalysisSystem.__globals, data)
            except Exception as e:
                debug.append(e)
                if print_debug: print(f"DataAnalysisSystem.process: (simple) {e}")
        else:
            try:
                result = eval(compile(expression, '<string>', 'exec'), DataAnalysisSystem.__globals, data)
            except Exception as e:
                debug.append(e)
                if print_debug: print(f"DataAnalysisSystem.process: (!simple) {e}")

        if return_debug:
            if print_debug: print(f"DataAnalysisSystem.process: {debug}")
            return result, debug
        return result
