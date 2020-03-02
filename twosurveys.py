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

sgrg = {
        "tag"        : "SGRG",
        "name"       : "St. George Respiratory Questionnaire",
        "description": "This questionnaire is designed to help us learn much more about how your breathing is troubling you and how it affects your life.",
        "elements"   : [
                {
                        "element_type": "text",
                        "name"        : "Intro",
                        "description" : "Intro Paragraph",
                        "text"        : "Please read the instructions carefully and ask if you do not understand anything. Do not spend too long deciding about your answers."
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                               "number_of_choices": 5,
                               "initial"          : None,
                               "labels"           : ["Most days a week", "Several days a week",
                                                      "A few days a month", "Only with chest infections",
                                                      "Not at all"],
                },
                        "text"                    : "<b>Questions about how much chest trouble you have had over the past 3 months.</b>",
                        "number_of_questions"     : 4,
                        "questions"               : [
                                {
                                        "number"   : "1",
                                        "text"     : "Over the past 3 months, I have coughed:",
                                        "help_text": None
                                },
                                {
                                        "number"   : "2",
                                        "text"     : "Over the past 3 months, I have brought up phlegm (sputum):",
                                        "help_text": None
                                },
                                {
                                        "number"   : "3",
                                        "text"     : "Over the past 3 months, I have had shortness of breath:",
                                        "help_text": None
                                },
                                {
                                        "number"   : "4",
                                        "text"     : "Over the past 3 months, I have had attacks of wheezing:",
                                        "help_text": None
                                },
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 5,
                                "initial"          : None,
                                "labels"           : ["more than 3 attacks",
                                                      "3 attacks",
                                                      "2 attacks",
                                                      "1 attack"
                                                      "no attacks"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "5",
                                        "text"     : "During the past 3 months how many severe or very unpleasant attacks of chest trouble have you had?",
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
                                "labels"           : ["a week or more",
                                                      "3 or more days",
                                                      "1 or 2 days",
                                                      "less than a day"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "6",
                                        "text"     : "How long did the worst attack of chest trouble last? (Go to question 7 if you had no severe attacks)",
                                        "help_text": None
                                }
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "exclusive_choices",
                        "question_group_type_data": {
                                "number_of_choices": 5,
                                "initial"          : None,
                                "labels"           : ["No good days",
                                                      "1 or 2 good days",
                                                      "3 or 4 good days",
                                                      "nearly every day is good"
                                                      "every day is good"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "7",
                                        "text"     : "Over the past 3 months, in an average week, how many good days (with little chest trouble) have you had?",
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
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : "8",
                                        "text"     : "If you have a wheeze, is it worse in the morning?",
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
                                "labels"           : ["The most important problem I have",
                                                      "Causes me quite a lot of problems",
                                                      "Causes me a few problems",
                                                      "Causes no problem"],
                        },
                        "text"                    : "<b>Section 1</b>",
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "How would you describe your chest condition?",
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
                                "labels"           : ["My chest trouble made me stop work altogether",
                                                      "My chest trouble interferes with my work or made me change my work",
                                                      "My chest trouble does not affect my work"],
                        },
                        "number_of_questions"     : 1,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "If you have ever had paid employment.",
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
                        "text"                    : "<b>Section 2</b>"
                                                    "Questions about what activities usually make you feel breathless <u>these days.</u></b>",
                        "number_of_questions"     : 7,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "Sitting or lying still",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Getting washed or dressed",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Walking around the home",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Walking outside on the level",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Walking up a flight of stairs",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Walking up hills",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Playing sports or games",
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
                        "text"                    : "<b>Section 3</b>"
                                                    "<b>Some more questions about your cough and breathlessness <u>these days.</u></b>",
                        "number_of_questions"     : 6,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "My cough hurts",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "My cough makes me tired",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I am breathless when I talk",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I am breathless when I bend over",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "My cough or breathing disturbs my sleep",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I get exhausted easily",
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
                        "text"                    : "<b>Section 4</b>"
                                                    "<b>Questions about other effects that your chest trouble may have on you <u>these days.</u></b>",
                        "number_of_questions"     : 8,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "My cough or breathing is embarrassing in public",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "My chest trouble is a nuisance to my family, friends or neighbours",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I get afraid or panic when I cannot get my breath",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I feel that I am not in control of my chest problem",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I do not expect my chest to get any better",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I have become frail or an invalid because of my chest",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Exercise is not safe for me",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Everything seems too much of an effort",
                                        "help_text": None
                                },
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
                        "text"                    : "<b>Section 5</b>"
                                                    "<b>Questions about your medication, if you are receiving no medication go straight to section 6.</b>",
                        "number_of_questions"     : 4,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "My medication does not help me very much",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I get embarrassed using my medication in public",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I have unpleasant side effects from my medication",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "My medication interferes with my life a lot",
                                        "help_text": None
                                },
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
                        "text"                    : "<b>Section 6</b>"
                                                    "<b>These are questions about how your activities might be affected by your breathing.</b>",
                        "number_of_questions"     : 9,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "I take a long time to get washed or dressed",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I cannot take a bath or shower, or I take a long time",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I walk slower than other people, or I stop for rests",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Jobs such as housework take a long time, or I have to stop for rests",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "If I walk up one flight of stairs, I have to go slowly or stop",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "If I hurry or walk fast, I have to stop or slow down",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "My breathing makes it difficult to do things such as walk up hills, carrying things "
                                                     "up stairs, light gardening such as weeding, dance, play bowls or play golf",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "My breathing makes it difficult to do things such as carry heavy loads, dig the "
                                                     "garden or shovel snow, jog or walk at 5 miles per hour, play tennis or swim",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "My breathing makes it difficult to do things such as very heavy manual work,"
                                                     "run, cycle, swim fast or play competitive sports",
                                        "help_text": None
                                },
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
                        "text"                    : "<b>Section 7</b>"
                                                    "<b>We would like to know how your chest <u>usually</u> affects your daily life.</b>",
                        "number_of_questions"     : 5,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "I cannot play sports or games",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I cannot go out for entertainment or recreation",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I cannot go out of the house to do the shopping",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I cannot do housework",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "I cannot move far from my bed or chair",
                                        "help_text": None
                                },
                        ]
                },
                {
                        "element_type"            : "question_group",
                        "number"                  : None,
                        "question_group_type"     : "text",
                        "question_group_type_data": {
                                "min_length"      : 0,
                                "max_length"      : 20,
                                "labels"           : ["Yes, No"],
                        },
                        "text"                    : "<b>Here is a list of other activities that your chest trouble may prevent you doing. "
                                                    "(You do not have to tick these, they are just to remind you of ways in which your breathlessness may affect you):</b>",
                        "number_of_questions"     : 6,
                        "questions"               : [
                                {
                                        "number"   : " ",
                                        "text"     : "Going for walks or walking the dog",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Doing things at home or in the garden",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Sexual intercourse",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Going out to church, pub, club or place of entertainment",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Going out in bad weather or into smoky rooms",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "Visiting family or friends or playing with children",
                                        "help_text": None
                                },
                        ],
                        "text"                    : "Please write in any other important activities that your chest trouble may stop you doing:",
                        "text"                    : "Now would you tick in the box (one only) which you think best describes how your chest affects you:",
                        "number_of_questions": 4,
                        "questions"          : [
                                {
                                        "number"   : " ",
                                        "text"     : "It does not stop me doing anything I would like to do",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "It stops me doing one or two things I would like to do",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "It stops me doing most of the things I would like to do",
                                        "help_text": None
                                },
                                {
                                        "number"   : " ",
                                        "text"     : "It stops me doing everything I would like to do",
                                        "help_text": None
                                },
                        ],
                        "text"                    : "Thank you for filling in this questionnaire. "
                                                    "Before you finish would you please check to see that you have answered all the questions.",
                },

        ]
}