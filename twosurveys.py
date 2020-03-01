linq = {
        "tag"        : "LINQ",
        "name"       : "Lung Information Needs Questionnaire",
        "description": "The questionnaire measures the extent to which the patient needs more information, as perceived by the patient and clinician.",
        "elements"   : [
                {
                        "element_type": "text",
                        "name"        : "Intro",
                        "description" : "Intro Paragraph",
                        "text"        : "The questionnaire is reproduced on the following with the scores indicated against the different response options"
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "boolean",
                        "question_group_type_data": {
                               "number_of_choices": 2,
                                "initial"         : None,
                                "labels"          : ["Yes, No"],
                        },
                        "text"                    : "Please answer the following",
                        "number_of_questions"     : 3,
                        "questions"               : [
                                {
                                        "number"   : "1",
                                        "text"     : "Do you know the name of your lung disease?",
                                        "help text": None
                                },
                                {
                                        "number"   : "2",
                                        "text"     : "Has a doctor or nurse told you how this disease affects your lungs?",
                                        "help text": None
                                },
                                {
                                        "number"   : "3",
                                        "text"     : "Has a doctor or nurse told you what is likely to happen in the future?",
                                        "help text": None
                                },

                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                               "number_of_choices": 4,
                                "initial"         : None,
                                "labels"          : ["I will get worse", "Now that my disease is being treated, I will probably 1 stay the same",
                                                     "Now that my disease is being treated, I will probably 1 get better", "I have no idea"],
                        },
                        "number_of_questions": 1,
                        "questions": [
                                {
                                        "number"   : "4",
                                        "text"     : "Which of the following statements best describes what will happen to you over the next few years?",
                                        "help_text": None
                                }]

                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "boolean",
                        "question_group_type_data": {
                               "number_of_choices": 2,
                                "initial"         : None,
                                "labels"          : ["Yes, No"],
                        },
                        "number_of_questions"     : 2,
                        "questions"               : [
                                {
                                        "number"   : "5",
                                        "text"     : "Has a doctor or nurse explained the <b>reason</b> for taking your inhalers or medicines?",
                                        "help text": None
                                },
                                {
                                        "number"   : "6",
                                        "text"     : "Do you <b>try</b> to take your inhalers or medicines <b>exactly</b> as you have been instructed by a doctor or nurse?",
                                        "help text": None
                                },
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 4,
                                "initial"          : None,
                                "labels"           : ["I understand everything I need to know",
                                                      "I understand what I have been told but I would 1 like to know more",
                                                      "I am slightly confused about my medicines",
                                                      "I am very confused about my medicines"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "7",
                                        "text"     : "Are you satisfied with the information doctors and nurses have given you about your inhalers or medicines?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 4,
                                "initial"          : None,
                                "labels"           : ["I have been told what to do and the doctor/nurse has given me written instructions",
                                                      "I have been told but it is not written on paper",
                                                      "I haven't been told but I know what to do",
                                                      "I haven't been told and I don’t know what to do"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "8",
                                        "text"     : "What sentence best describes what you have been told to do if your breathing gets worse (e.g., take two puffs instead of one)?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 4,
                                "initial"          : None,
                                "labels"           : ["I have been told what to do and the doctor/nurse 0 Has given me written instructions",
                                                      "I have been told but it isn't written on paper",
                                                      "I haven't been told but I know what to do",
                                                      "I haven't been told and I am uncertain when an ambulance should be called"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "9",
                                        "text"     : "Have you been told when you should call an <b>ambulance</b> if your breathing worsens?",
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
                                "labels"           : ["Never smoked (go to question 13)",
                                                      "Used to smoke but don't now (go to question 13)",
                                                      "Still smoking (go to question 11)"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "10",
                                        "text"     : "What best describes you?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "boolean",
                        "question_group_type_data": {
                                "number_of_choices": 2,
                                "initial"          : None,
                                "labels"           : ["Yes, No"],
                        },
                        "number_of_questions"     : 3,
                        "questions"               : [
                                {
                                        "number"   : "11",
                                        "text"     : "Has a doctor or nurse advised you to give up smoking?",
                                        "help text": None
                                },
                                {
                                        "number"   : "12",
                                        "text"     : "Has a doctor or nurse offered to help you to give up smoking?"
                                                     "(e.g., given you nicotine gum or patches referral to a Smoking Cessation clinic)?",
                                        "help text": None
                                },
                                {
                                        "number"   : "13",
                                        "text"     : "Have you been told by a doctor or nurse to try to do some physical activity "
                                                     "(e.g., walking, brisk walking and other forms of exercise?",
                                        "help text": None
                                },
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 4,
                                "initial"          : None,
                                "labels"           : ["Yes and I know what to do",
                                                      "Yes but I am unsure what to do",
                                                      "Yes but I am unable to do it",
                                                      "No"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "14",
                                        "text"     : "Has a doctor or nurse told you <b>how much</b> physical activity"
                                                     "(e.g., walking, brisk walking and other forms of exercise) you should do?",
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
                                "labels"           : ["I push myself as much as I can",
                                                      "I make an effort",
                                                      "As little as possible"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "15",
                                        "text"     : "How much physical activity do you do?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 4,
                                "initial"          : None,
                                "labels"           : ["Eat several small meals per day "
                                                      "'(e.g., 6 small meals per day instead of 3 large ones)'",
                                                      "Lose or gain weight",
                                                      "Eat healthy food",
                                                      "Nothing"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "16",
                                        "text"     : "What have doctors or nurses told you about your diet or eating?",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 0,
                                "initial"          : None,
                                "labels"           : [],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "17",
                                        "text"     : "Have you any questions or comments about your lung disease?"
                                                     "If so, write them in the space below",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 2,
                                "initial"          : None,
                                "labels"           : ["Male, Female"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "18",
                                        "text"     : "Sex",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 0,
                                "initial"          : None,
                                "labels"           : [],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "19",
                                        "text"     : "In which year were you born?",
                                        "help_text": None
                                }
                        ]
                },
        ]
}

