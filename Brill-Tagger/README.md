# Team Details

- Team name : Fairies
- Team members : Aditya Kadam, Giorgia Sorrentino, Samia Qbaibi

# Task Details

- Task : Part-of-Speech Tagger
- Approach : Brill Tagger
- Evaluation :  Macro & Micro F1-Scores
- Language : Python

# How to run the files

learning_algorithm.py is the file that performs transformation based brill by using learning algorithm for English, Italian & French.

contextual_rules.py is the file that performs rule based brill for English language.

evaluation.py is the evaluation file

train.col, test.col : Data from IMS server
it_train.col, it_test.col, fr_train.col, fr_test.col : Data from universaldependencies.org

- Keep all of these files in the same folder;

[Rule Based] # Baseline
- Run contextual_rules.py ; 
- On running contextual_rules.py, the Accuracy, Macro & Micro average F1-Score values will be calculated and printed for English data. 

[Transformation Based]
- Run learning_algorithm.py ;
- On running learning_algorithm.py, the Accuracy, Macro & Micro average F1-Score values will be calculated and printed for English, Italian & French data. Estimated time : 1 Hour 
