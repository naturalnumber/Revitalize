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
        return self.mean(self.questions['all'].values())


class RAND36:
    def __init__(self, responses: dict = None):
        if responses is None:
            responses = RAND36_response  # this just makes this data default

        self.__dict__.update(functions)
        self.__dict__.update(responses)

    def analyse(self):
        # Also ok
        # return self.sum(self.questions['all'].values())/6
        # return self.average(self.questions['all'].values())
        # return self.mean(self.questions['all'].values())

        # The self. will be necessary here but will get removed in final use

        total = [0] * 40

        # Group 1

        if self.q1 is 1:
            total[1] = 100
        elif self.q1 is 2:
            total[1] = 75
        elif self.q1 is 3:
            total[1] = 50
        elif self.q1 is 4:
            total[1] = 25
        elif self.q1 is 5:
            total[1] = 0

        if self.q2 is 1:
            total[2] = 100
        elif self.q2 is 2:
            total[2] = 75
        elif self.q2 is 3:
            total[2] = 50
        elif self.q2 is 4:
            total[2] = 25
        elif self.q2 is 5:
            total[2] = 0

        if self.q20 is 1:
            total[20] = 100
        elif self.q20 is 2:
            total[20] = 75
        elif self.q20 is 3:
            total[20] = 50
        elif self.q20 is 4:
            total[20] = 25
        elif self.q20 is 5:
            total[20] = 0

        if self.q22 is 1:
            total[22] = 100
        elif self.q22 is 2:
            total[22] = 75
        elif self.q22 is 3:
            total[22] = 50
        elif self.q22 is 4:
            total[22] = 25
        elif self.q22 is 5:
            total[22] = 0

        if self.q34 is 1:
            total[34] = 100
        elif self.q34 is 2:
            total[34] = 75
        elif self.q34 is 3:
            total[34] = 50
        elif self.q34 is 4:
            total[34] = 25
        elif self.q34 is 5:
            total[34] = 0

        if self.q36 is 1:
            total[36] = 100
        elif self.q36 is 2:
            total[36] = 75
        elif self.q36 is 3:
            total[36] = 50
        elif self.q36 is 4:
            total[36] = 25
        elif self.q36 is 5:
            total[36] = 0

        # Group 2

        if self.q3 is 1:
            total[3] = 0
        elif self.q3 is 2:
            total[3] = 50
        elif self.q3 is 3:
            total[3] = 100

        if self.q4 is 1:
            total[4] = 0
        elif self.q4 is 2:
            total[4] = 50
        elif self.q4 is 3:
            total[4] = 100

        if self.q5 is 1:
            total[5] = 0
        elif self.q5 is 2:
            total[5] = 50
        elif self.q5 is 3:
            total[5] = 100

        if self.q6 is 1:
            total[6] = 0
        elif self.q6 is 2:
            total[6] = 50
        elif self.q6 is 3:
            total[6] = 100

        if self.q7 is 1:
            total[7] = 0
        elif self.q7 is 2:
            total[7] = 50
        elif self.q7 is 3:
            total[7] = 100

        if self.q8 is 1:
            total[8] = 0
        elif self.q8 is 2:
            total[8] = 50
        elif self.q8 is 3:
            total[8] = 100

        if self.q9 is 1:
            total[9] = 0
        elif self.q9 is 2:
            total[9] = 50
        elif self.q9 is 3:
            total[9] = 100

        if self.q10 is 1:
            total[10] = 0
        elif self.q10 is 2:
            total[10] = 50
        elif self.q10 is 3:
            total[10] = 100

        if self.q11 is 1:
            total[11] = 0
        elif self.q11 is 2:
            total[11] = 50
        elif self.q11 is 3:
            total[11] = 100

        if self.q12 is 1:
            total[12] = 0
        elif self.q12 is 2:
            total[12] = 50
        elif self.q12 is 3:
            total[12] = 100

        # Group 3

        if self.q13 is 1:
            total[13] = 0
        elif self.q13 is 2:
            total[13] = 100

        if self.q14 is 1:
            total[14] = 0
        elif self.q14 is 2:
            total[14] = 100

        if self.q15 is 1:
            total[15] = 0
        elif self.q15 is 2:
            total[15] = 100

        if self.q16 is 1:
            total[16] = 0
        elif self.q16 is 2:
            total[16] = 100

        if self.q17 is 1:
            total[17] = 0
        elif self.q17 is 2:
            total[17] = 100

        if self.q18 is 1:
            total[18] = 0
        elif self.q18 is 2:
            total[18] = 100

        if self.q19 is 1:
            total[19] = 0
        elif self.q19 is 2:
            total[19] = 100

        # Group 4

        if self.q21 is 1:
            total[21] = 100
        elif self.q21 is 2:
            total[21] = 80
        elif self.q21 is 3:
            total[21] = 60
        elif self.q21 is 4:
            total[21] = 40
        elif self.q21 is 5:
            total[21] = 20
        elif self.q21 is 6:
            total[21] = 0

        if self.q23 is 1:
            total[23] = 100
        elif self.q23 is 2:
            total[23] = 80
        elif self.q23 is 3:
            total[23] = 60
        elif self.q23 is 4:
            total[23] = 40
        elif self.q23 is 5:
            total[23] = 20
        elif self.q23 is 6:
            total[23] = 0

        if self.q26 is 1:
            total[26] = 100
        elif self.q26 is 2:
            total[26] = 80
        elif self.q26 is 3:
            total[26] = 60
        elif self.q26 is 4:
            total[26] = 40
        elif self.q26 is 5:
            total[26] = 20
        elif self.q26 is 6:
            total[26] = 0

        if self.q27 is 1:
            total[27] = 100
        elif self.q27 is 2:
            total[27] = 80
        elif self.q27 is 3:
            total[27] = 60
        elif self.q27 is 4:
            total[27] = 40
        elif self.q27 is 5:
            total[27] = 20
        elif self.q27 is 6:
            total[27] = 0

        if self.q30 is 1:
            total[30] = 100
        elif self.q30 is 2:
            total[30] = 80
        elif self.q30 is 3:
            total[30] = 60
        elif self.q30 is 4:
            total[30] = 40
        elif self.q30 is 5:
            total[30] = 20
        elif self.q30 is 6:
            total[30] = 0

        # Group 5

        if self.q24 is 1:
            total[24] = 0
        elif self.q24 is 2:
            total[24] = 20
        elif self.q24 is 3:
            total[24] = 40
        elif self.q24 is 4:
            total[24] = 60
        elif self.q24 is 5:
            total[24] = 80
        elif self.q24 is 6:
            total[24] = 100

        if self.q25 is 1:
            total[25] = 0
        elif self.q25 is 2:
            total[25] = 20
        elif self.q25 is 3:
            total[25] = 40
        elif self.q25 is 4:
            total[25] = 60
        elif self.q25 is 5:
            total[25] = 80
        elif self.q25 is 6:
            total[25] = 100

        if self.q28 is 1:
            total[28] = 0
        elif self.q28 is 2:
            total[28] = 20
        elif self.q28 is 3:
            total[28] = 40
        elif self.q28 is 4:
            total[28] = 60
        elif self.q28 is 5:
            total[28] = 80
        elif self.q28 is 6:
            total[28] = 100

        if self.q29 is 1:
            total[29] = 0
        elif self.q29 is 2:
            total[29] = 20
        elif self.q29 is 3:
            total[29] = 40
        elif self.q29 is 4:
            total[29] = 60
        elif self.q29 is 5:
            total[29] = 80
        elif self.q29 is 6:
            total[29] = 100

        if self.q31 is 1:
            total[31] = 0
        elif self.q31 is 2:
            total[31] = 20
        elif self.q31 is 3:
            total[31] = 40
        elif self.q31 is 4:
            total[31] = 60
        elif self.q31 is 5:
            total[31] = 80
        elif self.q31 is 6:
            total[31] = 100

        # Group 6

        if self.q32 is 1:
            total[32] = 0
        elif self.q32 is 2:
            total[32] = 25
        elif self.q32 is 3:
            total[32] = 50
        elif self.q32 is 4:
            total[32] = 75
        elif self.q32 is 5:
            total[32] = 100

        if self.q33 is 1:
            total[33] = 0
        elif self.q33 is 2:
            total[33] = 25
        elif self.q33 is 3:
            total[33] = 50
        elif self.q33 is 4:
            total[33] = 75
        elif self.q33 is 5:
            total[33] = 100

        if self.q35 is 1:
            total[35] = 0
        elif self.q35 is 2:
            total[35] = 25
        elif self.q35 is 3:
            total[35] = 50
        elif self.q35 is 4:
            total[35] = 75
        elif self.q35 is 5:
            total[35] = 100

        physical_functioning = (total[3] + total[4] + total[5] + total[6] + total[7] + total[8] + total[9] + total[10] + total[11] + total[12]) / 10
        role_limitations_due_to_physical_health = (total[13] + total[14] + total[15] + total[16]) / 4
        role_limitations_due_to_emotional_problems = (total[3] + total[4] + total[5]) / 3
        energy_fatigue = (total[23] + total[27] + total[29] + total[31]) / 4
        emotional_well_being = (total[24] + total[25] + total[26] + total[28] + total[30]) / 5
        social_functioning = (total[3] + total[4]) / 2
        pain = (total[21] + total[22]) / 2
        general_health = (total[1] + total[33] + total[34] + total[35] + total[36]) / 5

        return f"\n" \
               f"pf {physical_functioning}\n" \
               f"rlph {role_limitations_due_to_physical_health}\n" \
               f"rlep {role_limitations_due_to_emotional_problems}\n" \
               f"ef {energy_fatigue}\n" \
               f"ewb {emotional_well_being}\n" \
               f"sf {social_functioning}\n" \
               f"pain {pain}\n" \
               f"gh {general_health}"


class PHQ9:
    def __init__(self, responses: dict = None):
        if responses is None:
            responses = PHQ9_response  # this just makes this data default

        self.__dict__.update(functions)
        self.__dict__.update(responses)

    def analyse(self):
        # Also ok
        # return self.sum(self.questions['all'].values())/6
        # return self.average(self.questions['all'].values())
        # return self.mean(self.questions['all'].values())

        # The self. will be necessary here but will get removed in final use
        return self.q1 + self.q2 + self.q3 + self.q4 + self.q5 + self.q6 + self.q7 + self.q8 + self.q9


class GAD7:
    def __init__(self, responses: dict = None):
        if responses is None:
            responses = GAD7_response  # this just makes this data default

        self.__dict__.update(functions)
        self.__dict__.update(responses)

    def analyse(self):
        # Also ok
        # return self.sum(self.questions['all'].values())/6
        # return self.average(self.questions['all'].values())
        # return self.mean(self.questions['all'].values())

        # The self. will be necessary here but will get removed in final use
        return self.q1 + self.q2 + self.q3 + self.q4 + self.q5 + self.q6 + self.q7


# test it
print(f"Results for SEMCD6 = {SEMCD6(SEMCD6_response).analyse()}")
print(f"Results for RAND36 = {RAND36(RAND36_response).analyse()}")
print(f"Results for PHQ9 = {PHQ9(PHQ9_response).analyse()}")
print(f"Results for GAD7 = {GAD7(GAD7_response).analyse()}")

