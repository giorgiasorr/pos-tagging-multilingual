########## Temporary Data ##########
true_tags = ["NN", "DT", "P", "HYP", "NN", "P", "DT","DT"] #correct(GoldStandard data)
dummy_tags = ["NN", "VB", "P", "P", "DT", "P", "HYP","DT"]  #predicted(Dummy data)
tag = ["NN","P","DT"] # Multi label
# tag = "P" # Single label
########## Temporary Data ##########



########## Function to get tp,fp,fn,tn values ##########
def matrix_values(y_true,y_pred,label): # check position of parameter
    each_tag = {} 
    for j in range (len(label)):
        # initialize variables 
        true_positive = 0
        true_negative = 0
        false_negative = 0
        false_positive = 0
        
        if (len(y_true)) == (len(y_pred)):          # procceed only if the length is the same
            for i in range(len(y_true)):
                if (y_true[i] == label[j]) and (y_pred[i] == label[j]):
                    true_positive = true_positive+1             # if conditions met then increment true_positive by 1
                elif (y_true[i] == label[j]) and (y_pred[i] != label[j]):
                    false_negative = false_negative+1           # if conditions met then increment false_negative by 1
                elif (y_true[i] != label[j]) and (y_pred[i] == label[j]):
                    false_positive = false_positive+1           # if conditions met then increment false_positive by 1
                elif (y_true[i] != label[j]) and (y_pred[i] != label[j]):
                    true_negative=true_negative+1               # if conditions met then increment true_negative by 1
        else:
            print("******\nTHE LENGTH OF CORRECT and PREDICTED LIST IS DIFFERENT\n*****")
        each_tag[label[j]] = [[true_positive, false_positive],[false_negative,true_negative]]
        # print("True positive1",true_positive)
        # print("False positive1",false_positive)
        # print("False negative1",false_negative)
        # print("True negative1",true_negative)
            
    return each_tag
########## Function to get tp,fp,fn,tn values ##########



print(matrix_values(true_tags,dummy_tags,tag)) #testing function matrix_values



########## Function to calculate Precision & Recall ##########
def calculate_precision_recall(y_true,y_pred,label):
    values = matrix_values(y_true,y_pred,label)             # call matrix_values to get tp,fp,fn,tn values
    PrecisionDict = {}
    RecallDict = {}
    Final_values = {"Precision":PrecisionDict, "Recall":RecallDict}
    for i in values:
    # Formula for Precision & Recall 
        PrecisionDict[i] = values[i][[0][0]][0]/(values[i][[0][0]][0]+values[i][[0][0]][1])  #since i stored it in nested list/array this is how we get the values 
        RecallDict[i] = values[i][[0][0]][0]/(values[i][[0][0]][0]+values[i][[1][0]][0])    
    # # print("True negative",values[[1][0]][1]) 
    return Final_values
########## Function to calculate Precision & Recall ##########



print(calculate_precision_recall(true_tags,dummy_tags,tag)) #testing function calculate_precision_recall



########## Function to calculate F1_Score ##########
def calculate_f1score(y_true,y_pred,label):
    prvalues = calculate_precision_recall(y_true,y_pred,label) # call matrix_values to get tp,fp,fn,tn values
    # only_precision = values[i]
    # Precision,Recall = calculate_precision_recall(y_true,y_pred,label) 
    Precision = prvalues["Precision"]
    Recall = prvalues["Recall"]
    F1_ScoreDict = {}
    for i in range(len(label)):  
        # F1_Score= 2*(Precision.get(label[i])*Recall.get(label[i]))/(Precision.get(label[i]) + Recall.get(label[i]))
        F1_ScoreDict[label[i]] = 2*(Precision.get(label[i])*Recall.get(label[i]))/(Precision.get(label[i]) + Recall.get(label[i]))
    return F1_ScoreDict
########## Function to calculate F1_Score ##########



print(calculate_f1score(true_tags,dummy_tags,tag)) #testing function calculate_f1score


########## Function to calculate Macro F1_Score ##########
def macro_average(y_true,y_pred,label):
    FScores= calculate_f1score(y_true,y_pred,label)
    total = 0
    for i in FScores:
        total = total + FScores[i]
    macro_F1Score = total / len(FScores)
    return macro_F1Score
########## Function to calculate Macro F1_Score ##########

print(macro_average(true_tags,dummy_tags,tag)) #testing function macro_average