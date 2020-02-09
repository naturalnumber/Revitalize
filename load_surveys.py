from Revitalize.models import *

# To load this run:
# python ./manage.py shell
# Then enter:
# exec(open("./load_surveys.py").read())

semcd6 = {
        "tag"        : "SEMCD6",
        "name"       : "Self-Efficacy for Managing Chronic Disease 6-item Scale",
        "description": "This 6-item scale contains items taken from several SE scales developed for the Chronic Disease Self Management study.",
        "elements"   : [
                {
                        "element_type": "text",
                        "name"        : "Intro",
                        "description" : "Intro Paragraph",
                        "text"        : "We would like to know how confident you are in doing certain activities. For each of the following questions, please choose the number that corresponds to your confidence that you can do the tasks regularly at the present time."
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 10,
                                "step"       : 1,
                                "initial"    : 6,
                                "labels"     : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                "annotations": {
                                        "minimum": "not at all confident",
                                        "maximum": "totally confident"
                                }
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "1",
                                        "text"     : "How confident do you feel that you can keep the fatigue caused by your disease from interfering with the things you want to do?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 10,
                                "step"       : 1,
                                "initial"    : 6,
                                "labels"     : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                "annotations": {
                                        "minimum": "not at all confident",
                                        "maximum": "totally confident",
                                }
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "2",
                                        "text"     : "How confident do you feel that you can keep the physical discomfort or pain of your disease from interfering with the things you want to do?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 10,
                                "step"       : 1,
                                "initial"    : 6,
                                "labels"     : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                "annotations": {
                                        "minimum": "not at all confident",
                                        "maximum": "totally confident",
                                }
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "3",
                                        "text"     : "How confident do you feel that you can keep the emotional distress caused by your disease from interfering with the things you want to do?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 10,
                                "step"       : 1,
                                "initial"    : 6,
                                "labels"     : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                "annotations": {
                                        "minimum": "not at all confident",
                                        "maximum": "totally confident",
                                }
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "4",
                                        "text"     : "How confident do you feel that you can keep any other symptoms or health problems you have from interfering with the things you want to do?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 10,
                                "step"       : 1,
                                "initial"    : 6,
                                "labels"     : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                "annotations": {
                                        "minimum": "not at all confident",
                                        "maximum": "totally confident",

                                }
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "5",
                                        "text"     : "How confident do you feel that you can the different tasks and activities needed to manage your health condition so as to reduce your need to see a doctor?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 10,
                                "step"       : 1,
                                "initial"    : 6,
                                "labels"     : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                "annotations": {
                                        "minimum": "not at all confident",
                                        "maximum": "totally confident",

                                }
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "6",
                                        "text"     : "How confident do you feel that you can do things other than just taking medication to reduce how much your illness affects your everyday life?",
                                        "help_text": None
                                }
                        ]
                }
        ]
}

rand36 = {
        "tag"                : "RAND36",
        "name"               : "The RAND 36-Item Health Survey",
        "description"        : "The RAND 36-Item Health Survey (Version 1.0) laps eight concepts: physical functioning, bodily pain, role limitations due to physical health problems, role limitations due to personal or emotional problems, emotional well-being, social functioning, energy/fatigue, and general health perceptions. It also includes a single item that provides an indication of perceived change in health.",

        "number_of_elementss": 11,

        "elements"           : [
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 5,
                                "step"       : 1,
                                "initial"    : 3,
                                "labels"     : ["Excellent", "Very good", "Good", "Fair", "Poor"],
                                "annotations": None
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "1",
                                        "text"     : "In general, would you say your health is:",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 5,
                                "step"       : 1,
                                "initial"    : 3,
                                "labels"     : ["Much better now than one year ago",
                                                "Somewhat better now than one year ago",
                                                "About the same",
                                                "Somewhat worse now than one year ago",
                                                "Much worse now than one year ago"],
                                "annotations": None
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "2",
                                        "text"     : "<b>Compared to one year ago</b>, how would your rate your health in general <b>now</b>?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 3,
                                "initial"          : None,
                                "labels"           : ["Yes, Limited a Lot", "Yes, Limited a Little",
                                                      "No, Not limited at All"],
                        },
                        "text"                    : "The following items are about activities you might do during a typical day. Does <b>your health now limit you</b> in these activities? If so, how much?",
                        "number_of_questions"     : 10,
                        "questions"               : [
                                {
                                        "number"   : "3",
                                        "text"     : "<b>Vigorous activities</b>, such as running, lifting heavy objects, participating in strenuous sports",
                                        "help_text": None
                                },
                                {
                                        "number"   : "4",
                                        "text"     : "<b>Moderate activities</b>, such as moving a table, pushing a vacuum cleaner, bowling, or playing golf",
                                        "help_text": None
                                },
                                {
                                        "number"   : "5",
                                        "text"     : "Lifting or carrying groceries",
                                        "help_text": None
                                },
                                {
                                        "number"   : "6",
                                        "text"     : "Climbing <b>several</b> flights of stairs",
                                        "help_text": None
                                },
                                {
                                        "number"   : "7",
                                        "text"     : "Climbing <b>one</b> flight of stairs",
                                        "help_text": None
                                },
                                {
                                        "number"   : "8",
                                        "text"     : "Bending, kneeling, or stooping",
                                        "help_text": None
                                },
                                {
                                        "number"   : "9",
                                        "text"     : "Walking <b>more than a mile</b>",
                                        "help_text": None
                                },
                                {
                                        "number"   : "10",
                                        "text"     : "Walking <b>several blocks</b>",
                                        "help_text": None
                                },
                                {
                                        "number"   : "11",
                                        "text"     : "Walking <b>one block</b>",
                                        "help_text": None
                                },
                                {
                                        "number"   : "12",
                                        "text"     : "Bathing or dressing myself",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"           : "boolean",
                        "question_group_type_data": {
                                "initial"    : None,
                                "labels"     : None,
                                "annotations": None
                        },
                        "text"                    : "During the <b>past 4 weeks</b>, have you had any of the following problems with your work or other regular daily activities <b>as a result of your physical health?</b>",
                        "number_of_questions"     : 4,
                        "questions"               : [
                                {
                                        "number"   : "13",
                                        "text"     : "Cut down the amount of time you spent on work or other activities",
                                        "help_text": None
                                },
                                {
                                        "number"   : "14",
                                        "text"     : "<b>Accomplished less</b> than you would like",
                                        "help_text": None
                                },
                                {
                                        "number"   : "15",
                                        "text"     : "Were limited in the <b>kind</b> of work or other activities",
                                        "help_text": None
                                },
                                {
                                        "number"   : "16",
                                        "text"     : "Had <b>difficulty</b> performing the work or other activities (for example, it took extra effort)",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"           : "boolean",
                        "question_group_type_data": {
                                "initial"    : None,
                                "labels"     : None,
                                "annotations": None
                        },
                        "text"                    : "During the <b>past 4 weeks</b>, have you had any of the following problems with your work or other regular daily activities <b>as a result of any emotional problems</b> (such as feeling depressed or anxious)?",
                        "number_of_questions"     : 3,
                        "questions"               : [
                                {
                                        "number"   : "17",
                                        "text"     : "Cut down the <b>amount of time</b> you spent on work or other activities",
                                        "help_text": None
                                },
                                {
                                        "number"   : "18",
                                        "text"     : "<b>Accomplished less</b> than you would like",
                                        "help_text": None
                                },
                                {
                                        "number"   : "19",
                                        "text"     : "Didn’t do work or other activities as <b>carefully</b> as usual",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 5,
                                "step"       : 1,
                                "initial"    : 1,
                                "labels"     : ["Not at all", "Slightly", "Moderately", "Quite a bit", "Extremely"],
                                "annotations": None
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "20",
                                        "text"     : "During the <b>past 4 weeks</b>, to what extent has your physical health or emotional problems interfered with your normal social activities with family, friends, neighbours, or groups?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 6,
                                "step"       : 1,
                                "initial"    : 1,
                                "labels"     : ["None", "Very mild", "Mild", "Moderate", "Severe", "Very severe"],
                                "annotations": None
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "21",
                                        "text"     : "How much <b>bodily</b> pain have you had during the <b>past 4 weeks</b>?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 5,
                                "step"       : 1,
                                "initial"    : 1,
                                "labels"     : ["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                                "annotations": None
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "22",
                                        "text"     : "During the <b>past 4 weeks</b>, how much did <b>pain</b> interfere with your normal work (including both work outside the home and housework)?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 6,
                                "step"       : 1,
                                "initial"    : 6,
                                "labels"     : [
                                        "All of the Time",
                                        "Most of the Time",
                                        "A Good Bit of the Time",
                                        "Some of the Time",
                                        "A Little of the Time",
                                        "None of the Time"
                                ],
                                "annotations": None
                        },
                        "text"                    : "These questions are about how you feel and how things have been with you <b>during the past 4 weeks</b>. For each question, please give the one answer that comes closest to the way you have been feeling. How much of the time during the past 4 weeks...",
                        "number_of_questions"     : 9,
                        "questions"               : [
                                {
                                        "number"   : "23",
                                        "text"     : " Did you feel full of pep?",
                                        "help_text": None
                                },
                                {
                                        "number"   : "24",
                                        "text"     : "Have you been a very nervous person?",
                                        "help_text": None
                                },
                                {
                                        "number"   : "25",
                                        "text"     : "Have you felt so down in the dumps that nothing could cheer you up?",
                                        "help_text": None
                                },
                                {
                                        "number"   : "26",
                                        "text"     : "Have you felt calm and peaceful?",
                                        "help_text": None
                                },
                                {
                                        "number"   : "27",
                                        "text"     : "Did you have a lot of energy?",
                                        "help_text": None
                                },
                                {
                                        "number"   : "28",
                                        "text"     : "Have you felt downhearted and blue?",
                                        "help_text": None
                                },
                                {
                                        "number"   : "29",
                                        "text"     : "Did you feel worn out?",
                                        "help_text": None
                                },
                                {
                                        "number"   : "30",
                                        "text"     : "Have you been a happy person?",
                                        "help_text": None
                                },
                                {
                                        "number"   : "31",
                                        "text"     : "Did you feel tired?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 5,
                                "step"       : 1,
                                "initial"    : 1,
                                "labels"     : [
                                        "All of the Time",
                                        "Most of the Time",
                                        "A Good Bit of the Time",
                                        "Some of the Time",
                                        "A Little of the Time",
                                        "None of the Time"
                                ],
                                "annotations": None
                        },
                        "text"                    : None,
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "32",
                                        "text"     : "During the <b>past 4 weeks</b>, how much of the time has your <physical health or emotional problems interfered with your social activities (like visiting with friends, relatives, etc.)?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "integer_range",
                        "question_group_type_data": {
                                "minimum"    : 1,
                                "maximum"    : 5,
                                "step"       : 1,
                                "initial"    : 3,
                                "labels"     : [
                                        "Definitely True",
                                        "Mostly True",
                                        "Don’t Know",
                                        "Mostly False",
                                        "Definitely False"
                                ],
                                "annotations": None
                        },
                        "text"                    : "How <b>TRUE</b> or <b>FALSE</b> is each of the following statements for you.",
                        "number_of_questions"     : 4,
                        "questions"               : [
                                {
                                        "number"   : "33",
                                        "text"     : "I seem to get sick a little easier than other people",
                                        "help_text": None
                                },
                                {
                                        "number"   : "34",
                                        "text"     : "I am as healthy as anybody I know",
                                        "help_text": None
                                },
                                {
                                        "number"   : "35",
                                        "text"     : "I expect my health to get worse",
                                        "help_text": None
                                },
                                {
                                        "number"   : "36",
                                        "text"     : "My health is excellent",
                                        "help_text": None
                                }
                        ]
                }
        ]
}

survey_list = [semcd6, rand36]

debug = False

def _s(s: str):
    if debug: print(f"_s({s})")
    return String.objects.create(value=s) if s is not None else None


def _t(s: str):
    if debug: print(f"_t({s})")
    return Text.objects.create(value=s) if s is not None else None


def _g(s: str):
    if debug: print(f"_g({s})")
    return StringGroup.objects.create(value=s) if s is not None and s not in ["{}"] else None


def _k(s: dict, key, default=None):
    if debug: print(f"_k({key}, {default})")
    return s.get(key) if (key in s.keys() and s.get(key) is not None) else default


def _n(s: dict, pre: str = "", default=""):
    if debug: print(f"_n({pre}, {default})")
    temp = _k(s, "name", default)
    return _s(pre + temp) if temp is not None else default


def _d(s: dict, pre: str = "", default=""):
    if debug: print(f"_d({pre}, {default})")
    temp = _k(s, "description", default)
    return _t(pre + temp) if temp is not None else default


def _a(s: dict, pre: str = "", default=None):
    if debug: print(f"_a({pre}, {default})")
    temp = _k(s, "annotations", default)
    return _g(pre + json.dumps(temp)) if temp is not None else default


def _l(s: dict, pre: str = "", default=None):
    if debug: print(f"_l({pre}, {default})")
    temp = _k(s, "labels", default)
    return _g(pre + json.dumps(temp)) if temp is not None else default


def _b(q: dict, key: str, default):
    temp = _k(q, key, None)
    return bool(temp) if temp is not None else default


def _nd(s: dict):
    if debug: print(f"_nd()")
    return {"name": _n(s), "description": _d(s)}


def _end(e: dict, tag: str, n: int):
    if debug: print(f"_end()")
    return {
            "name"       : _n(e, tag + f".{n}.", f"element"),
            "description": _d(e, tag + f" #{n}: ", None),  # f"element #{n}"),
            "text"       : _t(_k(e, "text", None)),
            "help_text"  : _t(_k(e, "help_text", None)),
            "number"     : n,
            "prefix"     : _k(e, "number", "")
    }


def _qty(g: dict):
    if debug: print(f"_qty()")
    type = None

    if g["question_group_type"] == "text":
        type = QuestionGroup.DataType.TEXT.value
    elif g["question_group_type"] == "int":
        type = QuestionGroup.DataType.INT.value
    elif g["question_group_type"] == "float":
        type = QuestionGroup.DataType.FLOAT.value
    elif g["question_group_type"] == "integer_range":
        type = QuestionGroup.DataType.INT_RANGE.value
    elif g["question_group_type"] == "boolean":
        type = QuestionGroup.DataType.BOOLEAN.value
    elif g["question_group_type"] == "exclusive_choices":
        type = QuestionGroup.DataType.EXCLUSIVE.value
    elif g["question_group_type"] == "multi_choices":
        type = QuestionGroup.DataType.CHOICES.value
    elif g["question_group_type"] == "float_range":
        type = QuestionGroup.DataType.FLOAT_RANGE.value

    return {
            "type": type
    }


def _qir(q: dict):
    if debug: print(f"_qir()")
    ir = {
            "initial": _k(q, "initial", 1),
            "min"    : _k(q, "minimum", 1),
            "max"    : _k(q, "maximum", 5),
            "step"   : _k(q, "step", 1),
            "labels" : _l(q)
    }

    ir["num_possibilities"] = (ir["max"] - ir["min"]) // ir["step"]

    return ir


def _qbl(q: dict):
    if debug: print(f"_qbl()")
    bl = {
            "initial": _k(q, "initial", -1),
            "labels" : _l(q)
    }

    bl["num_possibilities"] = 2

    return bl


def _qxc(q: dict):
    if debug: print(f"_qxc()")
    bl = {
            "initial": _k(q, "initial", -1),
            "labels" : _l(q)
    }

    bl["num_possibilities"] = _k(q, "number_of_choices", len(_k(q, "labels", [])))

    return bl


def _qnd(q: dict, tag: str, n: int, m: int):
    if debug: print(f"_qnd()")
    temp = {
            "name"       : _n(q, tag + f".{n}.{m}.", f"question"),
            "description": _d(q, tag + f" #{n}.{m}: ", None),  # f"question #{n}.{m}"),
            "text"       : _t(_k(q, "text", None)),
            "help_text"  : _t(_k(q, "help_text", None)),
            "number"     : m,
            "prefix"     : _k(q, "number", ""),
            "annotations": _a(q)
    }

    op = _k(q, "optional", None)
    if op is not None: temp["optional"] = op

    return temp


def load_survey(s: dict):
    tag: str = s["tag"]

    form = Form.objects.create(type=Form.FormType.SURVEY.value, tag=tag, **_nd(s))

    survey = Survey.objects.create(form=form)

    print(f"created: {form}")

    element = None
    n = 1
    elements = []
    element_questions = {}
    element_types = {}
    for e in s["elements"]:
        questions = None
        qtype = None
        if e["element_type"] == "text":
            print(f"starting #{n}: text")
            element = TextElement.objects.create(form=form, **_end(e, tag, n))
        elif e["element_type"] == "question_group":
            print(f"starting #{n}: question group " + e["question_group_type"])
            d = _k(e, "question_group_type_data", {})
            element = QuestionGroup.objects.create(form=form, **_end(e, tag, n), **_qty(e), annotations=_a(d))

            if e["question_group_type"] == "text":
                pass
            elif e["question_group_type"] == "int":
                pass
            elif e["question_group_type"] == "float":
                pass
            elif e["question_group_type"] == "integer_range":
                qtype = IntRangeQuestion.objects.create(group=element, **_qir(d))
            elif e["question_group_type"] == "boolean":
                qtype = BooleanChoiceQuestion.objects.create(group=element, **_qbl(d))
            elif e["question_group_type"] == "exclusive_choices":
                qtype = ExclusiveChoiceQuestion.objects.create(group=element, **_qxc(d))
            elif e["question_group_type"] == "multi_choices":
                pass
            elif e["question_group_type"] == "float_range":
                pass

            m = 0
            questions = []
            for q in _k(e, "questions", []):
                print(f"starting #{n}.{m}")
                question = Question.objects.create(group=element, **_qnd(q, tag, n, m))
                elements.append(element)
                print(f"created #{m}: {question}")
                questions.append(question)
                m += 1

        else:
            continue

        elements.append(element)
        if questions is not None:
            element_questions[element] = questions
        if qtype is not None:
            element_types[element] = qtype
        print(f"created #{n}: {element}")
        n += 1
    return {
            "tag"      : tag,
            "survey"   : survey,
            "form"     : form,
            "elements" : elements,
            "types"    : element_types,
            "questions": element_questions
    }

empty_string = _s("")
empty_text = _t("")
empty_string_group = _g("{}")

loaded = [load_survey(s) for s in survey_list]

# python ./manage.py shell
# exec(open("./load_surveys.py").read())
