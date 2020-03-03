from math import sqrt
from statistics import mean, mode, median, stdev, variance

SEMCD6_response = {'questions': {'all': {'q1': 1, 'q2': 10, 'q3': 2, 'q4': 9, 'q5': 3, 'q6': 8}, 'g2': {'q1': 1}, 'g3': {'q2': 10}, 'g4': {'q3': 2}, 'g5': {'q4': 9}, 'g6': {'q5': 3}, 'g7': {'q6': 8}}, 'q1': 1, 'q2': 10, 'q3': 2, 'q4': 9, 'q5': 3, 'q6': 8}

RAND36_response = {'questions': {'all': {'q1': 2, 'q2': 4, 'q3': 2, 'q4': 1, 'q5': 3, 'q6': 2, 'q7': 1, 'q8': 3, 'q9': 2, 'q10': 1, 'q11': 3, 'q12': 2, 'q13': False, 'q14': True, 'q15': False, 'q16': True, 'q17': True, 'q18': False, 'q19': True, 'q20': 3, 'q21': 3, 'q22': 4, 'q23': 3, 'q24': 4, 'q25': 2, 'q26': 5, 'q27': 1, 'q28': 6, 'q29': 4, 'q30': 3, 'q31': 5, 'q32': 2, 'q33': 3, 'q34': 4, 'q35': 2, 'q36': 5}, 'g1': {'q1': 2}, 'g2': {'q2': 4}, 'g3': {'q3': 2, 'q4': 1, 'q5': 3, 'q6': 2, 'q7': 1, 'q8': 3, 'q9': 2, 'q10': 1, 'q11': 3, 'q12': 2}, 'g4': {'q13': False, 'q14': True, 'q15': False, 'q16': True}, 'g5': {'q17': True, 'q18': False, 'q19': True}, 'g6': {'q20': 3}, 'g7': {'q21': 3}, 'g8': {'q22': 4}, 'g9': {'q23': 3, 'q24': 4, 'q25': 2, 'q26': 5, 'q27': 1, 'q28': 6, 'q29': 4, 'q30': 3, 'q31': 5}, 'g10': {'q32': 2}, 'g11': {'q33': 3, 'q34': 4, 'q35': 2, 'q36': 5}}, 'q1': 2, 'q2': 4, 'q3': 2, 'q4': 1, 'q5': 3, 'q6': 2, 'q7': 1, 'q8': 3, 'q9': 2, 'q10': 1, 'q11': 3, 'q12': 2, 'q13': False, 'q14': True, 'q15': False, 'q16': True, 'q17': True, 'q18': False, 'q19': True, 'q20': 3, 'q21': 3, 'q22': 4, 'q23': 3, 'q24': 4, 'q25': 2, 'q26': 5, 'q27': 1, 'q28': 6, 'q29': 4, 'q30': 3, 'q31': 5, 'q32': 2, 'q33': 3, 'q34': 4, 'q35': 2, 'q36': 5}

PHQ9_response = {'questions': {'all': {}}, 'q1': 2, 'q2': 3, 'q3': 1, 'q4': 4, 'q5': 2, 'q6': 3, 'q7': 1, 'q8': 4, 'q9': 2}

GAD7_response = {'questions': {'all': {}}, 'q1': 1, 'q2': 4, 'q3': 0, 'q4': 3, 'q5': 1, 'q6': 2, 'q7': 0}

# if you set print_test_data to True in models django will spit out the above for any survey submission by the front end

functions = {
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

class survey:
    def __init__(self, responses: dict):
        self.__dict__.update(functions)
        self.__dict__.update(responses)

    def analyse(self):

        # Don't use any functions other than the above for the moment

        return 0 # Put calc here


# Example
class SEMCD6:
    def __init__(self, responses: dict = None):
        if responses is None:
            responses = SEMCD6_response  # this just makes this data default

        self.__dict__.update(functions)
        self.__dict__.update(responses)

    def analyse(self):
        # Also ok
        # return self.sum(self.questions['all'].values())/6
        # return self.average(self.questions['all'].values())
        # return self.mean(self.questions['all'].values())

        # The self. will be necessary here but will get removed in final use
        return (self.q1 + self.q2 + self.q3 + self.q4 + self.q5 + self.q6)/6


# test it
print(f"Results for SEMCD6 = {SEMCD6(SEMCD6_response).analyse()}")