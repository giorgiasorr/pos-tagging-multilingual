########## Temporary Data ##########
true_tags = ["NN", "DT", "P", "HYP"] #correct(GoldStandard data)
dummy_tags = ["NN", "VB", "P", "P"]  #predicted(Dummy data)
tag = "P" # Single label
########## Temporary Data ##########



########## Function to get tp,fp,fn,tn values ##########
def matrix_values(y_true,y_pred,label): # check position of parameter
    # initialize variables 
    true_positive = 0
    true_negative = 0
    false_negative = 0
    false_positive = 0
    if (len(y_true)) == (len(y_pred)):          # procceed only if the length is the same
        for i in range(len(y_true)):
            if (y_true[i] == label ) and (y_pred[i] == label):
                true_positive = true_positive+1             # if conditions met then increment true_positive by 1
            elif (y_true[i] == label ) and  (y_pred[i] != label):
                false_negative = false_negative+1           # if conditions met then increment false_negative by 1
            elif (y_true[i] != label ) and  (y_pred[i] == label):
                false_positive = false_positive+1           # if conditions met then increment false_positive by 1
            elif (y_true[i] != label ) and  (y_pred[i] != label):
                true_negative=true_negative+1               # if conditions met then increment true_negative by 1
    else:
        print("******\nTHE LENGTH OF CORRECT and PREDICTED LIST IS DIFFERENT\n*****")
    # print("True positive1",true_positive)
    # print("False positive1",false_positive)
    # print("False negative1",false_negative)
    # print("True negative1",true_negative)
    return [[true_positive, false_positive],[false_negative,true_negative]]
########## Function to get tp,fp,fn,tn values ##########



print(matrix_values(true_tags,dummy_tags,tag)) #testing function matrix_values



########## Function to calculate Precision & Recall ##########
def calculate_precision_recall(y_true,y_pred,label):
    values = matrix_values(y_true,y_pred,label)             # call matrix_values to get tp,fp,fn,tn values
    # Formula for Precision & Recall 
    Precision = values[[0][0]][0]/(values[[0][0]][0]+values[[0][0]][1])  #since i stored it in nested list/array this is how we get the values 
    Recall = values[[0][0]][0]/(values[[0][0]][0]+values[[1][0]][0])    
    # print("True negative",values[[1][0]][1]) 
    return Precision,Recall
########## Function to calculate Precision & Recall ##########



print(calculate_precision_recall(true_tags,dummy_tags,tag)) #testing function calculate_precision_recall



########## Function to calculate F1_Score ##########
def calculate_f1score(y_true,y_pred,label):
    Precision,Recall = calculate_precision_recall(y_true,y_pred,label) # call matrix_values to get tp,fp,fn,tn values
    F1_Score= 2*(Precision*Recall)/(Precision + Recall)
    return F1_Score
########## Function to calculate F1_Score ##########



print(calculate_f1score(true_tags,dummy_tags,tag)) #testing function calculate_f1score


