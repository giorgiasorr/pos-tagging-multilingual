######### Temporary Data for testing ##########
true_tags = ["NN", "DT", "P", "HYP", "NN", "P", "DT", "DT"]  # correct(GoldStandard data)
dummy_tags = ["NN", "VB", "P", "P", "DT", "P", "HYP", "DT"]  # predicted(Dummy data)
tag = ["NN", "P", "DT"]  # Multi label
# tag = "P" # Single label
########## Temporary Data ##########


########## Function to get tp, fp, fn, tn values ##########
def matrix_values(y_true, y_pred, label):  # check position of parameter
    each_tag = {}
    for j in range(len(label)):
        # initialize variables
        true_positive = 0
        true_negative = 0
        false_negative = 0
        false_positive = 0

        if len(y_true) == len(y_pred):  # proceed only if the length is the same
            for i in range(len(y_true)):
                if (y_true[i] == label[j]) and (y_pred[i] == label[j]):
                    true_positive += 1  # increment true_positive by 1
                elif (y_true[i] == label[j]) and (y_pred[i] != label[j]):
                    false_negative += 1  # increment false_negative by 1
                elif (y_true[i] != label[j]) and (y_pred[i] == label[j]):
                    false_positive += 1  # increment false_positive by 1
                elif (y_true[i] != label[j]) and (y_pred[i] != label[j]):
                    true_negative += 1  # increment true_negative by 1
        else:
            print("******\nTHE LENGTH OF CORRECT and PREDICTED LIST IS DIFFERENT\n*****")
        each_tag[label[j]] = [
            [true_positive, false_positive],
            [false_negative, true_negative],
        ]

    return each_tag


########## Function to get tp, fp, fn, tn values ##########


# print(matrix_values(true_tags,dummy_tags,tag)) #testing function matrix_values


########## Function to calculate Precision & Recall ##########
def calculate_precision_recall(y_true, y_pred, label):
    values = matrix_values(y_true, y_pred, label)  # call matrix_values to get tp, fp, fn, tn values
    PrecisionDict = {}
    RecallDict = {}
    Final_values = {"Precision": PrecisionDict, "Recall": RecallDict}
    for i in values:
        tp = values[i][0][0]
        fp = values[i][0][1]
        fn = values[i][1][0]
        PrecisionDict[i] = tp / (tp + fp) if (tp + fp) > 0 else 0  # handle division by zero
        RecallDict[i] = tp / (tp + fn) if (tp + fn) > 0 else 0  # handle division by zero
    return Final_values


########## Function to calculate Precision & Recall ##########


# print(calculate_precision_recall(true_tags,dummy_tags,tag)) #testing function calculate_precision_recall


########## Function to calculate F1_Score ##########
def calculate_f1score(y_true, y_pred, label):
    prvalues = calculate_precision_recall(y_true, y_pred, label)  # call calculate_precision_recall to get precision and recall values
    Precision = prvalues["Precision"]
    Recall = prvalues["Recall"]
    F1_ScoreDict = {}
    for i in range(len(label)):
        prec = Precision[label[i]]
        rec = Recall[label[i]]
        F1_ScoreDict[label[i]] = (
            2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0  # handle division by zero
        )
    return F1_ScoreDict


########## Function to calculate F1_Score ##########


# print(calculate_f1score(true_tags,dummy_tags,tag)) #testing function calculate_f1score


########## Function to calculate Macro F1_Score ##########
def macro_average(y_true, y_pred, labels):
    f_scores = calculate_f1score(y_true, y_pred, labels)
    total_f1_score = sum(f_scores.values())
    macro_f1_score = total_f1_score / len(f_scores) if len(f_scores) > 0 else 0
    return macro_f1_score
########## Function to calculate Macro F1_Score ##########


# print(macro_average(true_tags,dummy_tags,tag)) #testing function macro_average


########## Function to calculate Micro F1_Score ##########
def micro_average(y_true, y_pred, labels):
    values = matrix_values(y_true, y_pred, labels)
    total_tp = 0
    total_fp = 0
    total_fn = 0
    for label in labels:
        tp = values[label][0][0]
        fp = values[label][0][1]
        fn = values[label][1][0]
        total_tp += tp
        total_fp += fp
        total_fn += fn
    # Calculate overall precision and recall
    overall_precision = (
        total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    )
    overall_recall = (
        total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    )
    # Calculate micro-average F1 score
    if overall_precision + overall_recall > 0:
        micro_f1 = (
            2 * (overall_precision * overall_recall) / (overall_precision + overall_recall)
        )
    else:
        micro_f1 = 0

    return micro_f1


########## Function to calculate Micro F1_Score ##########


# print(micro_average(true_tags,dummy_tags,tag)) #testing function macro_average



########## Accuracy ##########
def calculate_accuracy(y_true, y_pred):
    correct_predictions = 0
    total_predictions = len(y_true)

    for true_tag, pred_tag in zip(y_true, y_pred):
        if true_tag == pred_tag:
            correct_predictions += 1

    accuracy = correct_predictions / total_predictions
    return accuracy


########## Accuracy ##########


def evaluate(gold_tags, annotated_tags, labels):
    "import the evaluation file to compare the tags from after_rule_corpus and test. Calculate and print macro_average, micro_average, F1-score, Precision and Recall"
    final_annotated_tags = []
    for i in annotated_tags:
        for j in i:
            final_annotated_tags.append(j[1])

    final_gold_tags = []
    for i in gold_tags:
        for j in i:
            final_gold_tags.append(j[1])
    print("length of gold standard list : ", len(final_gold_tags))
    print("length of final list : ", len(final_annotated_tags))
    try:
        print("Accuracy : ", calculate_accuracy(final_gold_tags, final_annotated_tags))
    except ZeroDivisionError as e:
        print("Error in calculate_accuracy calculation:", e)
    try:
        print(
        "Macro Average values for given labels : ",
        macro_average(final_gold_tags, final_annotated_tags, labels),
    )  # testing function macro_average
    except ZeroDivisionError as e:
        print("Error in macro_average calculation:", e)
    try:
        print(
        "Micro Average values for given labels : ",
        micro_average(final_gold_tags, final_annotated_tags, labels),
    )  # testing function micro_average
    except ZeroDivisionError as e:
        print("Error in micro_average calculation:", e)
    try : 
        print(
        "F1 Score for given labels : ",
        calculate_f1score(final_gold_tags, final_annotated_tags, labels),
    )  # testing function calculate_f1score
    except ZeroDivisionError as e:
        print("Error in calculate_f1score calculation:", e)
    try:
        print(
        "Precision-Recall for given labels : ",
        calculate_precision_recall(
            final_gold_tags, final_annotated_tags, labels
        ),
    )  # testing function calculate_f1score
    except ZeroDivisionError as e:
        print("Error in calculate_precision_recall calculation:", e)
    try:
        print(
        "Matrix values for given labels : ",
        matrix_values(final_gold_tags, final_annotated_tags, labels),
    )  # testing function calculate_f1score
    except ZeroDivisionError as e:
        print("Error in matrix_values calculation:", e)
    return

# Test the evaluate function with some dummy data
# evaluate([["DT", "NN"], ["VB", "DT"], ["NN", "DT"]], [["DT", "NN"], ["VB", "NN"], ["NN", "VB"]], ["DT", "NN", "VB"])
